from dataclasses import dataclass
from typing import Any
from scripts.game.components.tag_handler import TagHandler
from os import path as os_path, makedirs
from json import dump as json_dump, load as json_load
from scripts.utility.logger import Logger
from scripts.utility.basic import get_filename


class PersistentData:
    __ITEM_DOES_NOT_EXIST = "Item '{item_name}' does not exist in Persistent Data '{name}'. Adding new entry '{item_name}': {{'{value_name}': {default_value}}}"
    __VALUE_DOES_NOT_EXIST = "Value '{value_name}' in Item '{item_name}' does not exist in Persistent Data '{name}'. Adding new entry '{value_name}': {default_value}"

    def __init__(self, name: str, filepath: str, data: dict, tags: TagHandler):
        self.name = name
        self.filepath = filepath
        self.data = data
        self.tags = tags

    def get_data(self, item_name: str, value_name: str, default_value: Any = None):
        if not Logger.raise_key_error(self.data, item_name, PersistentData.__ITEM_DOES_NOT_EXIST.format(item_name=item_name, name=self.name, value_name=value_name, default_value=default_value), raise_exception=False):
            if not Logger.raise_key_error(self.data[item_name], value_name, PersistentData.__VALUE_DOES_NOT_EXIST.format(value_name=value_name, item_name=item_name, name=self.name, default_value=default_value), raise_exception=False):
                return self.data[item_name][value_name]

            self.data[item_name][value_name] = default_value
            return default_value

        self.data[item_name] = {value_name: default_value}
        return default_value


class PersistentDataService:

    __FILE_DOES_NOT_EXIST = ("File '{filepath}' does not exist. Created new file '{filepath}' with the following "
                             "default contents: {dict_data}")
    __FILE_LOADED = "File '{filepath}' loaded."
    __FILE_SAVED = "File '{filepath}' saved with the following contents: {dict_data}."
    __DATA_ADDED = "Data {data} added to persistent data."
    __SAVING_DATA = "Saving all data. Tags required: {tags}"

    CONFIG_DIR = "configs"

    def __init__(self):
        self.__data: dict[str, PersistentData] = {}

    @staticmethod
    def __load_data(filepath: str, default_data: dict | None = None) -> dict:
        if os_path.exists(filepath):

            with open(filepath, "r") as f:
                file_data = json_load(f)

            Logger.log_info(PersistentDataService.__FILE_LOADED.format(filepath=filepath))

        else:
            if default_data is None:
                file_data = {}
            else:
                file_data = default_data

            if os_path.dirname(filepath):
                makedirs(os_path.dirname(filepath), exist_ok=True)

            with open(filepath, "w") as f:
                json_dump(file_data, f)

            Logger.log_warning(
                PersistentDataService.__FILE_DOES_NOT_EXIST.format(filepath=filepath, dict_data=default_data))

        return file_data

    @staticmethod
    def __save_data(filepath: str, data: dict) -> bool:

        if os_path.dirname(filepath):
            makedirs(os_path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as f:
            json_dump(data, f)

        Logger.log_info(PersistentDataService.__FILE_SAVED.format(filepath=filepath, dict_data=data))

        return True


    def add(self, filepath: str, name: str = None, data: dict | None = None) -> PersistentData | None:

        if name is None:
            name = get_filename(filepath, include_extension=False)

        if data is None:
            data = {}

        new_persistent_data = PersistentData(name = name, filepath = filepath, data = data, tags = TagHandler())

        if name in self.__data:
            Logger.log_warning(Logger.OVERWRITTEN.format(
                data_type = "PersistentData",
                name = name,
                pre_data = self.__data[name],
                post_data = new_persistent_data
            ))

        self.__data[name] = new_persistent_data

        Logger.log_info(PersistentDataService.__DATA_ADDED.format(data = self.__data[name]))

        return self.__data[name]


    def get(self, name: str) -> PersistentData | None:

        if not Logger.raise_key_error(self.__data, name, raise_exception=False):
            return self.__data[name]

        return None


    def save(self, name: str, new_data: dict | None = None) -> bool:

        if Logger.raise_key_error(self.__data, name, raise_exception=False):
            return False

        if type(new_data) is dict:
            self.__data[name].data = new_data

            Logger.log_info(Logger.OVERWRITTEN.format(
                data_type="PersistentData",
                name=name,
                pre_data=self.__data[name].data,
                post_data=new_data
            ))

        return self.__save_data(filepath = self.__data[name].filepath, data = self.__data[name].data)


    def __is_data_tagged(self, name, *tags: str) -> bool:

        if len(tags) > 0:
            for tag_name in tags:
                if self.__data[name].tags.is_tag_assigned(tag_name):
                    return True
        else:
            return True

        return False


    def save_all(self, *tags: str):
        Logger.log_info(PersistentDataService.__SAVING_DATA.format(tags=tags))

        successful = True

        for i in self.__data.keys():
            if self.__is_data_tagged(i, *tags):
                if not self.save(i):
                    successful = False

        return successful


    def load(self, name: str) -> PersistentData | None:
        if Logger.raise_key_error(self.__data, name, raise_exception=False):
            return None

        loaded_data = self.__load_data(filepath = self.__data[name].filepath)

        if type(loaded_data) is dict:
            self.__data[name].data = loaded_data

            return self.__data[name]

        return None


    def load_all(self, *tags: str) -> bool:
        successful = True

        for i in self.__data.keys():

            if self.__is_data_tagged(i, *tags):
                loaded_data = self.load(i)
                if loaded_data is None or loaded_data.data is None:
                    successful = False

        return successful
