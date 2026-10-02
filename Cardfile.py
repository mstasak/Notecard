import application
import sys
import logging
#import logging.handlers

def main():
    logger = logging.getLogger("notecard")
    logger.setLevel(logging.INFO)
    #hndlr = logging.handlers.RotatingFileHandler(filename="notecard.log", maxBytes=1000000)
    #hndlr.setFormatter(logging.Formatter(fmt=(
    #    "%(asctime)s | %(levelname)s | "
    #    "%(name)s | %(filename)s:%(lineno)d | "
    #    "%(message)s")))
    #while logger.hasHandlers():
    #    logger.removeHandler(logger.handlers[0])
    #logger.addHandler(hndlr)
    logging.basicConfig(filename='notecard.log', level=logging.INFO, format="%(asctime)s | %(levelname)s | "
            "%(name)s | %(filename)s:%(lineno)d | "
            "%(message)s")
    logger.info("App launched")
    #print("Hello") #shows me if I'm looking at console output
    gApp = application.CardFileApp(orgName="mstasak", orgDomain="org", appName="notecard", args=sys.argv)
    exitVal = gApp.run()
    logger.info("App terminating.")
    sys.exit(exitVal)

if __name__ == "__main__":
    main()