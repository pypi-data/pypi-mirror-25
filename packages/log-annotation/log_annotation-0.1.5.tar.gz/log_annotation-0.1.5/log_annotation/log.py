import logging
import graypy
import requests
def log(name='', level=logging.INFO, **graylog):
    import time
    import logging
    def decorator(function):
        def wrapper(*args, **kwds):
            log = dict()
            error = dict()
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
                log = {"function":function.__name__,"result":res}
                return res
            except requests.exceptions.HTTPError as err:
                error = {"error": {"description": str(err), "response": err.response.json()}}
            except Exception as err:
                error = {"error": {"description": str(err)}}
            finally:
                log = {"function":function.__name__, "elapsed_time": str(round(time.time() - start_time,2))}
                if not error:
                    logger.info(log)
                else:
                    log.update(error)
                    logger.error(log)
                    return error
        return wrapper
    return decorator
