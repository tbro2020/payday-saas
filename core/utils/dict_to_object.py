from django.utils.text import slugify

class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = DictToObject(value)
            _key = slugify(key).replace('-', '_')
            setattr(self, _key.lower(), value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"