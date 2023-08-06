import logging
import graypy
import requests
def log(name='', level=logging.INFO, **graylog):
    import time
    import logging
    def decorator(function):
        def wrapper(*args, **kwds):
            try:
                # Init logger
                logger = logging.getLogger(name)
                logger.setLevel(level)
                # Log Init
                if (graylog.get("host",None) != None and graylog.get("port",None) != None):
                    handler = graypy.GELFHandler(graylog["host"], graylog["port"])
                    logger.addHandler(handler)
                else:
                    logger.addHandler(logging.StreamHandler())
                start_time = time.time()
                res = function(*args, **kwds)
                elapsed_time = str(round(time.time() - start_time,2))
                logger.info({"function":function.__name__, "elapsed_time":elapsed_time})
                return res
            except requests.exceptions.HTTPError as err:
                logger.error({'error': {'function':function.__name__ , 'description': str(err), 'response': err.response.json()}})
            except Exception as err:
                logger.error({'error': {'function':function.__name__ , 'description': str(err)}})
        return wrapper
    return decorator
