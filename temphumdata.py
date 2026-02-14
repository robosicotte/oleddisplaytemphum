from datetime import datetime

class temphumdata:
    def __init__(self, readtime: datetime, temp, humidity, degrees_f=True):
        """
        __init__: Initializes an object of class temphumdata
        
        :param readtime: The current time
        :type readtime: datetime
        :param temp: The temperature
        :type temp: float
        :param humidity: The humidity
        :type humidity: float
        :param degrees_f: Whether degrees are in Fahrenheit
        :type degrees_f: bool
        """
        self.readtime=readtime
        self.temp=temp
        self.humidity=humidity
        self.degrees_f=degrees_f

    def get_temp(self):
        """
        get_temp: Gets the temperature in the default units used by the object
        
        Returns:
        Temp (Float): The temperature

        """
        return self.temp
    
    def get_temp_f(self):
        """
        get_temp_f: Gets the temperature in degrees Fahrenheit
        
        Returns: 
        Temp_f (float): The temperature in degrees Fahrenheit
        """
        if self.degrees_f:
            return self.temp
        else:
            return self.temp*1.8+32
    
    def get_temp_c(self):
        """
        get_temp_c: Gets the temperature in degrees Celsius
        
        Returns: 
        Temp_c (float): The temperature in degrees Celsius
        """
        if not self.degrees_f:
            return self.temp
        else:
            return (self.temp-32)*5/9
        
    def get_humidity(self):
        return self.humidity
    
    def get_read_time(self):
        return self.readtime