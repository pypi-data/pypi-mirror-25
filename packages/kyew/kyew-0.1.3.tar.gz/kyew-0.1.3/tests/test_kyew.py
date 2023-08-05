import pytest
import fakeredis
from kyew import Kyew
from mock import Mock

@pytest.fixture()
def mock_redis(resp=None):
    fake_redis = Mock()
    fake_redis.lpop.return_value = resp
    fake_redis.lpush.return_value = 1
    return fake_redis

def test_pop_without_message():
    kyew = Kyew(mock_redis())
    assert kyew.pop_message('empty_pop') == None

def test_pop_with_message():
    kyew = Kyew(mock_redis('{"hello": "world"}'))
    assert kyew.pop_message('pop') == {'hello': 'world'}

def test_push_without_message():
    kyew = Kyew(mock_redis())
    assert kyew.push_message('empty_push', None) == None

def test_push_with_message():
    kyew = Kyew(mock_redis())
    assert kyew.push_message('push', {'hello': 'world'}) == 1

def test_push_and_pop_with_json():
    redis = fakeredis.FakeStrictRedis()
    kyew = Kyew(redis)
    message = {'hello': 'world'}
    queue_name = 'push_pop'
    kyew.push_message(queue_name, message)
    assert kyew.pop_message(queue_name) == message

def test_push_and_pop_with_string():
    redis = fakeredis.FakeStrictRedis()
    kyew = Kyew(redis)
    message = 'Hello World!'
    queue_name = 'push_pop'
    kyew.push_message(queue_name, message)
    assert kyew.pop_message(queue_name) == message

def test_push_and_pop_from_wrong_queue():
    redis = fakeredis.FakeStrictRedis()
    kyew = Kyew(redis)
    kyew.push_message('push_pop_wrong', {'hello': 'world'})
    assert kyew.pop_message('push_pop_wrong_1') == None
