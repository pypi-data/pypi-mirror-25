import os

import aiofiles
import ruamel.yaml


class Config(dict):
    def __init__(self, default_dict: dict=None, **defaults):
        super(Config, self).__init__(default_dict or {}, **defaults)

    async def from_file(self, path: str):
        """
        Read the config data from the config YAML and parse it with
         the available loader. The parsed dict is then used to update
         the config object.
        :param path: Path to file that should be loaded
        :return:
        """
        async with aiofiles.open(path, "r") as in_file:
            stream = await in_file.read()
            config = ruamel.yaml.load(stream, preserve_quotes=True,
                                      Loader=ruamel.yaml.Loader)

            if isinstance(config, dict):
                self.update(**config)

    async def from_env_vars(self, prefix: str="JOSEPH_"):
        """
        Load upper case environment variables as config values.
        Note: The prefix is removed from the environment variable before
         it's stored on the config object.

        :param prefix: Only variables starting with this values are parsed
            as config values
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                key = key.replace(prefix, '')
                self[key] = value

    async def to_file(self, path: str):
        """
        Write the current config object to a file

        :param path: File of the path to write the values to
        """
        yaml_string = ruamel.yaml.dump(self.copy(), default_flow_style=False)
        async with aiofiles.open(path, "w+") as out_file:
            await out_file.write(yaml_string)
