#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""This script creates the VERA fingervein SQL database in a single pass.
"""

import os
import re
import csv
import pkg_resources

from .models import *


def add_clients(session, verbose):
  """Create client entries at the database"""

  metadata = pkg_resources.resource_filename(__name__, os.path.join('data',
    'metadata.csv'))
  with open(metadata, 'rt') as f:
    header = None
    for row in csv.reader(f):
      if header is None:
        header = row
        continue
      id_, gender, age = row
      id_ = int(id_)
      age = int(age)

      # create client
      client = Client(id_, gender, age)
      session.add(client)

      if verbose:
        print("Created %s" % client)


def add_fingers(session, verbose):
  """Create finger entries at the database"""

  for client in session.query(Client):
    for side in Finger.side_choices:
      finger = Finger(client, side)
      session.add(finger)

      if verbose:
        print("Created %s" % finger)


def add_files(db_session, verbose):
  """Create file entries at the database"""

  for finger in db_session.query(Finger):
    for session in File.session_choices:
      file_ = File(finger, session)
      db_session.add(file_)

      if verbose:
        print("Created %s" % file_)


def retrieve_file(session, ref):
  """Retrieves the given File object from a full path"""

  bits = re.split(r'[-_/]', ref)
  # here is the outcome of this split:
  # [0] client-id
  # [1] gender (F or M)
  # [2] client-id
  # [3] side (L or R)
  # [4] session (1 or 2)
  return session.query(File).join(Finger,Client).filter(
    File.session==bits[4],
    Client.id==int(bits[0]),
    Finger.side==bits[3],
    ).one()


def add_protocols(session, verbose):
  """Create protocol entries at the database"""

  protocol_dir = pkg_resources.resource_filename(__name__, os.path.join('data',
    'protocols'))
  for name in os.listdir(protocol_dir):
    protocol = Protocol(name)
    session.add(protocol)
    if verbose:
      print("Created %s" % protocol)

    # training data
    train_filename = os.path.join(protocol_dir, name, 'train.txt')
    subset = Subset(protocol, 'train', 'train')
    session.add(subset)
    if verbose:
      print("Created %s" % subset)
    with open(train_filename, 'rt') as f:
      for row in f:
        filename_ref, finger_ref = row.split()
        file_ = retrieve_file(session, filename_ref)
        subset.files.append(file_)
        if verbose:
          print("Added %s to %s" % (file_, subset))

    # enrollment data
    models_filename = os.path.join(protocol_dir, name, 'models.txt')
    subset = Subset(protocol, 'dev', 'enroll')
    session.add(subset)
    if verbose:
      print("Created %s" % subset)
    with open(models_filename, 'rt') as f:
      for row in f:
        filename_ref, model_ref, finger_ref = row.split()
        file_ = retrieve_file(session, filename_ref)
        subset.files.append(file_)
        if verbose:
          print("Added %s to %s" % (file_, subset))

    # probing data
    probes_filename = os.path.join(protocol_dir, name, 'probes.txt')
    subset = Subset(protocol, 'dev', 'probe')
    session.add(subset)
    if verbose:
      print("Created %s" % subset)
    with open(probes_filename, 'rt') as f:
      for row in f:
        filename_ref, model_ref = row.split()
        file_ = retrieve_file(session, filename_ref)
        subset.files.append(file_)
        if verbose:
          print("Added %s to %s" % (file_, subset))



def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  echo = args.verbose > 2 if args.verbose else False
  engine = create_engine_try_nolock(args.type, args.files[0], echo=echo)
  Base.metadata.create_all(engine)


def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  echo = args.verbose > 2 if args.verbose else False
  s = session_try_nolock(args.type, args.files[0], echo=echo)
  add_clients(s, args.verbose)
  add_fingers(s, args.verbose)
  add_files(s, args.verbose)
  add_protocols(s, args.verbose)
  s.commit()
  s.close()


def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true',
    help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count',
    help='Do SQL operations in a verbose way')

  parser.set_defaults(func=create) #action
