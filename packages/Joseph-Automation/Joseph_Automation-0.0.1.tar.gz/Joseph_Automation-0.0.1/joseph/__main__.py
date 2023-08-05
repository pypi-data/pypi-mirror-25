import sys

from joseph.core import Joseph


def setup_uvloop():
    """ Attempt to set Asyncio's event loop policy to UVLoop """
    import asyncio

    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass


def main():
    setup_uvloop()

    joseph = Joseph()
    exception = None
    
    try:
        joseph.start()
    except Exception as e:
        exception = e
    finally:
        exit_code = joseph.stop(exception)

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
