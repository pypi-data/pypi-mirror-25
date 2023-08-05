import importlib


def import_object(path) -> object:
    if path.count('.') == 0:
        return importlib.import_module(path)

    parts = path.split('.')

    try:
        obj = importlib.import_module('.'.join(parts[:-1]))
    except ImportError:
        return importlib.import_module(path)
    else:
        try:
            return getattr(obj, parts[-1])
        except AttributeError:
            raise ImportError('No module named {}'.format(parts[-1]))
