class Platform(object):
    WINDOWS, LINUX, MAC = range(3)

    @staticmethod
    def contain(_platform):
        if _platform == Platform.WINDOWS or _platform == Platform.LINUX or _platform == Platform.MAC:
            return True
        else:
            return False


class Step(object):
    NEW, INIT, STATS, NORMALIZE, VARSELECT, TRAIN, POSTTRAIN, EVAL = range(8)


class CommandRunningStatus(object):
    SUCCESS, FAILED = range(2)
