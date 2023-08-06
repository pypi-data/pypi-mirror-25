import os
import xldeploy
from xld.xld_args_validator import XldArgsValidator


class XldCommands:

    def __init__(self, url=None, username=None, password=None):
        self.__url = self.__get_arg_value(url, XldArgsValidator.XL_DEPLOY_URL)
        self.__username = self.__get_arg_value(username, XldArgsValidator.XL_DEPLOY_USERNAME)
        self.__password = self.__get_arg_value(password, XldArgsValidator.XL_DEPLOY_PASSWORD)

        XldArgsValidator().validate(self.__url, self.__username, self.__password)

        config = xldeploy.Config.initialize(url=self.__url + '/deployit',
                                            username=self.__username,
                                            password=self.__password)
        self.__client = xldeploy.Client(config)

    def __get_arg_value(self, param_value, env_variable):
        return os.environ.get(env_variable, None) if param_value is None else param_value

    def apply(self, path):
        return self.__client.deployfile.apply(open(path, 'r').read())

    def generate(self, *directories):
        return self.__client.deployfile.generate(list(directories))
