/*
e:
cd \data
rem or c:
rem cd /users/mstas/appdata/roaming/mjstasak/notecard/notecard.db
sqlite3 notecard.db

Note: ';' statement terminator is needed for sqlite.exe
Note: SQLite does not enforce text column widths; VARCHAR(n) is an alias for TEXT
*/

CREATE TABLE notecard (
  notecard_id INTEGER PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  body VARCHAR(65535)
);

CREATE TABLE category (
  category_id INTEGER PRIMARY KEY,
  category VARCHAR(160) NOT NULL,
  description VARCHAR(65535)
);

CREATE TABLE notecard_category (
  notecard_category_id INTEGER PRIMARY KEY,
  notecard_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  FOREIGN KEY(notecard_id) REFERENCES notecard(notecard_id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
);

/* .schema */
/* .quit */
