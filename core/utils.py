def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)

class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict) and key != 'metadata':
                value = DictToObject(value)
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"