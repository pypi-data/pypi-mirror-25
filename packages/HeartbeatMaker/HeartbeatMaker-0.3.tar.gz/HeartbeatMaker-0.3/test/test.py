#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import StrictRedis
from HeartbeatMaker import HeartbeatMaker
import arrow


def test(it):
    print('%s:%s:心跳' % (arrow.now(), it))


maker = HeartbeatMaker('redis://localhost:6379/0', 'test-beat', test)

# maker.clean()
# maker.beat_it('bac', 6,'bac-par')
# maker.beat_it('shawn', 2,'par')
maker.omit_it('bac')

# maker.start()
