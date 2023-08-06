#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""A few checks at the VERA Fingervein database.
"""

import os
import numpy

from . import Database

import nose.tools
from nose.plugins.skip import SkipTest

# base directories where the VERA files sit
DATABASE_PATH = "/idiap/project/vera/databases/VERA-fingervein"


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
      raise SkipTest("The interface SQL file (%s) is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'vera'))

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
def test_counts():

  # test whether the correct number of clients is returned
  db = Database()

  nose.tools.eq_(db.groups(), ('train', 'dev'))

  protocols = db.protocol_names()
  nose.tools.eq_(len(protocols), 4)
  assert 'Nom' in protocols
  assert 'Full' in protocols
  assert 'Fifty' in protocols
  assert 'B' in protocols

  nose.tools.eq_(db.purposes(), ('train', 'enroll', 'probe'))
  nose.tools.eq_(db.genders(), ('M', 'F'))
  nose.tools.eq_(db.sides(), ('L', 'R'))

  # test model ids
  model_ids = db.model_ids()
  nose.tools.eq_(len(model_ids), 440)

  model_ids = db.model_ids(protocol='Nom')
  nose.tools.eq_(len(model_ids), 220)

  model_ids = db.model_ids(protocol='Fifty')
  nose.tools.eq_(len(model_ids), 100)

  model_ids = db.model_ids(protocol='B')
  nose.tools.eq_(len(model_ids), 216)

  model_ids = db.model_ids(protocol='Full')
  nose.tools.eq_(len(model_ids), 440)

  # test database sizes
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='train')), 0)
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='dev')), 440)
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='dev',
    purposes='enroll')), 220)
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='dev',
    purposes='probe')), 220)

  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='train')), 240)
  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='dev')), 200)
  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='dev',
    purposes='enroll')), 100)
  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='dev',
    purposes='probe')), 100)

  nose.tools.eq_(len(db.objects(protocol='B', groups='train')), 224)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev')), 216)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev',
    purposes='enroll')), 216)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev',
    purposes='probe')), 216)

  nose.tools.eq_(len(db.objects(protocol='Full', groups='train')), 0)
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev')), 440)
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='enroll')), 440)
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='probe')), 440)

  # make sure that we can filter by model ids
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='enroll', model_ids=model_ids[:10])), 10)

  # filtering by model ids on probes, returns all
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='probe', model_ids=model_ids[0])), 440)


@sql3_available
def test_driver_api():

  from bob.db.base.script.dbmanage import main

  nose.tools.eq_(main('verafinger dumplist --self-test'.split()), 0)
  nose.tools.eq_(main('verafinger dumplist --protocol=Full --group=dev --purpose=enroll --model=101_L_1 --self-test'.split()), 0)
  nose.tools.eq_(main('verafinger checkfiles --self-test'.split()), 0)


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


@sql3_available
@db_available
def test_annotations():

  db = Database()

  for f in db.objects():

    # loads an image from the database
    image = f.load(DATABASE_PATH)

    roi = f.roi()
    assert isinstance(roi, numpy.ndarray)
    nose.tools.eq_(len(roi.shape), 2) #it is a 2D array
    nose.tools.eq_(roi.shape[1], 2) #two columns
    nose.tools.eq_(roi.dtype, numpy.uint16)
    assert len(roi) > 10 #at least 10 points

    # ensures all annotation points are within image boundary
    Y,X = image.shape
    for y,x in roi:
      assert y < Y, 'Annotation (%d, %d) for %s surpasses the image size (%d, %d)' % (y, x, f.path, Y, X)
      assert x < X, 'Annotation (%d, %d) for %s surpasses the image size (%d, %d)' % (y, x, f.path, Y, X)


@sql3_available
def test_model_id_to_finger_name_conversion():

  db = Database()

  for f in db.objects():

    assert len(db.finger_name_from_model_id(f.model_id)) == 5
