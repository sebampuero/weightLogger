import redis
#import rediscluster
import time
import datetime
import common.constants as DBConstants
from functools import reduce

class Database:
    URI = "192.168.2.3"
    redis = None

    @classmethod
    def initialize(cls):
        #startup_nodes = [{"host": URI, "port": "6379"}, {"host": "192.168.2.18", "port": "6379"}]
        cls.redis = redis.StrictRedis(host=cls.URI, decode_responses=True)


    @classmethod
    def saveToDb(cls, weight, unit):
        #check if todays_weight is already been given. If so, delete last entry with year_day of today == year day of last entrys timestamp
        if cls.getLastEntry() is not None:
            last_entry_id, last_entry_ts = cls.getLastEntry()
            if datetime.datetime.fromtimestamp(float(last_entry_ts)).strftime('%j') == datetime.datetime.fromtimestamp(float(time.time())).strftime('%j'):
                cls.redis.hmset('weight:{0}'.format(last_entry_id), {"value":weight, "unit":unit})
                cls.redis.zadd('weights', time.time(), str(last_entry_id))
                return 'OK', None
        try:
            cls.redis.incr(DBConstants.NEXT_WEIGHT_ID)
            cls.redis.incr(DBConstants.WEEKLY_ENTRY_COUNTER)
            weight_id = cls.redis.get(DBConstants.NEXT_WEIGHT_ID)
            cls.redis.hmset('weight:{0}'.format(weight_id), {"value":weight, "unit":unit})
            cls.redis.zadd('weights', time.time(), str(weight_id))
            cls.setWeeklyAverage()
            weekly_counter = cls.redis.get(DBConstants.WEEKLY_ENTRY_COUNTER)
            if int(weekly_counter) == 7:
                last_week_id = cls.redis.get(DBConstants.NEXT_WEEK_ID)
                avg_value = cls.redis.hget('week:{0}'.format(str(last_week_id)), 'avg_value')
                cls.redis.set(DBConstants.WEEKLY_ENTRY_COUNTER, '0')
                return 'OK', str(avg_value)
            return 'OK', None
        except Exception as e:
            print(e)
            return 'ERROR', None


    @classmethod
    def setWeeklyAverage(cls):
        counter = cls.redis.get(DBConstants.WEEKLY_ENTRY_COUNTER)
        if int(counter) == 7:
            # weights = [(id, timestamp), (id, timestamp), ...]
            cls.redis.incr(DBConstants.NEXT_WEEK_ID)
            week_id = cls.redis.get(DBConstants.NEXT_WEEK_ID)
            weights = cls.redis.zrevrange("weights",0,6, withscores=True)
            weight_values = [cls.redis.hget('weight:{0}'.format(str(weight[0])), 'value') for weight in weights]
            last_day_ts = weights[len(weights)-1][1]
            used_unit = cls.redis.hget("weight:{0}".format(str(weights[0][0])), 'unit')
            week_avg = reduce(lambda x, y: float(x) + float(y), weight_values) / len(weight_values)
            cls.redis.hmset('week:{0}'.format(week_id), {'avg_value':str(round(week_avg, 2)), 'unit': used_unit})
            cls.redis.zadd('week_avgs', last_day_ts, week_id)

    @classmethod
    def getLastEntry(cls):
        last_entry =  cls.redis.zrange('weights', -1, -1, withscores=True)
        if len(last_entry) == 0:
            return None
        else:
            return last_entry[0] #return first tuple


    @classmethod
    def getHistoryInDays(cls, days):
        # weights = [(id, timestamp), (id, timestamp), ...]
        try:
            weight_ids = cls.redis.zrevrange('weights', 0, days, withscores=True)
            if len(weight_ids) == 0:
                return ('OK', [], [], None )
            unit = cls.redis.hget('weight:{0}'.format(weight_ids[0][0]), 'unit')
            values = [cls.redis.hget('weight:{0}'.format(str(weight[0])), 'value') for weight in weight_ids]
            days = [datetime.datetime.fromtimestamp(float(ts[1])).strftime('%d-%m') for ts in weight_ids]
            return ('OK',list(reversed(values)), list(reversed(days)), unit)
        except Exception as e:
            print(e)
            return 'ERROR', None, None, None


    @classmethod
    def getHistoryInWeeks(cls, weeks):
        try:
            week_ids = cls.redis.zrevrange('week_avgs', 0, weeks, withscores=True)
            if len(week_ids) == 0:
                return ('OK', [], [], None )
            unit = cls.redis.hget('week:{0}'.format(week_ids[0][0]), 'unit')
            avg_values = [cls.redis.hget('week:{0}'.format(str(week[0])), 'avg_value') for week in week_ids]
            day_in_week = [datetime.datetime.fromtimestamp(float(ts[1])).strftime('%d-%m') for ts in week_ids]
            return ('OK',list(reversed(avg_values)), list(reversed(day_in_week)), unit)
        except Exception as e:
            print(e)
            return 'ERROR', None, None, None
