import logging

# FileName=colorlogs.py
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': YELLOW,
        'INFO': GREEN,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }

    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        name = record.name
        filename = record.filename
        lineno = record.lineno
        funcName = record.funcName
        if self.use_color and levelname in self.COLORS:
            level_name_color = COLOR_SEQ % (30 + self.COLORS[levelname]) + "-" + levelname + "-" + RESET_SEQ
            record.levelname = level_name_color
            name_color = COLOR_SEQ % (30 + self.COLORS[levelname]) + name + RESET_SEQ
            record.name = name_color
            filename_color = COLOR_SEQ % (30 + self.COLORS[levelname]) + filename + RESET_SEQ
            record.filename = filename_color
            lineno_color = COLOR_SEQ % (30 + self.COLORS[levelname]) + str(lineno) + RESET_SEQ
            record.lineno = lineno_color
            funcName_color = COLOR_SEQ % (30 + self.COLORS[levelname]) + funcName + RESET_SEQ
            record.funcName = funcName_color
        return logging.Formatter.format(self, record)


class colorlogs(logging.Logger):

    def __init__(self, name):
        FORMAT = "%(asctime)s  $BOLD%(name)  s$RESET   %(funcName)s $BOLD%(filename)s$RESET:%(lineno)s %(levelname)s \n%(message)s "
        COLOR_FORMAT = self.formatter_message(FORMAT, True)
        logging.Logger.__init__(self, name, logging.DEBUG)
        color_formatter = ColoredFormatter(COLOR_FORMAT)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(color_formatter)
        self.addHandler(console)
        return

    def formatter_message(self, message, use_color=True):
        if use_color:
            message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
        else:
            message = message.replace("$RESET", "").replace("$BOLD", "")
        return message


# 用法
logging.setLoggerClass(colorlogs)
rrclogger = logging.getLogger("rrcheck")
rrclogger.setLevel(logging.DEBUG)


def test():
    rrclogger.debug("DEBUG message")
    rrclogger.info("INFO message")


test()
