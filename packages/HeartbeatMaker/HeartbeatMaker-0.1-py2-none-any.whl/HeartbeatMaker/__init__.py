#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .beater import Beater
from concurrent.futures import ProcessPoolExecutor as Executor, wait
from redis import StrictRedis


class HeartbeatMaker(object):
    def __init__(self, redis_url, prefix_key, beat_callback, max_beaters=20, beater_workers=1):
        self.redis_url = redis_url
        self.prefix_key = prefix_key
        self.beaters_key = self.prefix_key + ":beaters"
        self.beaters = set()
        self.beater_workers = beater_workers
        self.beat_callback = beat_callback

        redis = self._get_redis()
        bs = redis.smembers(self.beaters_key)
        if bs:
            for beater in bs:
                interval = int(beater)
                self.beaters.add(interval)

        self.workers = Executor(max_workers=max_beaters)

    def start(self):

        fss = []
        for interval in self.beaters:
            fs = self.workers.submit(_create_worker, self.redis_url, self.prefix_key, interval, self.beat_callback,
                                     self.beater_workers)
            fss.append(fs)

        wait(fss)

    def stop(self):
        self.workers.shutdown()

    def clean(self):
        for interval in self.beaters:
            beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.beater_workers)
            beater.clean()
        self._get_redis().delete(self.beaters_key)

    def beat_it(self, it, interval):
        self.omit_it(it)
        beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.beater_workers)
        beater.beat_it(it)
        self._get_redis().sadd(self.beaters_key, interval)
        self.beaters.add(interval)

    def omit_it(self, it):
        for interval in self.beaters:
            beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.beater_workers)
            beater.omit_it(it)

    def _get_redis(self):
        return StrictRedis.from_url(self.redis_url)


def _create_worker(redis_url, prefix_key, interval, beat_callback, worker_number):
    beater = Beater(redis_url, prefix_key, interval, beat_callback, worker_number)
    beater.start()
