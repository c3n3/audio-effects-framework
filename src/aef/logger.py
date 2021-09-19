class Logger():
    """The logger class. Used to log any useful messages.
       Use this instead of print in ALL cases
    """

    log_location = 'PRINT'

    PRINT = "PRINT"

    NOTE = "NOTE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DANGER = "DANGER"

    level_to_log = "NOTE"

    @staticmethod
    def log(msg, severity = "NOTE"):

        if (Logger.log_location == Logger.PRINT) and (Logger.level_to_log == Logger.NOTE):
            print("AEF::", severity,': ', msg)

        elif (Logger.log_location == Logger.PRINT) and (Logger.level_to_log == Logger.WARNING) and ((severity == Logger.WARNING) or (severity == Logger.ERROR) or (severity == Logger.DANGER)):
            print("AEF::", severity, ': ', msg)

        elif (Logger.log_location == Logger.PRINT) and (Logger.level_to_log == Logger.ERROR) and ((severity == Logger.ERROR) or (severity == Logger.DANGER)):
            print("AEF::", severity, ': ', msg)

        elif (Logger.log_location == Logger.PRINT) and (Logger.level_to_log == Logger.DANGER) and (severity == Logger.DANGER):
            print("AEF::", severity, ': ', msg)

        elif Logger.log_location == Logger.PRINT:
            pass
        else: 
            Logger.log_location = open(Logger.log_location, 'w')    
            print("AEF::", severity,': ', msg, file = Logger.log_location)  
            