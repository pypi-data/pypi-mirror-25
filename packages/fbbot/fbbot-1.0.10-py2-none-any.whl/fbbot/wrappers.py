media_types = ['image', 'gif', 'audio', 'video', 'file']


def validate_media(value):
    assert value in media_types, \
        "Wrong media type got: {}, expected: {}".format(value, media_types)
    if value == 'gif':
        return 'image'
    return False


def require_media(func):
    def wrapper(*args, **kwargs):
        print("args:{}, kwargs:{}".format(args, kwargs))
        if "media_type" in kwargs:
            new_value = validate_media(kwargs["media_type"])
            if new_value:
                kwargs["media_type"] = new_value
        else:
            raise KeyError("can't find a valid media_type, is 'media_type' key present in function?")
        return func(*args, **kwargs)
    return wrapper


def require_media_in(index):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("args:{}, kwargs:{}, index:{}".format(args, kwargs, index))
            if index and index < len(args):
                print("arg selected: {}".format(args[index]))
                new_value = validate_media(args[index])
                if new_value:
                    args = tuple([new_value if i == index else x for i, x in enumerate(args)])
            else:
                raise IndexError("can't find a valid media_type, is the rigth media_type index in function?")
            return func(*args, **kwargs)
        return wrapper
    return decorator
