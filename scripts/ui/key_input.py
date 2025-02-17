from scripts.utility.logger import Logger
from scripts.utility.basic import load_json_file
import pygame

class KeyInput:
    KEYBIND_JSON_PATH = r"config/ui/keybind.json"
    
    KEYBIND_NOT_EXIST_TEXT = "Custom keybind name does not exist."
    KEYCODE_NOT_EXIST_TEXT = "Keycode does not exist."
    
    def __init__(self):
        self.__keybind_dict: dict[str, str] = load_json_file(KeyInput.KEYBIND_JSON_PATH)
        
        self.__current_inputs = pygame.key.get_pressed()
        self.__past_input = self.__current_inputs
        
        
    def __get_key_code(self, keybind_name: str) -> int:
        
        if not Logger.raise_key_error(self.__keybind_dict,
                                      keybind_name,
                                      KeyInput.KEYBIND_NOT_EXIST_TEXT,
                                      False):
                
            return pygame.key.key_code(self.__keybind_dict[keybind_name])
        
        else:
            return -1
        
        
    def set_current_inputs(self):
        self.__past_input = self.__current_inputs
        self.__current_inputs = pygame.key.get_pressed()
        
        
    def is_pressed(self, keybind_name: str, hold = False) -> bool:
        
        keycode = self.__get_key_code(keybind_name)
        
        if not Logger.raise_index_error(self.__current_inputs,
                                      keycode,
                                      KeyInput.KEYCODE_NOT_EXIST_TEXT,
                                      False):
            
            if hold:
                return self.__current_inputs[self.__get_key_code(keybind_name)]
            
            else:
                return (self.__current_inputs[self.__get_key_code(keybind_name)] and
                        not self.__past_input[self.__get_key_code(keybind_name)])
        
        return False
            
        
        