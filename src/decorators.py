def execute_if(boolean: bool):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if boolean:
                func(*args, **kwargs)
            
        return wrapper
        
    return decorator