#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .beater import Beater
from concurrent.futures import ProcessPoolExecutor as Executor, ThreadPoolExecutor as TExecutor, wait
from redis import StrictRedis
import logging
import signal


class HeartbeatMaker(object):
    def __init__(self, redis_url, prefix_key, beat_callback, max_beaters=20, beater_workers=1):
        self.redis_url = redis_url
        self.prefix_key = prefix_key
        self.beaters_key = self.prefix_key + ":beaters"
        self.beaters = set()
        self.beater_workers = beater_workers
        self.beat_callback = beat_callback
        self.logger = logging.getLogger("HeartbeatMaker")

        redis = self._get_redis()
        bs = redis.smembers(self.beaters_key)
        if bs:
            for beater in bs:
                interval = int(beater)
                self.beaters.add(interval)

        self.workers = Executor(max_workers=max_beaters)
        self.watcher_worker = TExecutor(max_workers=1)

    def start(self):

        #  监视新的beater
        ps = self._get_redis().pubsub()
        ps.subscribe(self.prefix_key + ":new-interval")

        def _exit(signum, frame):
            ps.unsubscribe()
            self.logger.warning('new beater watcher exit')

        signal.signal(signal.SIGINT, _exit)
        signal.signal(signal.SIGTERM, _exit)
        self.watcher_worker.submit(self._watch_new_interval,ps)

        fs = []
        for interval in self.beaters:
            f = self._create_beater(interval)
            fs.append(f)
        try:
            wait(fs)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.workers.shutdown()
        self.watcher_worker.shutdown()

    def clean(self):
        for interval in self.beaters:
            beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.beater_workers)
            beater.clean()
        self._get_redis().delete(self.beaters_key)

    def beat_it(self, it, interval, par=None):
        self.omit_it(it)
        beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.beater_workers)
        beater.beat_it(it, par)
        self._get_redis().sadd(self.beaters_key, interval)
        self.beaters.add(interval)

        self._get_redis().publish(self.prefix_key + ":new-interval", interval)

    def omit_it(self, it):
        for interval in self.beaters:
            beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.beater_workers)
            beater.omit_it(it)

    def _create_beater(self, interval):
        return self.workers.submit(_create_worker, self.redis_url, self.prefix_key, interval, self.beat_callback,
                                   self.beater_workers)

    def _watch_new_interval(self,ps):

        for item in ps.listen():
            if item['type'] == 'message':
                interval = int(item['data'])
                if interval not in self.beaters:
                    self._create_beater(interval)
                    self.beaters.add(interval)
                    self.logger.info("创建新的Beater(interval=%d)" % interval)

    def _get_redis(self):
        return StrictRedis.from_url(self.redis_url)


def _create_worker(redis_url, prefix_key, interval, beat_callback, worker_number):
    beater = Beater(redis_url, prefix_key, interval, beat_callback, worker_number)
    beater.start()
