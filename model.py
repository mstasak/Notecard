#from PySide6.QtGui import QGuiApplication
#from PySide6.QtQml import QQmlApplicationEngine
#from PySide6.QtSql import QSqlDatabase

# Database / Model
# (ref https://doc.qt.io/qtforpython-6/tutorials/qmlsqlintegration/qmlsqlintegration.html)
# (ref https://doc.qt.io/qtforpython-6/tutorials/qmlsqlintegration/qmlsqlintegration.html#main-py)

#import sys
# for database
#import datetime
import logging
#from PySide6.QtCore import Slot
#from PySide6.QtQml import QmlElement

from PySide6.QtCore import QDir, QFile, QStandardPaths #, QLoggingCategory
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlResult

from datastructures import CategoryRec, NotecardIdTitleRec, NotecardRec #,CategoriesOfCardRec

#dbNormallyClosed: bool = True # LET'S USE REQUESTOPEN(), RELEASEOPEN() instead

logger = logging.getLogger(__name__)

def CardRecsEqual(c1: NotecardRec, c2:NotecardRec) -> bool:
    rslt = True
    if rslt and c1.title != c2.title:
        rslt = False
    if rslt and c1.body != c2.body:
        rslt = False
    if rslt and sortedCatgIdList(c1) != sortedCatgIdList(c2):
        rslt = False
    return rslt

def sortedCatgIdList(c: NotecardRec) -> list[int]:
    rslt = [n.categoryId for n in c.categories if n.selected]
    rslt.sort()
    return rslt

class Notecard:
    def __init__(self) -> None:
        super().__init__()

        self.notecardId: int | None = None
        self.title: str = ""
        self.body: str = ""
        self.categories: list[CategoryRec] = []
        #self.categories?  maybe backed by lazy method to read table: id, title, description, selectedbycard
        #self.selectedCategories: filter categories on selectedbycard = True

    def loadWithId(self, model: CardfileModel, notecardId: int) -> bool:
        logger.info(f"Loading Card object from db card row with id={notecardId}")
        rslt: bool = True
        if model.open():
            try:
                #1, read card details
                qry: QSqlQuery = QSqlQuery(query="SELECT title,body FROM notecard WHERE notecard_id=:ncid",
                                           db=model.database)
                qry.addBindValue(notecardId)
                if qry.exec():
                    if qry.next():
                        self.notecardId = notecardId
                        self.title = qry.value(0)
                        self.body = qry.value(1)
                else:
                    rslt = False
                #del qry

                # 2, read categories
                if rslt:
                    qry = QSqlQuery(query="SELECT c.category_id, c.category, c.description, nc.notecard_id "
                                        "FROM category c LEFT JOIN notecard_category nc "
                                        "ON c.category_id = nc.category_id "
                                        "AND :cardid=nc.notecard_id "
                                        "order by 2",
                                db=model.database)
                    qry.addBindValue(self.notecardId)
                    if qry.exec():
                        self.categories = []
                        while qry.next():
                            self.categories.append(
                                CategoryRec(
                                    categoryId=qry.value(0),
                                    title=qry.value(1),
                                    description=qry.value(2),
                                    selected=not qry.isNull(3)
                                )
                            )
                            #vSelected = qry.value(3)  # null returns ' '? bizarre
                            #print(qry.value(1),'=',vSelected)
                    else:
                        rslt = False
                    #del qry

            finally:
                model.close()
        logger.info("success" if rslt else "failed")
        return rslt

    def loadNotecardRec(self, c: NotecardRec) -> None:
        self.notecardId = c.notecardId
        self.title = c.title
        self.body = c.body
        self.categories = c.categories

    def save(self, model: CardfileModel) -> bool:
        logger.info(f"Saving Card object to db card row")
        rslt: bool = False
        if model.open():
            try:
                qry: QSqlQuery
                if self.notecardId is None: #insert scenario
                    qry = QSqlQuery(query="INSERT INTO notecard(title, body) "
                                          "VALUES (:title, :body) "
                                          "RETURNING notecard_id",
                                               db=model.database)
                    qry.bindValue(":title", self.title)
                    qry.bindValue(":body", self.body)
                    if qry.exec():
                        rslt = True
                        if qry.next():
                            self.notecardId = qry.value(0)
                            rslt = True
                    else: #insert failed
                        #rslt remains False
                        pass #may want to return some error string or save it to model?
                    logger.info(f"Created notecard row with notecard_id={self.notecardId}")
                    if rslt:
                        #now add new row
                        pass
                else: #update scenario
#begintrans                    
                    qry = QSqlQuery(query="",
                                    db=model.database)
                    qry.prepare("UPDATE notecard "
                                "SET title=:title, body=:body "
                                "WHERE notecard_id=:ncid")
                    qry.bindValue(":title", self.title)
                    qry.bindValue(":body", self.body)
                    qry.bindValue(":ncid", self.notecardId)
                    if qry.exec():
                        rslt = True
                    else:
                        logger.error("Query error: %s", qry.lastError().text())
                    logger.info(f"Updated notecard row with id={self.notecardId}")

                    qry = QSqlQuery(query="",
                                    db=model.database)
                    qry.prepare("DELETE FROM notecard_category "
                                "WHERE notecard_id=:ncid")
                    qry.bindValue(":ncid", self.notecardId)
                    if qry.exec():
                        rslt = True
                    else:
                        logger.error("Query error deleting notecard_category row: %s", qry.lastError().text())
                    logger.info(f"Updated notecard row with id={self.notecardId}")

                    for catg in self.categories:
                        if catg.selected:
                            qry = QSqlQuery(query="",
                                            db=model.database)
                            qry.prepare("INSERT INTO notecard_category(notecard_id, category_id) "
                                        "VALUES (:ncid, :catgid)")
                            qry.bindValue(":ncid", self.notecardId)
                            qry.bindValue(":catgid", catg.categoryId)
                            if not qry.exec():
                                rslt = False
                                logger.error("Query error inserting notecard_category row: %s", qry.lastError().text())
                                break
                    logger.info("Updated notecard categories")
#commit
            finally:
                model.close()
            logger.info(f"{'success' if rslt else 'failed'}")
        else:
            pass #show status in app
        logger.info(f"{'success' if rslt else 'failed'}")
        return rslt

    def toCardRec(self) -> NotecardRec:
        return NotecardRec(
            notecardId=self.notecardId,
            title=self.title,
            body=self.body,
            categories=self.categories
        )
# end of class 'Card'

#from typing import TypeVarTuple

class CardList:
    def __init__(self) -> None:
        super().__init__()
        #self.cardTitles: list[tuple[int, str]] = []
        self.cardTitles: list[NotecardIdTitleRec] = []

    def load(self, model: CardfileModel) -> bool:
        rslt: bool = False
        if model.open():
            try:
                qry: QSqlQuery = QSqlQuery(query="SELECT notecard_id, title FROM notecard ORDER BY title",
                                 db=model.database)
                #qry.addBindValue(id)
                if qry.exec():
                    self.cardTitles = []
                    while qry.next():
                        self.cardTitles.append(NotecardIdTitleRec(qry.value(0), qry.value(1)))
                else:
                    self.cardTitles = [NotecardIdTitleRec(-1, "foo bad list load - " + str(qry.isValid()))]
                rslt = True
            finally:
                model.close()
        return rslt

# end of class 'CardList'

class CardfileModel:

    table_ddl: list[str] = [

"""CREATE TABLE notecard (
  notecard_id INT PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  body VARCHAR(UNLIMITED)
)""",

"""CREATE TABLE category (
  category_id INT PRIMARY KEY,
  category VARCHAR(160),
  description VARCHAR(UNLIMITED)
)""",

"""CREATE TABLE notecard_category (
  notecard_category_id INT PRIMARY KEY,
  notecard_id FOREIGN KEY REFERENCES notecard(notecard_id) ON DELETE CASCADE,
  category_id FOREIGN KEY REFERENCES category(category_id) ON DELETE CASCADE
)""" 

    ]

    def __init__(self) -> None:
        super().__init__()
        self.success: bool
        self.error: str
        self.rows: int
        self.lastId: int
        self.database : QSqlDatabase
        #opened: bool
        #self.opened = False

    def open(self) -> bool:
        #if self.opened:
        #    return True

        #return False
        self.database = QSqlDatabase.database()
        if not self.database.isValid():
            self.database = QSqlDatabase.addDatabase("QSQLITE")
            if not self.database.isValid():
                #gLogger.error("Cannot add database")
                self.error = "QSqlDatabase could not create driver instance for SQLite."
                #gLogger.error(self.error)
                return False

        app_data = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        write_dir = QDir(app_data)
        if not write_dir.mkpath("."):
            #logger.error(f"Failed to create writable directory {app_data}")
            self.error = f"Could not create or write to directory {app_data} ."
            #gLogger.error(self.error)
            return False

        # Ensure that we have a writable location on all devices.
        abs_path = write_dir.absolutePath()
        filename = f"{abs_path}/cardfile.db"

        # When using the SQLite driver, open() will create the SQLite
        # database if it doesn't exist.
        self.database.setDatabaseName(filename)
        if not self.database.open():
            #logger.error("Cannot open database")
            self.error = f"Cannot open database {filename} ."
            QFile.remove(filename)
            return False
        else:
            #gLogger.info("database model opened")
            self.createModel()
            #self.opened = True

        return True

    def close(self):
        self.database.close()
        #gLogger.info("database model closed")
        #self.opened = False

    def tableExists(self, tName: str) -> bool:
        return tName.lower() in map(str.lower, self.database.tables())

    def createModel(self) -> bool:
        self.success = True
        self.error = ""
        if self.success and not self.tableExists("notecard"):
            self.success = self.queryExec(self.table_ddl[0])

        if self.success and not self.tableExists("category"):
            self.success = self.queryExec(self.table_ddl[1])

        if self.success and not self.tableExists("notecard_category"):
            self.success = self.queryExec(self.table_ddl[2])

        return self.success

    def populateSampleData(self) -> bool:
        return False

    def queryExec(self, query: str) -> bool:
        qry : QSqlQuery = QSqlQuery(query=query, db=self.database)
        rslt : bool = qry.exec_()
        if rslt:
            self.error=""
        else:
            self.error = qry.lastError().databaseText()
        return rslt

    def queryFetch(self, query:str) -> bool | QSqlResult:
        qry : QSqlQuery = QSqlQuery(query=query, db=self.database)
        if qry.exec_():
            self.error = ""
            return qry.result()
        else:
            self.error = qry.lastError().databaseText()
            return False

#if __name__ == "__main__":
    #app = MyApp([])

    #sets up determining data directory under %userprofile%/appdata/...
    #enables default QSettings constructor
    #app.setOrganizationName("mstasak")
    #app.setOrganizationDomain("org")
    #app.setApplicationName("notecard")

    #window = MainWindow()
    #window.setGeometry(100, 100, 1000, 700)
    #window.show()
    #windowContent:Ui_MainWindow

    #widget = MyWidget()
    #widget.resize(800, 600)
    #widget.show()

    #sys.exit(app.exec())        

#    sys.exit(0)

gModel: CardfileModel
