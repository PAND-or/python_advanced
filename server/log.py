import inspect

def log(func):
    def wrap(request, *args, **kwargs):
        print('*' * 50)

        print(func)
        print(request)
        #print(inspect.function(request))
        print('*' * 50)
        return func(request, *args, **kwargs)
    return wrap
