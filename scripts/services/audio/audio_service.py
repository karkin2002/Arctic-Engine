__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""


from pygame import mixer
from scripts.utility.logger import Logger
from scripts.utility.basic import get_filename


MAX_NO_CHANNELS = "Max no of channels reached: '{no_channels}'"
NEW_CHANNEL_ADDED = "Added new channel. No of channels: '{no_channels}'"


## Sets volume of audio class
def set_audio_volume(audio, value):
    audio.set_volume(value/100)        


## Sets num of audio channels
def set_num_channels(value: int):

    """Sets number of audio channels (how many sounds you can play at once).
    """

    mixer.set_num_channels(value)

## Gets the num of audio channels
def get_num_channels() -> int:

    """Returns num of audio channels.

    Returns:
        int: num of audio channels
    """

    return mixer.get_num_channels()

## Adds a new channel
def add_channel():

    """Adds a new audio channel.
    """

    set_num_channels(get_num_channels() + 1)

## finds an empty channel, creates new if no empty
def find_channel(max_channels: int) -> mixer.Channel | None:

    """Finds a channel with no audio playing, otherwise creates a new one,
    otherwise return None.

    Returns:
        Channel: empty channel
    """

    audio_channel = mixer.find_channel()
    
    if audio_channel is not None:
        return audio_channel
    
    else:
        if get_num_channels() < max_channels:
            add_channel()
            Logger.log_info(
                NEW_CHANNEL_ADDED.format(no_channels=get_num_channels()))
            return mixer.Channel(get_num_channels() - 1)

        else:
            Logger.log_warning(
                MAX_NO_CHANNELS.format(no_channels=max_channels))




## Audio
class Audio:

    """Class for individual audio
    """

    def __init__(self, name: str, path: str, volume: float = 50):
        self.__volume = None
        self.get_name = None
        self.__name = name
        self.set_volume(volume)

        self.audio = mixer.Sound(path) 

    def get_name(self):
        return self.__name

    def get_volume(self):
        return self.__volume

    def set_volume(self, value):
        self.__volume = value

    def get_audio(self):
        return self.audio

    def play(self, max_channels, loops = 0):
        channel = find_channel(max_channels)
        if channel is not None:
            channel.play(self.audio, loops)




## Audio Category
class AudioCategory:
    AUDIO_ERROR = "The audio '{audio_name}' doesn't exist."
    AUDIO_ADD = "Audio '{audio_name}' added as '{audio}'"
    
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume
        self.mute = False

        self.audio_dict: dict[str, Audio] = {}
    

    ## Returns the name of the audio category
    def get_name(self) -> str:

        """Returns the name of the audio category.

        Returns:
            str: audio category name
        """

        return self.name
    
    ## Returns the volume of an audio
    def get_volume(self) -> float:

        """Returns volume of the audio category

        Returns:
            float: volume
        """

        return self.volume
    
    ## checks if an audio is in the audio_dict
    def is_audio(self, name: str) -> bool:
        """Checks if an audio exists in the audio dict

        Returns:
            bool: True if audio exists, False otherwise
        """
        
        if not Logger.raise_key_error(self.audio_dict, 
                                      name, 
                                      self.AUDIO_ERROR.format(
                                          audio_name = name)):
            return True
        
        return False
    

    ## returns an audio class
    def __get_audio(self, name: str) -> Audio:

        """Returns audio from audio dict

        Returns:
            Audio: audio
        """

        return self.audio_dict[name]

    # Sets the volume of the category
    def set_cat_volume(self, overall_volume: float, value: float):

        """Sets the category volume
        """
        self.volume = value
        for each_audio in self.audio_dict:
            self.set_audio_volume(each_audio, overall_volume, value)

    ## Sets the volume of an audio
    def set_audio_volume(self, name: str, overall_volume: float, value: float = None):
        
        """Sets the volume of an audio
        """
        
        if self.is_audio(name):
            audio = self.__get_audio(name)
            if value is not None:
                audio.set_volume(value)

                # (overall*(category/100))*(audio/100)
                volume_value = (overall_volume * (self.volume/100)) * (audio.get_volume() / 100)
                set_audio_volume(audio.get_audio(), volume_value)

    ## Returns the volume of an audio
    def get_audio_volume(self, name: str) -> int:
        """Returns the volume of an audio

        Returns:
            int: volume
        """        
        
        return self.__get_audio(name).get_volume()


    ## Adds audio to the audio_dict and sets its volume, doesn't play the audio
    def add_audio(self, name: str, path: str, overall_volume: float, volume: float = 50):

        """Adds audio to audio dict, sets its volume (doesn't play the audio)
        """

        if name is None:
            name = get_filename(path, False)
        self.audio_dict[name] = Audio(name, path, volume)
        self.set_audio_volume(name, overall_volume, volume)
        
        Logger.log_info(self.AUDIO_ADD.format(
            audio_name = name, 
            audio=self.audio_dict[name]))

    ## Plays audio
    def play_audio(self, name: str, max_channels: int, loops: int = 0):

        """Plays audio
        """

        self.__get_audio(name).play(max_channels, loops)

    ## Finds which channel an audio is playing in
    def __find_channel_by_audio(self, name: str) -> int | None:

        """Returns a channel which an audio is playing in

        Returns:
            Channel: channel with audio playing
        """
        
        audio = self.__get_audio(name).audio
        for eachChannel in range(get_num_channels()):
            if mixer.Channel(eachChannel).get_sound() == audio:
                return eachChannel

    ## Pauses an audio
    def pause_audio(self, name: str):
        """Pauses an audio
        """

        mixer.Channel(self.__find_channel_by_audio(name)).pause()

    ## Unpauses an audio
    def unpause_audio(self, name: str):
        """Unpauses an audio
        """

        mixer.Channel(self.__find_channel_by_audio(name)).unpause()

    ## Queues an audio after another audio on a channel
    def queue_audio(self, audio_name: str, audio_queue_name: str):
        """Queues an audio after another audio on a specific channel
        """

        if self.is_audio(audio_name) and self.is_audio(audio_queue_name):
            channel = self.__find_channel_by_audio(audio_name)
            mixer.Channel(channel).queue(self.__get_audio(audio_queue_name).get_audio())





## Class used for all audio on the UI
class AudioService:
    """Handles all UI audio
    """
    
    CAT_ERROR = "Audio category '{cat_name}' doesn't exist"
    CAT_ADD = "Audio category '{cat_name}' created."
    CAT_EXISTS = "Audio category '{cat_name}' already exists."

    def __init__(self, 
            volume: float, 
            max_channels: int = 16, 
            frequency: int = 44100, 
            size: int = -16, 
            channels: int = 2, 
            buffer: int = 512, 
            device_name: str = None):
        
        self.volume = volume

        self.cat_dict = {}

        mixer.pre_init(frequency, size, channels, buffer, device_name) # Initialising the mixer
        mixer.init()

        self.max_channels = max_channels

        if max_channels < get_num_channels():
            set_num_channels(max_channels)

    ## Sets the overall volume for the application
    def set_volume(self, value: int):
        """Sets the overall volume for the application
        """        

        if self.volume != value:
            self.volume = value

            for cat_name in self.cat_dict:
                self.set_cat_volume(cat_name, self.get_cat_volume(cat_name))

    ## Returns the overall volume for the application
    def get_volume(self):
        """Returns the overall volume for the application

        Returns:
            float: volume
        """

        return self.volume 
        
    ## Returns whether the category exists
    def __is_cat(self, cat_name: str):
        
        if not Logger.raise_key_error(self.cat_dict, 
                                      cat_name,
                                      self.CAT_ERROR.format(cat_name = cat_name)):
            return True
        
        return False

    ## Returns the audio cat object
    def __get_audio_cat(self, cat_name) -> AudioCategory | None:
        if self.__is_cat(cat_name):
            return self.cat_dict[cat_name]

    ## Adds a new Audio Cat to a dict
    def add_cat(self, cat_name: str, volume: float = 50):

        """Adds a new category
        """

        if not cat_name in self.cat_dict:
            self.cat_dict[cat_name] = AudioCategory(cat_name, volume)
            Logger.log_info(self.CAT_ADD.format(cat_name = cat_name))

        else:
            Logger.log_info(self.CAT_EXISTS.format(cat_name = cat_name))

    ## Adds an audio to an audioCat
    def add_audio(self, cat_name: str, path: str, audio_name: str = None, volume: float = 50):

        """Adds a new audio to a category
        """

        self.__get_audio_cat(cat_name).add_audio(audio_name, path, self.volume, volume)
    
    ## Sets the volume of the audioCat
    def set_cat_volume(self, cat_name: str, value: float):

        """Sets the category volume
        """

        self.__get_audio_cat(cat_name).set_cat_volume(self.volume, value)


    ## Returns the volume of the category
    def get_cat_volume(self, cat_name: str) -> float:
        """Returns a categories volume

        Returns:
            int: volume
        """

        return self.__get_audio_cat(cat_name).get_volume()

    ## Sets the audio in the audioCat
    def set_audio_volume(self, cat_name: str, audio_name: str, value: float):

        """Sets an audio's volume
        """

        self.__get_audio_cat(cat_name).set_audio_volume(audio_name, self.volume, value)

    ## Returns the volume of the category
    def get_audio_volume(self, cat_name: str, audio_name: str) -> int:
        """Returns an audios volume

        Returns:
            int: volume
        """

        return self.__get_audio_cat(cat_name).get_audio_volume(audio_name)

    ## Plays an audio
    def play(self, cat_name: str, audio_name: str, loops: int = 0):

        """Plays an audio
        """

        if self.__get_audio_cat(cat_name).is_audio(audio_name):
            self.__get_audio_cat(cat_name).play_audio(audio_name, self.max_channels, loops)
            #Logger.log_info(f"Playing '{audio_name}' from '{cat_name}' with {loops} loops.")

    ## Pauses the audio
    def pause(self, cat_name: str, audio_name: str):

        """Pauses an audio
        """

        if self.__get_audio_cat(cat_name).is_audio(audio_name):
            self.__get_audio_cat(cat_name).pause_audio(audio_name)

    ## Unpauses the audio
    def unpause(self, cat_name: str, audio_name: str):

        """Unpauses an audio
        """

        if self.__get_audio_cat(cat_name).is_audio(audio_name):
            self.__get_audio_cat(cat_name).unpause_audio(audio_name)

    ## Queue an audio
    def queue(self, cat_name: str, audio_name: str, audio_queue_name: str):

        """Queues an audio
        """

        self.__get_audio_cat(cat_name).queue_audio(audio_name, audio_queue_name)