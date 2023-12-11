import logging
from datetime import datetime

class Logger:
    """Class used for logging script info. Includes methods for raising 
    exceptions.
    """    
    
    ## Log file output variables.
    LOG_OUT_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    DATE_TIME_OUT_FORMAT = '%m/%d/%Y %H:%M:%S'
    START_TEXT = "Log started as '{filename}'."
    
    ##Exception Error Msgs
    ATTRIBUTE_ERROR = "'{value}' is of type {value_type}. Expected {expected_type}."
    
    
    def __init__(self, 
                 filename: str, 
                 level: int = logging.INFO):
        """Sets up logger file & adds a log stating the log has started.

        Args:
            filename (str): filename of the log file.
            level (int, optional): Level of logs recorded. Defaults to 
            logging.INFO.
        """         
        
        log_start_time = datetime.now().strftime('%m%d%y_%H%M%S')

        log_filename = f"{filename}_{log_start_time}.log"
        
        logging.basicConfig(
            filename = log_filename, 
            format = self.LOG_OUT_FORMAT,
            datefmt = self.DATE_TIME_OUT_FORMAT,
            level = level)
        
        logging.info(self.START_TEXT.format(filename = log_filename))
        
        
    def raise_attribute_error(value, expected_type):
        """_summary_

        Args:
            value (Any): Value that exceptions being raised for.
            expected_type (Any): Expected type for the value.

        Raises:
            AttributeError: For the value being the incorrect type.
        """        
        
        error_msg = Logger.ATTRIBUTE_ERROR.format(
            value = value, 
            value_type = type(value),
            expected_type = expected_type)
        
        logging.critical(error_msg)
        
        raise AttributeError(error_msg)
            