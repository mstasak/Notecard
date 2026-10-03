import application
import sys
import logging

def main():
    logger = logging.getLogger("notecards")
    logger.setLevel(logging.INFO)
    logging.basicConfig(filename='notecards.log', level=logging.INFO, format="%(asctime)s | %(levelname)s | "
            "%(name)s | %(filename)s:%(lineno)d | "
            "%(message)s")
    logger.info("Notecards app launched.")
    #print("Hello") #shows me if I'm looking at console output, in VS Code
    gApp = application.CardFileApp(orgName="mstasak", orgDomain="org", appName="notecards", args=sys.argv)
    exitVal = gApp.run()
    logger.info("Notecards app terminating.")
    sys.exit(exitVal)

if __name__ == "__main__":
    main()