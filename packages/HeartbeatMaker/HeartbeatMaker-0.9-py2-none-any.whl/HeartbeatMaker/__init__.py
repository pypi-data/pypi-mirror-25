#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .beater import Beater
from concurrent.futures import ProcessPoolExecutor as Executor, ThreadPoolExecutor as TExecutor, wait
from redis import StrictRedis
import logging
import signal

logger = logging.getLogger("HeartbeatMaker")


class HeartbeatMaker(object):
    def __init__(self, redis_url, prefix_key, beat_callback=None, callback_pars=None, max_beaters=20, beater_workers=1):
        self.redis_url = redis_url
        self.prefix_key = prefix_key
        self.beaters_key = self.prefix_key + ":beaters"
        self.max_beaters = max_beaters
        self.beaters = set()
        self.beater_workers = beater_workers
        self.beat_callback = beat_callback
        self.callback_pars = callback_pars
        self.logger = logger
        self.beating = False

        redis = self._get_redis()
        bs = redis.smembers(self.beaters_key)
        if bs:
            for beater in bs:
                interval = int(beater)
                self.beaters.add(interval)

    def start(self):

        self.beating = True

        #  监视新的beater
        ps = self._get_redis().pubsub()
        ps.subscribe(self.prefix_key + ":new-interval")

        def _exit(signum, frame):
            ps.unsubscribe()
            self.stop()

        signal.signal(signal.SIGINT, _exit)
        signal.signal(signal.SIGTERM, _exit)

        self.workers = Executor(max_workers=self.max_beaters)
        try:

            for interval in self.beaters:
                f = self._create_beater(interval)
                f.add_done_callback(lambda x: self.beaters.discard(interval))

            self.logger.warning('%d beater started' % len(self.beaters))

            self._watch_new_interval(ps)
        except KeyboardInterrupt:
            _exit(None, None)
        self.logger.warning('heartbeat maker exit')

    def stop(self):
        if self.beating:
            self.beating = False
            self.logger.warning('stoped')

    def clean(self):
        for interval in self.beaters:
            beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.callback_pars,
                            self.beater_workers)
            beater.clean()
        self._get_redis().delete(self.beaters_key)
        self.beaters.clear()

    def beat_it(self, it, interval, par=None):
        self.omit_it(it)
        beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.callback_pars,
                        self.beater_workers)
        beater.beat_it(it, par)
        self._get_redis().sadd(self.beaters_key, interval)
        self.beaters.add(interval)

        self._get_redis().publish(self.prefix_key + ":new-interval", interval)

    def omit_it(self, it):
        for interval in self.beaters:
            beater = Beater(self.redis_url, self.prefix_key, interval, self.beat_callback, self.callback_pars,
                            self.beater_workers)
            beater.omit_it(it)

    def _create_beater(self, interval):
        return self.workers.submit(_create_worker, self.redis_url, self.prefix_key, interval, self.beat_callback,
                                   self.callback_pars,
                                   self.beater_workers)

    def _watch_new_interval(self, ps):

        self.logger.warning('new-beater-watcher started')
        try:

            for item in ps.listen():
                if item['type'] == 'message':
                    interval = int(item['data'])
                    if interval not in self.beaters:
                        self._create_beater(interval)
                        self.beaters.add(interval)
                        self.logger.info("创建新的Beater(interval=%d)" % interval)

        except:
            self.logger.exception('等待新Beater时,出现异常')

        self.logger.warning('new-beater-watcher exit')

    def _get_redis(self):
        return StrictRedis.from_url(self.redis_url)


def _create_worker(redis_url, prefix_key, interval, beat_callback, callback_pars, worker_number):
    try:
        beater = Beater(redis_url, prefix_key, interval, beat_callback, callback_pars, worker_number)
        beater.start()
    except:
        logger.exception('worker出现异常')
