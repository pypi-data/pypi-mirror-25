import logging
import graypy
import requests
def log(name='', level=logging.INFO, **graylog):
    import time
    import logging
    def decorator(function):
        def wrapper():
            try:
                # Init logger
                logger = logging.getLogger(name)
                logger.setLevel(level)
                # Log Init
                print(graylog)
                print(graylog.get("host",None))
                if (graylog.get("host",None) != None and graylog.get("port",None) != None):
                    handler = graypy.GELFHandler(graylog["host"], graylog["port"])
                    logger.addHandler(handler)
                else:
                    logger.addHandler(logging.StreamHandler())
                start_time = time.time()
                res = function()
                elapsed_time = str(round(time.time() - start_time,2))
                logger.info({"function":function.__name__, "elapsed_time":elapsed_time})
                return res
            except requests.exceptions.HTTPError as err:
                logger.error({'error': {'description': str(err), 'response': err.response.json()}})
            except Exception as e:
                print('Error in ' + function.__name__ + ' :'  + str(e))
        return wrapper
    return decorator #returning the decorator function
