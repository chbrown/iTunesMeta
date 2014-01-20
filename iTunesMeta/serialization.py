import json
from datetime import date, datetime

date_format = '%Y-%m-%d'
datetime_format = '%Y-%m-%dT%H:%M:%S'


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif hasattr(obj, 'timeIntervalSince1970'):
            return datetime.fromtimestamp(obj.timeIntervalSince1970())
        elif isinstance(obj, datetime):
            # datetime inherits date, so it must be checked first
            return obj.strftime(datetime_format)
        elif isinstance(obj, date):
            return obj.strftime(date_format)
        return super(CustomEncoder, self).default(obj)

custom_encoder = CustomEncoder(sort_keys=True)

def jsonize(obj):
    return custom_encoder.encode(obj)
