import json

class Config():
    """
    Provide a single global access instance
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls,*args,**kwargs)
        return cls._instance
    def load(self,path:str = 'data/config.json'):
        """
        Load configuration
        """
        with open(path,'r') as f:
            self._settings = json.load(f)
        print("Configuration amounted.")
    def get(self,key,default=None):
        """
        Get a single configure value
        """
        return self._settings.get(key,default)

config_manager = Config()