import asyncio
import logging
import logging.handlers
import os
import signal
import sys
from typing import Iterable

from .config import Config
from .constants import CONFIG_FILE, LOG_ROOT, GENERAL_ERROR_CODE, \
    MANUAL_EXIT_ERROR_CODE, MANUAL_RESTART_ERROR_CODE, CLEAN_EXIT_ERROR_CODE, \
    ENTITIES_ROOT, CONFIG_ROOT
from .events import EventBus, Namespace, MiddlewareEvent, listen, AFTER_EVENT
from .events.events import Event
from .exceptions import StopException, RestartException
from .plugins.manager import Manager as Plugins, _LOGGER as _PLUGIN_LOGGER
from .states.entities import Entity, Room
from .states.manager import Manager as States
from .rules.engine import Engine
from .web.web import Web

JOSEPH_NAMESPACE = Namespace("joseph", Event)
FIRST_RUN_EVENT = JOSEPH_NAMESPACE.create_event("first_run")

# Fired right after the core components have been set up, but before the non
#  essential stuff is done (Plugins etc.)
STARTING_EVENT = JOSEPH_NAMESPACE.create_event("starting")
# Fired after the entire application has been started. (Fired right before
#  the ``run_forever`` method is called
STARTED_EVENT = JOSEPH_NAMESPACE.create_event("started")
# Fired when the application is about to shutdown
STOPPING_EVENT = JOSEPH_NAMESPACE.create_event("stopping", exit_code=0)

_LOGGER = logging.getLogger(__name__)


@listen(FIRST_RUN_EVENT)
async def ensure_config(event: Event):
    """
    Dump the application default config to a file, if no config file exists
    :param event: The event instance
    """
    if not os.path.isfile(CONFIG_FILE):
        _LOGGER.warning(f"No config file nor default config found. Using "
                        f"application defaults")

        await event.joseph.config.to_file(CONFIG_FILE)


@listen(FIRST_RUN_EVENT)
async def ensure_directories(event: Event):
    """
    Make sure all required directory exist and are accessible by the
     application. If a directory does not exist yet, it will be created
    """
    config: Config = event.app.config
    for directory in config.get("DIRECTORIES", {}).values():
        if not os.path.isdir(directory):
            _LOGGER.debug(
                f"Cannot find {directory} so attempting to create it")
            os.makedirs(directory)


@listen(STARTED_EVENT)
async def load_entities(event: Event):
    """
    Load the entities that have been written to a file, either by the
     user or by Joseph into memory after the application has started
    """
    await event.joseph.states.from_dir()


@listen(STARTED_EVENT)
async def load_periodic_rules(event: Event):
    """ Load the periodic rules into memory and start them. """
    await event.joseph.rules.parse_periodic_rules(event=event)


@listen(STARTED_EVENT)
async def start_http_server(event: Event):
    await event.joseph.http.start_server()


@listen(STOPPING_EVENT)
async def stop_http_server(event: Event):
    await event.joseph.http.stop_server()


@listen(STOPPING_EVENT)
async def exit_code(event: Event):
    """
    Set the exit code based on the exception that triggered the stopping
     exception
    :param event: The triggered event instance
    :return: The handled event. (Note: the instance is returned for easier
     testing and does not affect the actual
        program)
    """
    if event.exception is not None:
        if isinstance(event.exception, KeyboardInterrupt) and not isinstance(
                event.exception, RestartException):
            event.exit_code = MANUAL_EXIT_ERROR_CODE
        elif isinstance(event.exception, RestartException):
            event.exit_code = MANUAL_RESTART_ERROR_CODE
        else:
            event.exit_code = GENERAL_ERROR_CODE
    else:
        event.exit_code = CLEAN_EXIT_ERROR_CODE

    return event


@listen(STOPPING_EVENT)
async def save_states(event: Event):
    """
    Save the state of the entities (registered) on the manager to a
     file. This should always be called when the application shuts
     down to make sure the last known states of the entities can
     loaded upon next boot.
    """
    await event.joseph.states.save_states()


@listen(AFTER_EVENT)
async def trigger_rules(event: MiddlewareEvent):
    """
    Makes sure the rules are evaluated after the "regular" event handlers
     have had their chance to update the event to it's final state.
    :param event: The middleware event
    """
    joseph = event.joseph
    if isinstance(joseph, Joseph):
        context = event.original_event.context.copy()
        context['event'] = event.original_event
        await joseph.rules.parse_rules(**context)


class Joseph(object):
    __slots__ = ("loop", "config", "events", "rules", "plugins", "states",
                 "http")

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.config = Config({
            'DEBUG': False,
            'DIRECTORIES': {
                'CONFIG_ROOT': CONFIG_ROOT,
                'ENTITIES': ENTITIES_ROOT,
                'LOGS': LOG_ROOT,
            },
            'LOGGING': {
                'LEVEL': "INFO",
                'ROTATE_DAYS': 5,
                'ROLLOVER': "midnight"
            },
            'CONFIG': {
                'PATH': CONFIG_FILE,
                'ENV_PREFIX': "JOSEPH_"
            },
            'TEMPLATES': {
                'BLOCK_START_STRING': "{%",
                'BLOCK_END_STRING': "%}",
                'VARIABLE_START_STRING': "<{",
                'VARIABLE_END_STRING': "}>",
                'COMMENT_START_STRING': "{#",
                'COMMENT_END_STRING': "#}",
            }
        })
        self.loop = loop or asyncio.get_event_loop()
        self.events = EventBus(loop=self.loop)
        self.events.joseph = self
        self.plugins = Plugins(loop=self.loop)
        self.states = States()
        self.states.types = self.plugins.get_by_entry_point("entities").copy()
        self.http = Web(self, self.config.get("http", {}), loop=self.loop)

        jinja2_config = {key.lower(): value
                         for key, value
                         in self.config.get("TEMPLATES").items()}

        # Create the action context from plugin entry points and core
        #  functions that might be used in a rule.
        action_context = self.plugins.get_by_entry_point("actions")
        action_context.update(
            fire=self.events.fire,
            log_info=_PLUGIN_LOGGER.info,
        )
        self.rules = Engine(action_context,
                            self._template_context,
                            jinja_env_config=jinja2_config)

    def setup_logging(self):
        log_config = self.config['LOGGING']

        # Get the log level from the config or default to info level
        log_level = logging._nameToLevel[log_config.get("LOG_LEVEL", "INFO")]
        logging.basicConfig(level=log_level)
        # Remove the default handlers handlers so we can replace t
        #  hem with our own
        for handler in logging.root.handlers:
            logging.root.removeHandler(handler)

        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        # Setup rotating file handler
        log_file_name = os.path.join(LOG_ROOT, "joseph.log")
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_file_name,
            when=log_config['ROLLOVER'],
            backupCount=log_config['ROTATE_DAYS'])
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)

        # Setup console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logging.root.addHandler(console_handler)

    async def register_signal_handlers(self):
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

    def start(self):
        self.setup_logging()
        _LOGGER.info("===== [Starting Joseph ] =====")

        if self.is_first_run():
            _LOGGER.info("Joseph is started for the first time, making sure "
                         "all required files are in order")
            self.loop.run_until_complete(self.events.fire(FIRST_RUN_EVENT))
            _LOGGER.info("Finished first time run setup")

        self.loop.run_until_complete(asyncio.gather(
            self.config.from_file(
                self.config.get("CONFIG", {}).get("PATH", CONFIG_FILE)),
            self.config.from_env_vars(
                self.config.get("CONFIG", {}).get("ENV_PREFIX", None))
        ))

        # Load non essential modules
        self.loop.run_until_complete(asyncio.gather(
            self.events.fire(STARTING_EVENT),
            self.states.register_entity_types([
                ("default", Entity),
                ("room", Room)
            ]),
            self.http.prepare_server(),
            self.rules.parse_periodic_rules(),
        ))

        _LOGGER.info("Finished starting all of Joseph's components")
        self.loop.run_until_complete(self.events.fire(STARTED_EVENT))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def required_dirs(self) -> Iterable[str]:
        for directory in self.config.get("DIRECTORIES", {}).values():
            yield directory

    def required_files(self) -> Iterable[str]:
        return (CONFIG_FILE,)

    def is_first_run(self) -> bool:
        """
        :return: ``True`` if all required directories and files exist,
         ``False`` other wise
        """
        return not (all(os.path.isdir(path)
                        for path in self.required_dirs()) and
                    all(os.path.isfile(path)
                        for path in self.required_files()))

    def stop(self, exception: BaseException = None):
        if exception:
            _LOGGER.exception(f"Fatal exception '{exception}' caused the "
                              f"application to quit")
        else:
            _LOGGER.info("Received stopping signal, cleanly exiting "
                         "application")

        self.loop.run_until_complete(
            self.events.fire(STOPPING_EVENT, exception=exception))
        self.loop.stop()

        _LOGGER.info("Bye bye")
        return STOPPING_EVENT.exit_code

    @staticmethod
    def stop_soon():
        raise StopException()

    @staticmethod
    def restart_soon():
        raise RestartException()

    @property
    def _template_context(self):
        return {
            'config': self.config
        }
