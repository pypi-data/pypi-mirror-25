#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""A few checks at the UTFVP database.
"""

import os
import numpy
import nose.tools
from nose.plugins.skip import SkipTest

from . import Database


# base directories where the UTFVP files sit
DATABASE_PATH = "/idiap/resource/database/UTFVP/data"


def sql3_available(test):
  """Decorator for detecting if the sql3 file is available"""

  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = datafile("db.sql3", __name__, None)
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The interface SQL file (%s) is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'utfvp'))

  return wrapper


def db_available(test):
  """Decorator for detecting if the database files are available"""

  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    if os.path.exists(DATABASE_PATH):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The database path (%s) is not available" % (DATABASE_PATH))

  return wrapper


@sql3_available
def test_clients():

  # test whether the correct number of clients is returned
  db = Database()

  nose.tools.eq_(len(db.groups()), 3)
  nose.tools.eq_(len(db.protocols()), 15)
  nose.tools.eq_(len(db.protocol_names()), 15)
  nose.tools.eq_(len(db.purposes()), 3)

  nose.tools.eq_(len(db.clients()), 360)
  nose.tools.eq_(len(db.clients(protocol='1vsall')), 360)
  nose.tools.eq_(len(db.clients(protocol='nom')), 360)
  nose.tools.eq_(len(db.clients(protocol='nomLeftRing')), 60)
  nose.tools.eq_(len(db.clients(protocol='nomLeftMiddle')), 60)
  nose.tools.eq_(len(db.clients(protocol='nomLeftIndex')), 60)
  nose.tools.eq_(len(db.clients(protocol='nomRightIndex')), 60)
  nose.tools.eq_(len(db.clients(protocol='nomRightMiddle')), 60)
  nose.tools.eq_(len(db.clients(protocol='nomRightRing')), 60)
  nose.tools.eq_(len(db.clients(protocol='full')), 360)
  nose.tools.eq_(len(db.clients(protocol='fullLeftRing')), 60)
  nose.tools.eq_(len(db.clients(protocol='fullLeftMiddle')), 60)
  nose.tools.eq_(len(db.clients(protocol='fullLeftIndex')), 60)
  nose.tools.eq_(len(db.clients(protocol='fullRightIndex')), 60)
  nose.tools.eq_(len(db.clients(protocol='fullRightMiddle')), 60)
  nose.tools.eq_(len(db.clients(protocol='fullRightRing')), 60)

  nose.tools.eq_(len(db.client_ids()), 360)
  nose.tools.eq_(len(db.client_ids(protocol='1vsall')), 360)
  nose.tools.eq_(len(db.client_ids(protocol='nom')), 360)
  nose.tools.eq_(len(db.client_ids(protocol='nomLeftRing')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='nomLeftMiddle')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='nomLeftIndex')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='nomRightIndex')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='nomRightMiddle')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='nomRightRing')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='full')), 360)
  nose.tools.eq_(len(db.client_ids(protocol='fullLeftRing')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='fullLeftMiddle')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='fullLeftIndex')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='fullRightIndex')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='fullRightMiddle')), 60)
  nose.tools.eq_(len(db.client_ids(protocol='fullRightRing')), 60)

  nose.tools.eq_(len(db.models()), 4780) #1300 + 300 + 50 * 6 + 1440 + 240 * 6
  nose.tools.eq_(len(db.models(protocol='1vsall')), 1300) # (35 clients * 5 fingers per client * 4 samples per finger) + (25 clients * 6 fingers per client * 4 samples per finger)
  nose.tools.eq_(len(db.models(protocol='nom')), 300) # (1 model per finger * 6 fingers per client) * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='nomLeftRing')), 50) # 1 model per client * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='nomLeftMiddle')), 50) # 1 model per client * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='nomLeftIndex')), 50) # 1 model per client * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='nomRightIndex')), 50) # 1 model per client * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='nomRightMiddle')), 50) # 1 model per client * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='nomRightRing')), 50) # 1 model per client * (18 "dev" clients + 32 "eval" clients)
  nose.tools.eq_(len(db.models(protocol='full')), 1440) # 60 clients * 6 fingers per client * 4 samples per finger
  nose.tools.eq_(len(db.models(protocol='fullLeftRing')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.models(protocol='fullLeftMiddle')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.models(protocol='fullLeftIndex')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.models(protocol='fullRightIndex')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.models(protocol='fullRightMiddle')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.models(protocol='fullRightRing')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  nose.tools.eq_(len(db.model_ids()), 4780) #1300 + 300 + 50 * 6 + 1440 + 240 * 6
  nose.tools.eq_(len(db.model_ids(protocol='1vsall')), 1300)
  nose.tools.eq_(len(db.model_ids(protocol='nom')), 300)
  nose.tools.eq_(len(db.model_ids(protocol='nom', groups='dev')), 108) #18 subjects *6 fingers
  nose.tools.eq_(len(db.model_ids(protocol='nom', groups='eval')), 192) #32 subjects *6 fingers

  nose.tools.eq_(len(db.model_ids(protocol='nomLeftRing')), 50)
  nose.tools.eq_(len(db.model_ids(protocol='nomLeftRing', groups='dev')), 18)
  nose.tools.eq_(len(db.model_ids(protocol='nomLeftRing', groups='eval')), 32)

  nose.tools.eq_(len(db.model_ids(protocol='nomLeftMiddle')), 50)
  nose.tools.eq_(len(db.model_ids(protocol='nomLeftMiddle', groups='dev')), 18)
  nose.tools.eq_(len(db.model_ids(protocol='nomLeftMiddle', groups='eval')), 32)

  nose.tools.eq_(len(db.model_ids(protocol='nomLeftIndex')), 50)
  nose.tools.eq_(len(db.model_ids(protocol='nomLeftIndex', groups='dev')), 18)
  nose.tools.eq_(len(db.model_ids(protocol='nomLeftIndex', groups='eval')), 32)

  nose.tools.eq_(len(db.model_ids(protocol='nomRightIndex')), 50)
  nose.tools.eq_(len(db.model_ids(protocol='nomRightIndex', groups='dev')), 18)
  nose.tools.eq_(len(db.model_ids(protocol='nomRightIndex', groups='eval')), 32)

  nose.tools.eq_(len(db.model_ids(protocol='nomRightMiddle')), 50)
  nose.tools.eq_(len(db.model_ids(protocol='nomRightMiddle', groups='dev')), 18)
  nose.tools.eq_(len(db.model_ids(protocol='nomRightMiddle', groups='eval')), 32)

  nose.tools.eq_(len(db.model_ids(protocol='nomRightRing')), 50)
  nose.tools.eq_(len(db.model_ids(protocol='nomRightRing', groups='dev')), 18)
  nose.tools.eq_(len(db.model_ids(protocol='nomRightRing', groups='eval')), 32)

  nose.tools.eq_(len(db.model_ids(protocol='full')), 1440)

  nose.tools.eq_(len(db.model_ids(protocol='fullLeftRing')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.model_ids(protocol='fullLeftMiddle')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.model_ids(protocol='fullLeftIndex')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.model_ids(protocol='fullRightIndex')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.model_ids(protocol='fullRightMiddle')), 240) # 60 clients * 1 finger per client * 4 samples per finger
  nose.tools.eq_(len(db.model_ids(protocol='fullRightRing')), 240) # 60 clients * 1 finger per client * 4 samples per finger


@sql3_available
def test_objects():

  # tests if the right number of File objects is returned
  db = Database()

  # Protocol '1vsall'
  nose.tools.eq_(len(db.objects(protocol='1vsall')), 1440) #1440 - 60 users * 6 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='world')), 140) #35 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='world', purposes='train')), 140) #35 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev')), 1300) #(1440-140)
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',))), 1300)
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', purposes='enroll')), 1300)
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='probe')), 1299)
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', purposes='probe', classes='impostor')), 1300)
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='client')), 3) # 4 acq - 1
  nose.tools.eq_(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='impostor')), 1296) #1300 - 4 acq


@sql3_available
def test_objects_2():

  # tests if the right number of File objects is returned
  db = Database()


  #####################################################
  # Protocol 'nom'
  nose.tools.eq_(len(db.objects(protocol='nom')), 1440) #1440 - 60 subjects * 6 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nom', groups='world')), 240) #10 users * 6 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='world', purposes='train')), 240) #10 users * 6 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev')), 432) #18 users * 6 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',))), 218) #18 users * 6 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev', purposes='enroll')), 216) #18 users * 6 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='probe')), 216) #18 users * 6 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='probe', classes='impostor')), 214) #384 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval')), 768) #32 users * 6 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',))), 386) #32 users * 6 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval', purposes='enroll')), 384) #18 users * 6 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='probe')), 384) #18 users * 6 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='probe', classes='impostor')), 382) #384 - 2


@sql3_available
def test_objects_3():

  # tests if the right number of File objects is returned
  db = Database()

  #####################################################
  # Protocol 'nomLeftRing'
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='world')), 40) #10 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev')), 72) #18 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',))), 38) #18 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev', purposes='enroll')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='probe', classes='impostor')), 34) #36 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval')), 128) #32 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',))), 66) #32 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval', purposes='enroll')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='probe', classes='impostor')), 62) #64 - 2


  #####################################################
  # Protocol 'nomLeftMiddle'
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='world')), 40) #10 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev')), 72) #18 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',))), 38) #18 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev', purposes='enroll')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='probe', classes='impostor')), 34) #36 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval')), 128) #32 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',))), 66) #32 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval', purposes='enroll')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='probe', classes='impostor')), 62) #64 - 2


  #####################################################
  # Protocol 'nomLeftIndex'
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='world')), 40) #10 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev')), 72) #18 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',))), 38) #18 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev', purposes='enroll')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='probe', classes='impostor')), 34) #36 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval')), 128) #32 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',))), 66) #32 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval', purposes='enroll')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='probe', classes='impostor')), 62) #64 - 2


@sql3_available
def test_objects_4():

  # tests if the right number of File objects is returned
  db = Database()

  #####################################################
  # Protocol 'nomRightIndex'
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='world')), 40) #10 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev')), 72) #18 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',))), 38) #18 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev', purposes='enroll')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='probe', classes='impostor')), 34) #36 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval')), 128) #32 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',))), 66) #32 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval', purposes='enroll')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='probe', classes='impostor')), 62) #64 - 2


  #####################################################
  # Protocol 'nomRightMiddle'
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='world')), 40) #10 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev')), 72) #18 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',))), 38) #18 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev', purposes='enroll')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='probe', classes='impostor')), 34) #36 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval')), 128) #32 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',))), 66) #32 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval', purposes='enroll')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='probe', classes='impostor')), 62) #64 - 2


  #####################################################
  # Protocol 'nomRightRing'
  nose.tools.eq_(len(db.objects(protocol='nomRightRing')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

  # World group
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='world')), 40) #10 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev')), 72) #18 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',))), 38) #18 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev', purposes='enroll')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='probe', classes='impostor')), 34) #36 - 2

  # Eval group
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval')), 128) #32 users * 1 fingers * 4 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',))), 66) #32 users * 1 fingers * 2 acq + 2
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval', purposes='enroll')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='enroll')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='probe', classes='client')), 2)
  nose.tools.eq_(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='probe', classes='impostor')), 62) #64 - 2


@sql3_available
def test_objects_5():

  # tests if the right number of File objects is returned
  db = Database()

  # Protocol 'full'
  nose.tools.eq_(len(db.objects(protocol='full')), 1440) # 60 clients * 6 fingers per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev')), 1440) 
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', model_ids=('1_2_3',))), 1440)
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', purposes='enroll')), 1440)
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', model_ids=('1_2_3',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', model_ids=('1_2_3',), purposes='probe')), 1439)
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', purposes='probe', classes='impostor')), 1440)
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='full', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='impostor')), 1436) # 1440 total samples - 4 genuine samples


@sql3_available
def test_objects_6():

  # tests if the right number of File objects is returned
  db = Database()

  #####################################################
  # Protocol 'fullLeftRing'
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev')), 240) 
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', model_ids=('1_1_1',))), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', purposes='enroll')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', model_ids=('1_1_1',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', model_ids=('1_1_1',), purposes='probe')), 239)
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', purposes='probe', classes='impostor')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', model_ids=('1_1_1',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='fullLeftRing', groups='dev', model_ids=('1_1_1',), purposes='probe', classes='impostor')), 236) # 240 total samples - 4 genuine samples


  #####################################################
  # Protocol 'fullLeftMiddle'
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev')), 240) 
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', model_ids=('1_2_1',))), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', purposes='enroll')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', model_ids=('1_2_1',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', model_ids=('1_2_1',), purposes='probe')), 239)
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', purposes='probe', classes='impostor')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', model_ids=('1_2_1',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='fullLeftMiddle', groups='dev', model_ids=('1_2_1',), purposes='probe', classes='impostor')), 236) # 240 total samples - 4 genuine samples


  #####################################################
  # Protocol 'fullLeftIndex'
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev')), 240) 
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', model_ids=('1_3_1',))), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', purposes='enroll')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', model_ids=('1_3_1',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', model_ids=('1_3_1',), purposes='probe')), 239)
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', purposes='probe', classes='impostor')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', model_ids=('1_3_1',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='fullLeftIndex', groups='dev', model_ids=('1_3_1',), purposes='probe', classes='impostor')), 236) # 240 total samples - 4 genuine samples


@sql3_available
def test_objects_7():

  # tests if the right number of File objects is returned
  db = Database()

  #####################################################
  # Protocol 'fullRightIndex'
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev')), 240) 
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', model_ids=('1_4_1',))), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', purposes='enroll')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', model_ids=('1_4_1',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', model_ids=('1_4_1',), purposes='probe')), 239)
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', purposes='probe', classes='impostor')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', model_ids=('1_4_1',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='fullRightIndex', groups='dev', model_ids=('1_4_1',), purposes='probe', classes='impostor')), 236) # 240 total samples - 4 genuine samples


  #####################################################
  # Protocol 'fullRightMiddle'
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev')), 240) 
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', model_ids=('1_5_1',))), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', purposes='enroll')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', model_ids=('1_5_1',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', model_ids=('1_5_1',), purposes='probe')), 239)
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', purposes='probe', classes='impostor')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', model_ids=('1_5_1',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='fullRightMiddle', groups='dev', model_ids=('1_5_1',), purposes='probe', classes='impostor')), 236) # 240 total samples - 4 genuine samples


  #####################################################
  # Protocol 'fullRightRing'
  nose.tools.eq_(len(db.objects(protocol='fullRightRing')), 240) # 60 clients * 1 finger per client * 4 samples per finger

  # Dev group
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev')), 240) 
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', model_ids=('1_6_1',))), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', purposes='enroll')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', model_ids=('1_6_1',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', model_ids=('1_6_1',), purposes='probe')), 239)
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', purposes='probe', classes='impostor')), 240)
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', model_ids=('1_6_1',), purposes='probe', classes='client')), 3) # 3 genuine comparisons per sample
  nose.tools.eq_(len(db.objects(protocol='fullRightRing', groups='dev', model_ids=('1_6_1',), purposes='probe', classes='impostor')), 236) # 240 total samples - 4 genuine samples


@sql3_available
def test_driver_api():

  from bob.db.base.script.dbmanage import main

  nose.tools.eq_(main('utfvp dumplist --self-test'.split()), 0)
  nose.tools.eq_(main('utfvp dumplist --protocol=1vsall --class=client --group=dev --purpose=enroll --model=1_2_3 --self-test'.split()), 0)
  nose.tools.eq_(main('utfvp checkfiles --self-test'.split()), 0)


@sql3_available
@db_available
def test_load():

  db = Database()

  for f in db.objects():

    # loads an image from the database
    image = f.load(DATABASE_PATH)
    assert isinstance(image, numpy.ndarray)
    nose.tools.eq_(len(image.shape), 2) #it is a 2D array
    nose.tools.eq_(image.dtype, numpy.uint8)

