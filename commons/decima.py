import json
from datetime import datetime, date
from time import time, struct_time, mktime
import decimal

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        if isinstance(o, date):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, struct_time):
            return datetime.fromtimestamp(mktime(o))
        # Any other serializer if needed
        return super(CustomJSONEncoder, self).default(o)