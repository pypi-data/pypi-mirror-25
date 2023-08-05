#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor as Executor, wait
import time
import logging
from redis import StrictRedis
import signal


class Beater(object):
    def __init__(self, redis_url, prefix_key, interval, beat_callback, worker_number=1):
        self.redis_url = redis_url
        self.interval = interval
        self.beat_callback = beat_callback
        self.worker_number = worker_number
        self.prefix_key = prefix_key + ':beater-' + str(interval)
        self.beating_mapping_key = self.prefix_key + ':beating-items'

        self.beating = False
        self.executor = None
        self.redis = None
        self.last_pool_index = -1
        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGTERM, self._exit)

        self.logger = logging.getLogger("beater.%d" % interval)

    def beat_it(self, it):

        if self._get_redis().hexists(self.beating_mapping_key, it):
            return

        latest_pool_size = 0
        for i in range(0, self.interval):
            pool_key = self.prefix_key + ":pool:%d" % i
            pool_size = self._get_redis().scard(pool_key)
            if pool_size > 0:
                current_pool_size = pool_size

                # 如果当前pool比上一个小,则放到当前pool
                if current_pool_size < latest_pool_size:

                    pipeline = self._get_redis().pipeline()
                    pipeline.sadd(pool_key, it)
                    pipeline.hset(self.beating_mapping_key, it, i)
                    pipeline.execute()
                    break

                else:  # maybe next pool

                    if i == self.interval - 1:  # last pool,put it in first pool
                        first_pool_key = self.prefix_key + ":pool:0"
                        pipeline = self._get_redis().pipeline()
                        pipeline.sadd(first_pool_key, it)
                        pipeline.hset(self.beating_mapping_key, it, 0)
                        pipeline.execute()
                        break
                    else:
                        latest_pool_size = current_pool_size

            else:  # first item in current pool
                pipeline = self._get_redis().pipeline()
                pipeline.sadd(pool_key, it)
                pipeline.hset(self.beating_mapping_key, it, i)
                pipeline.execute()

                break

    def omit_it(self, it):
        pool_index = self._get_redis().hget(self.beating_mapping_key, it)
        if pool_index:
            pool_key = self.prefix_key + ":pool:%d" % int(pool_index)

            pipeline = self._get_redis().pipeline()
            pipeline.srem(pool_key, it)
            pipeline.hdel(self.beating_mapping_key, it)
            pipeline.execute()

    def start(self):
        if self.beating:
            return

        self.executor = Executor(max_workers=self.worker_number)
        self.beating = True

        while self.beating:
            start_time = time.time()
            cost = self._tick()
            end_timestamp = int(time.time())
            if int(start_time) == end_timestamp:
                if cost < 1:
                    time.sleep((end_timestamp + 1) - start_time)  # 等到下秒

    def _exit(self, signum, frame):
        self.stop()

    def stop(self):
        self.logger.warning('beater %d exit' % self.interval)
        self.beating = False

    def clean(self):
        pipeline = self._get_redis().pipeline()
        for i in range(0, self.interval):
            pipeline.delete(self.prefix_key + ":pool:%d" % i)

        pipeline.delete(self.beating_mapping_key)
        pipeline.execute()

    def _get_redis(self):
        if not self.redis:
            self.redis = StrictRedis.from_url(self.redis_url)
        return self.redis

    def _tick(self):

        start_time = time.time()
        timestamp = int(start_time)

        pool_index, key = self._get_pool(timestamp)

        if self.last_pool_index > -1 and pool_index != self.last_pool_index + 1 and (
                        pool_index == 0 and self.last_pool_index + 1 != self.interval):
            self.logger.warning("pool:%d ~ %d:被跳过了" % (self.last_pool_index + 1, pool_index - 1))

        log_prefix = str(timestamp) + ':pool:' + str(pool_index)
        self.logger.info("%s: 准备处理:%s" % (log_prefix, start_time))

        items = self._get_redis().smembers(key)
        if items:
            self._process(items)

        cost = time.time() - start_time
        self.logger.info("%s,处理完毕,耗时:%f s" % (log_prefix, cost))
        self.last_pool_index = pool_index

        return int(cost)

    def _process(self, items):

        fs = []
        for it in items:
            fs.append(self.executor.submit(self.beat_callback, it.decode('utf-8')))
        wait(fs)

    def _get_pool(self, timestamp):

        pool_index = timestamp % self.interval

        key = self.prefix_key + ':pool:' + str(pool_index)

        return pool_index, key
