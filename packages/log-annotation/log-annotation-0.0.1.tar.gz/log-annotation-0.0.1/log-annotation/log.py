def log(job_type='info'):
    import time
    def log_decorator(function):
        def log_work():

            try:
                start = time.time()
                log_info = function()

                end = time.time()

                # elapsed time for above function in seconds
                elapsed_time = str(round(end - start,2))
                print(function.__name__ + ' ' + elapsed_time + 's')
            except Exception as e:
                print('Error in ' + function.__name__ + ' :'  + str(e))

            return log_info #returning what the decorated function returns
        return log_work
    return log_decorator #returning the decorator function