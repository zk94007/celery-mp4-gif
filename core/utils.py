import os


def is_file_locked(filepath, logger):
    """
    Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            logger.info("Trying to open %s." % filepath)
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                logger.info("%s is not locked." % filepath)
                locked = False
        except IOError as message:
            logger.warning("File is locked (unable to open in append mode). %s." % message)
            locked = True
        finally:
            if file_object:
                file_object.close()
                logger.info("%s closed." % filepath)
    else:
        logger.warning("%s not found." % filepath)
    return locked


def seconds_to_ms_tuple(duration):
    """
    Convert a float duration into a (minute, seconds) tuple
    :param duration: A float
    :return: A tuple formed as (minute, seconds)
    """
    minute = duration // 60
    seconds = duration - minute * 60
    return int(minute), seconds

