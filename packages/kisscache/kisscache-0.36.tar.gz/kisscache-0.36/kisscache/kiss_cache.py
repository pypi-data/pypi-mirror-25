# -*- coding:utf-8 -*-

"""kiss cache.

dependens appid.py
put appid into appid module.


cache by set func
>>> import appid
>>> appid.appid = 'kiss_cache_test'
>>> import kiss_cache
>>> key = "keyX"
>>> value = "valueX"
>>> appid.appid
'kiss_cache_test'
>>> kiss_cache_static = SqlalchemyCache()
>>> kiss_cache_static.set(key, value)
>>> kiss_cache_static.get(key)
'valueX'
>>> kiss_cache_static.delete(key)
>>> kiss_cache_static.sets([["12key", "value1"],["13key", "value21"]])
>>> kiss_cache_static.get("13key")
'value21'
>>> kiss_cache_static.deleteEndwith("key")
>>> kiss_cache_static.set("timekey", "abc", 2)
>>> "timekey" in kiss_cache_static
True
>>> import time
>>> time.sleep(2)
>>> "timekey" in kiss_cache_static
False


>>> NativeCache_static = NativeCache()
>>> NativeCache_static.set(key, "valueY")
>>> NativeCache_static.get(key)
'valueY'
>>> NativeCache_static.delete(key)
>>> NativeCache_static.sets([["21key", "value1"],["22key", "value2"]])
>>> NativeCache_static.get("22key")
'value2'
>>> "22key" in NativeCache_static
True
>>> NativeCache_static.deleteEndwith("key")
True
>>> "22key" in NativeCache_static
False

"""


import datetime
import time
import logging

flag = 0
try:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.schema import Column
    from sqlalchemy.types import Integer, String, DATETIME
    from sqlalchemy.engine import create_engine
    from sqlalchemy.orm.session import sessionmaker
    Base = declarative_base()

except BaseException:
    flag = 1


appid = 'kiss_cache_test'

if flag != 1:
    class Cache(Base):
        """Cache class.
        """
        __tablename__ = 'cache{appid}'.format(**dict(appid=appid))

        id = Column(Integer, primary_key=True, autoincrement=True)
        ch = Column(Integer, nullable=False)
        cle = Column(String, nullable=False)
        val = Column(String)
        timeout = Column(Integer, default=float("inf"))
        dt = Column(DATETIME, default=datetime.datetime.now, nullable=False)

        def __repr__(self):
            return '<Cache(%d, %s, %s, %s, ch:%d)>' % (
                self.id, self.cle, self.val, self.dt, self.ch)


class SqlalchemyCache(object):
    def __init__(self, appid=appid):
        param = dict(appid=appid)
        try:
            self.engine = create_engine(
                'sqlite:///{appid}.sqlite3'.format(**param), echo=False)
            Base.metadata.create_all(self.engine)
            self.SessionMaker = sessionmaker(bind=self.engine)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logging.error(e)

    #----------------------------------------------------------------------
    def __contains__(self, key, **kw):
        """contain method.

		It checks if the value exist or not
		keyword arguments:
		key -- name of the key

		return -- True if key exist otherwise return False
		"""
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        item_buf = session.query(Cache.cle).filter(Cache.ch == ch).all()
        for item in item_buf:
            if key == item[0]:
                timeout = self.checktimeout(key)
                if timeout == 0:
                    return True
        return False

    def config(self, *ar, **kw):
        self.config = kw

    def set(self, key, value, timeout=float("inf"), **kw):
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        now = None
        # upcerting

        item_buf = session.query(Cache).filter(
            Cache.cle == key, Cache.ch == ch)

        if item_buf.count() == 0:
            # 'insert'
            session.add(Cache(ch=ch, cle=key, val=value, timeout=timeout))
        else:
            # 'updating'
            if not now:
                now = datetime.datetime.now()
            assert item_buf.count() == 1

            item_buf.update({'id': Cache.id, 'val': value,
                             'timeout': timeout, 'dt': now})
        session.commit()

    def sets(self, item_list, **kw):
        assert isinstance(item_list, list)
        if len(item_list):
            for item in item_list:
                assert isinstance(item, list) and len(item) >= 2
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        now = None
        for item_pair in item_list:
            # upcerting
            try:
                timeout = item_pair[2]
            except BaseException:
                timeout = float("inf")
            item_buf = session.query(Cache).filter(
                Cache.cle == item_pair[0], Cache.ch == ch)
            if item_buf.count() == 0:
                # 'insert'
                session.add(
                    Cache(
                        ch=ch,
                        cle=item_pair[0],
                        val=item_pair[1],
                        timeout=timeout))

            else:
                # 'updating'
                if not now:
                    now = datetime.datetime.now()
                assert item_buf.count() == 1
                item_buf.update(
                    {'id': Cache.id, 'val': item_pair[1], 'timeout': timeout, 'dt': now})
        session.commit()

    def deleteList(self, cles, **kw):
        assert isinstance(cles, list)
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        for idx in range(len(cles)):
            item_buf = session.query(Cache).filter(
                Cache.cle == cles[idx], Cache.ch == ch)
            if item_buf.count() == 0:
                return
            'deleteing'
            assert item_buf.count() == 1
            session.delete(item_buf[0])
        session.commit()

    def deleteEndwith(self, key, **kw):
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        item_buf = session.query(Cache.cle).filter(Cache.ch == ch).all()
        for item in item_buf:
            if item[0].endswith(key):
                item_del = session.query(Cache).filter(
                    Cache.cle == item[0], Cache.ch == ch)
                session.delete(item_del[0])
        session.commit()

    def delete(self, key, **kw):
        #assert isinstance(key)
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        item_buf = session.query(Cache).filter(
            Cache.cle == key, Cache.ch == ch)
        if item_buf.count() == 0:
            return
        'deleteing'
        assert item_buf.count() == 1
        session.delete(item_buf[0])
        session.commit()

    def get(self, key, **kw):
        assert not isinstance(key, list)
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        item_buf = session.query(Cache).filter(
            Cache.cle == key, Cache.ch == ch)
        cnt = item_buf.count()
        if cnt == 1:
            timeout = self.checktimeout(key)
            if timeout == 0:
                return item_buf[0].val
            else:
                raise KeyError("Key timeout: " + key)

        else:
            assert cnt == 0
            raise KeyError("Not Found: " + key)


    def checktimeout(self, key, **kw):
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        item_buf = session.query(
            Cache.dt, Cache.timeout).filter(Cache.cle == key, Cache.ch == ch).first()
        now = datetime.datetime.now()
        delta_time = (now - item_buf[0]).total_seconds()
        timeout = float(item_buf[1])
        if delta_time >= timeout:
            item_del = session.query(Cache).filter(
                Cache.cle == key, Cache.ch == ch)
            session.delete(item_del[0])
            session.commit()
            return 1
        return 0

    def dump(self, **kw):
        debug = kw.get('debug')
        ch = kw.get('ch', 0)
        session = self.SessionMaker()
        item_buf = session.query(Cache)
        for i in item_buf:
            print(str(i))
    def connected_module(self):
        return "Sqlalchemy"


class NativeCache(object):
    """My Cache Class. It uses simple python function to get and set cache keys and values."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor.

        Create a cache dictionary object.
        """
        self.cache = {}

    #----------------------------------------------------------------------
    def __contains__(self, key):
        """contain method.

		It checks if the value exist or not
		keyword arguments:
		key -- name of the key

		return -- True if key exist otherwise return False
		"""
        if key in self.cache:
            timeout = self.checktimeout(key)
            if timeout == None:
                return True
        return False

    #----------------------------------------------------------------------

    def set(self, key, value, timeout=None, **kw):
        """Function set the value of the key. It takes key, value and timeout as arguments.

        keyword arguments:
        key -- name of the key
        value -- value of the key
        timeout -- Time after which key has to be deleted

        It saves the value of key with timeout.
        """
        value_temp = self.cache.get(key)
        ch = kw.get('ch', 0)
        if value_temp is not None:
            self.cache.pop(key)
        self.cache[key] = {'date_accessed': datetime.datetime.now(),
                           'value': value,
                           'timeout': timeout,
                           'ch': ch}

    #----------------------------------------------------------------------

    def sets(self, item_list, **kw):
        """Function set the value of the key. It takes key, value and timeout as arguments.

        keyword arguments:
        item_list -- list of items
        item_list contains a list of key, value and timeout

        It saves the value of keys with timeout.
        """
        assert isinstance(item_list, list)
        ch = kw.get('ch', 0)
        for item_pair in item_list:
            try:
                timeout = item_pair[2]
            except BaseException:
                timeout = float("inf")
            key = item_pair[0]
            value = self.cache.get(key)
            if value is not None:
                self.cache.pop(key)

            self.cache[key] = {'date_accessed': datetime.datetime.now(),
                               'value': item_pair[1],
                               'timeout': timeout,
                               'ch': ch}

    #----------------------------------------------------------------------
    def checktimeout(self, key, **kw):
        """Function check the timeout for a key.

        keyword arguments:
        key -- name of the key whose timeout has to bec checked

        If key value found and delta time is grater than timeout
           return success after deleting it
        else
           it will return None .
        """
        ch = kw.get('ch', 0)
        if self.cache[key]['timeout'] is None:
            return None
        now = datetime.datetime.now()
        delta_time = (now - self.cache[key]['date_accessed']).total_seconds()
        if delta_time >= self.cache[key]['timeout'] and ch == self.cache[key]['ch']:
            self.deleteList(key)
            raise KeyError("Key timeout: " +  key)
        return None

    #----------------------------------------------------------------------

    def get(self, key2, **kw):
        """Function retrieve the value for a key.

        keyword arguments:
        key2 -- name of the key whose value has to be obtained

        If key value found
           return the value of key
        else
           it will return None to the controller.
        In that case controller it  will calculate the value of that key
        It will also call set function to save it into cache.

        """
        ch = kw.get('ch', 0)
        try:
            data = self.cache.get(key2)
            timeout = self.checktimeout(key2)
            if timeout is not None:
                raise KeyError("Key not found: " + key2)

            return data['value']
        except Exception as e:
            raise KeyError("Key exception: " +  str(e))

#----------------------------------------------------------------------
    def deleteList(self, cles):
        """Function delete the list of keys.

        keyword arguments:
        key2 -- name of the key to be deleted

        It return a message
        """

        for key in cles:
            value = self.cache.get(key)
            if value is not None:
                self.cache.pop(key)


#----------------------------------------------------------------------
    def deleteEndwith(self, key2):
        """Function delete the list of keys which ends with same String.

        keyword arguments:
        key2 -- name of the keys whose match keys has to be deleted

        It return a message
        """
        flag = 0
        for key in list(self.cache):
            if key.endswith(key2):
                self.cache.pop(key)
                flag += 1
        return True

#----------------------------------------------------------------------

    def delete(self, key2):
        """Function delete the key and it's value.

        keyword arguments:
        key2 -- name of the key to be deleted

        It return a message
        """
        value = self.cache.get(key2)
        if value is not None:
            self.cache.pop(key2)
            #return "Success"
        #return "Key not found"

#----------------------------------------------------------------------
    @property
    def size(self):
        """Return the size of cache."""
        return len(self.cache)

    def dump(self):
        for i in self.cache:
            print(str(i))
    def connected_module(self):
        return "simple python"

#----------------------------------------------------------------------

class RedisCache(object):
    """The Redis Class."""

    def __init__(self):
        """The Redis Constructor."""
        import redis
        # redis.ConnectionPool(host='127.0.0.1', port='6379', db=0)
        self.POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        redis = redis.Redis(connection_pool=self.POOL)
        redis.set("Connection", "OK")
        #print("Error with Redis connection")

    #----------------------------------------------------------------------
    def __contains__(self, key):
        """contain method.

		It checks if the value exist or not
		keyword arguments:
		key -- name of the key

		return -- True if key exist otherwise return False
		"""
        my_server = redis.Redis(connection_pool=self.POOL)
        flag = my_server.exist(key)
        if flag == 1:
            return True
        return False

    def set(self, key, value, timeout=None):
        """Function add a key and it's value from redis server."""
        my_server = redis.Redis(connection_pool=self.POOL)
        my_server.set(key, value)
        if timeout is not None:
            my_server.expire(key, timeout)

    def sets(self, item_list):
        """Function add a key and it's value from redis server."""
        assert isinstance(item_list, list)
        my_server = redis.Redis(connection_pool=self.POOL)

        for item_pair in item_list:
            try:
                timeout = item_pair[2]
            except BaseException:
                timeout = None

            my_server.set(key, value)
            if timeout is not None:
                my_server.expire(key, timeout)

    def get(self, key):
        """Function retrieve a key and it's value from redis server."""
        my_server = redis.Redis(connection_pool=self.POOL)
        response = my_server.get(key)
        if response is not None:
            return response.decode()
        return response

    def deleteEndwith(self, key):
        """Function delete a list of keys which ends with a format from redis server."""
        my_server = redis.Redis(connection_pool=self.POOL)
        for rediskey in my_server.scan_iter("*" + key):
            my_server.delete(rediskey)

    def deleteList(self, cles):
        """Function delete a list of keys from redis server."""
        my_server = redis.Redis(connection_pool=self.POOL)
        for key in cles:
            my_server.delete(key)

    def delete(self, key):
        """Function delete a key and it's value from redis server."""
        my_server = redis.Redis(connection_pool=self.POOL)
        my_server.delete(key)

    def connected_module(self):
        return "redis"

#----------------------------------------------------------------------



"""
get
"""

if flag != 1:
    kiss_cache_static = SqlalchemyCache()
    config = kiss_cache_static.config
    get = kiss_cache_static.get
    sets = kiss_cache_static.sets
    set = kiss_cache_static.set
    delete = kiss_cache_static.delete
    deleteList = kiss_cache_static.deleteList
    deleteEndwith = kiss_cache_static.deleteEndwith
    dump = kiss_cache_static.dump

__all__ = ('config', 'get', 'set', 'sets', 'delete', 'dump')

"""
if __name__ == '__main__':
    import appid
    appid.appid = 'kiss_cache_test'
    print('main:hello')
    import kiss_cache

    try:
        value = kiss_cache.get("MyKey1")
        print(value)
    except BaseException:
        print('value not found')

    # kiss_cache.set("12MyKey","MyVal1")
    kiss_cache.sets([["12MyKey", "MyVal1", 2], ["13MyKey", "MyVal2"]])
    val = kiss_cache.get("12MyKey")
    print("main:" + val)
    # kiss_cache.deleteEndwith("3MyKey")
    print('main:bye')
"""

'''
if __name__ == '__main__':

    print('main:hello - expected to be cached')

    import appid
    appid.appid = 'kiss_cache_test'
    import kiss_cache
    print(kiss_cache.__version__)
    kiss_cache.set("12MyKey", "aaaa")
    try:
        value = kiss_cache.get("12MyKey")
        print(value)
        time.sleep(2)
        value1 = kiss_cache.get("12MyKey")
        print(value1)
    except KeyError:
        import traceback
        print('value not found: %s' % traceback.format_exc())

'''
class MainCacheClass:
    def __init__(self, mode):
        self.mode = mode

    def cache(self):
        if self.mode == "redis":
            try:
                self.cache = RedisCache()
                module = "Redis"
            except BaseException as e:
                raise("Can't able to connect Redis. " + str(e))

        elif self.mode == "sqlalchemy":
            try:
                self.cache = SqlalchemyCache()
            except BaseException as e:
                print("Can't able to connect SqlalchemyCache. "  + str(e))

        else:
            try:
                self.cache = NativeCache()
            except BaseException as e:
                print("Can't able to connect NativeCache. " + str(e))

        return self.cache



try:
    cache = RedisCache()
except:
    try:
        if flag != 1:
            cache = SqlalchemyCache()
        else:
            cache = NativeCache()
    except:
        cache = NativeCache()
