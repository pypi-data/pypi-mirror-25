import json

class Kyew(object):

    def __init__(self, r='redis://localhost:6379'):
        if isinstance(r, str):
            self.redis = redis.from_url(r)
        else:
            self.redis = r

    def pop_message(self, queue_name):
        message = self.redis.lpop(queue_name)
        return self._parse(message)

    def push_message(self, queue_name, message):
        if message == None:
            return None
        return self.redis.lpush(queue_name, self._dump(message))

    def _parse(_self, message):
        try:
            return json.loads(message)
        except TypeError:
            return message

    def _dump(_self, message):
        try:
            return json.dumps(message, separators=(',', ':'))
        except TypeError:
            return message
