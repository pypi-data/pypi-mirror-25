import logging
import graypy
import requests
def log(name='', level=logging.INFO, **graylog):
    import time
    import logging
    def decorator(function):
        def wrapper(*args, **kwds):
            res = dict()
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
                res = {"function":function.__name__,"result":res}
            except requests.exceptions.HTTPError as err:
                res = {'function':function.__name__, 'error': {'description': str(err), 'response': err.response.json()}}
            except Exception as err:
                res = {'function':function.__name__, 'error': {'description': str(err)}}
            finally:
                res["elapsed_time"] = str(round(time.time() - start_time,2))
                if res.get('error',None) == None:
                    logger.info(res)
                else:
                    logger.error(res)
        return wrapper
    return decorator
