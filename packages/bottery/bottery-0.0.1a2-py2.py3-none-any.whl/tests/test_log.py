import logging

from bottery.log import ColoredFormatter


class StreamHandlerTest(logging.StreamHandler):
    """Raise errors to be caught by py.test instead of printing to stdout."""

    def handleError(self, record):
        _type, value, _traceback = sys.exc_info()
        raise value


def test_colored_formatter(capsys):

    formatter = ColoredFormatter()

    stream = StreamHandlerTest()
    stream.setLevel(logging.DEBUG)
    stream.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream)


    logger.info('teste :)')
    out, err = capsys.readouterr()
    print('out', out)
    print('err', err)
