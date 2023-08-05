#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import StrictRedis
from HeartbeatMaker import HeartbeatMaker
import arrow


def test(it):
    print('%s:%s:心跳' % (arrow.now(), it))


maker = HeartbeatMaker('redis://localhost:6379/0', 'test-beat', test)

# maker.clean()
maker.beat_it('bac', 5)
maker.beat_it('jack', 15)
# maker.omit_it('bac')

# maker.start()
