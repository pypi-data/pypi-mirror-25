#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""This module provides the Dataset interface allowing the user to query the
UTFVP database in the most obvious ways.
"""

import os
import six
from bob.db.base import utils
from .models import *
from .driver import Interface

import bob.db.base

SQLITE_FILE = Interface().files()[0]


class Database(bob.db.base.SQLiteDatabase):
  """The dataset class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self, original_directory=None, original_extension=None):
    bob.db.base.SQLiteDatabase.__init__(
        self, SQLITE_FILE, File, original_directory, original_extension)

  def groups(self, protocol=None):
    """Returns the names of all registered groups"""

    if protocol == '1vsall':
      return ('world', 'dev')
    elif protocol == 'full' or protocol == 'fullLeftRing' or protocol == 'fullLeftMiddle' or protocol == 'fullLeftIndex' or protocol == 'fullRightIndex' or protocol == 'fullRightMiddle' or protocol == 'fullRightRing':
      return('dev')
    else:
      return ('world', 'dev', 'eval')

  def clients(self, protocol=None, groups=None):
    """Returns a set of clients for the specific query by the user.


    Parameters:

      protocol (:py:class:`str`, optional): One of the UTFVP protocols:

        * ``1vsall``
        * ``nom``
        * ``nomLeftRing``
        * ``nomLeftMiddle``
        * ``nomLeftIndex``
        * ``nomRightIndex``
        * ``nomRightMiddle``
        * ``nomRightRing``
	      * ``full``
        * ``fullLeftRing``
        * ``fullLeftMiddle``
        * ``fullLeftIndex``
        * ``fullRightIndex``
        * ``fullRightMiddle``
        * ``fullRightRing``

      groups (:py:class:`str`, Optional): ignored (The clients belong both to
        ``world`` and ``dev``)


    Returns

      list: Containing all the clients which have the given properties.

    """

    protocols = self.check_parameters_for_validity(
        protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())

    retval = []
    # List of the clients
    if 'world' in groups:
      q = self.query(Client).join((File, Client.files)).join(
          (Protocol, File.protocols_train)).filter(Protocol.name.in_(protocols))
      q = q.order_by(Client.id)
      retval += list(q)

    if 'dev' in groups or 'eval' in groups:
      q = self.query(Client).join((Model, Client.models)).join(
          (Protocol, Model.protocol)).filter(Protocol.name.in_(protocols))
      q = q.filter(Model.sgroup.in_(groups))
      q = q.order_by(Client.id)
      retval += list(q)

    if len(protocols) == len(self.protocols()):
      retval = list(self.query(Client))

    return retval

  def client_ids(self, protocol=None, groups=None):
    """Returns a set of client ids for the specific query by the user.


    Parameters:

      protocol (:py:class:`str`, optional): One of the UTFVP protocols:

        * ``1vsall``
        * ``nom``
        * ``nomLeftRing``
        * ``nomLeftMiddle``
        * ``nomLeftIndex``
        * ``nomRightIndex``
        * ``nomRightMiddle``
        * ``nomRightRing``
	      * ``full``
        * ``fullLeftRing``
        * ``fullLeftMiddle``
        * ``fullLeftIndex``
        * ``fullRightIndex``
        * ``fullRightMiddle``
        * ``fullRightRing``

      groups (:py:class:`str`, optional): Groups the clients belong to. Should
        be one of:

        * ``world``
        * ``dev``
        * ``eval``

    Returns:

      list: Containing all the clients which have the given properties.

    """

    return [client.id for client in self.clients(protocol, groups)]

  def models(self, protocol=None, groups=None):
    """Returns a set of models for the specific query by the user.

    Parameters:

      protocol (:py:class:`str`, optional): One of the UTFVP protocols:

        * ``1vsall``
        * ``nom``
        * ``nomLeftRing``
        * ``nomLeftMiddle``
        * ``nomLeftIndex``
        * ``nomRightIndex``
        * ``nomRightMiddle``
        * ``nomRightRing``
	      * ``full``
        * ``fullLeftRing``
        * ``fullLeftMiddle``
        * ``fullLeftIndex``
        * ``fullRightIndex``
        * ``fullRightMiddle``
        * ``fullRightRing``

      groups (:py:class:`str`, optional): Groups the clients belong to. Should
        be one of:

        * ``dev``
        * ``eval``


    Returns:

      list: containing all the models which have the given properties

    """

    protocols = self.check_parameters_for_validity(
        protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())

    retval = []
    if 'dev' in groups or 'eval' in groups:
      # List of the clients
      q = self.query(Model).join((Protocol, Model.protocol)
                                 ).filter(Protocol.name.in_(protocols))
      q = q.filter(Model.sgroup.in_(groups)).order_by(Model.name)
      retval += list(q)

    return retval

  def model_ids(self, protocol=None, groups=None):
    """Returns a set of models ids for the specific query by the user.


    Parameters:

      protocol (:py:class:`str`, optional): One of the UTFVP protocols:

        * ``1vsall``
        * ``nom``
        * ``nomLeftRing``
        * ``nomLeftMiddle``
        * ``nomLeftIndex``
        * ``nomRightIndex``
        * ``nomRightMiddle``
        * ``nomRightRing``
	      * ``full``
        * ``fullLeftRing``
        * ``fullLeftMiddle``
        * ``fullLeftIndex``
        * ``fullRightIndex``
        * ``fullRightMiddle``
        * ``fullRightRing``

      groups (:py:class:`str`, optional): Groups the clients belong to. Should
        be one of:

        * ``world``
        * ``dev``
        * ``eval``

    Returns:

      list: Containing all the models ids which have the given properties.

    """

    return [model.name for model in self.models(protocol, groups)]

  def has_client_id(self, id):
    """Returns True if we have a client with a certain integer identifier"""

    return self.query(Client).filter(Client.id == id).count() != 0

  def client(self, id):
    """Returns the client object in the database given a certain id. Raises
    an error if that does not exist."""

    return self.query(Client).filter(Client.id == id).one()

  def get_client_id_from_model_id(self, model_id):
    """Returns the client_id attached to the given model_id

    Parameters:

      model_id (str): The model_id to consider


    Returns:

      str: The client_id attached to the given model_id

    """

    return self.query(Model).filter(Model.name == model_id).first().client_id

  def objects(self, protocol=None, purposes=None, model_ids=None, groups=None,
              classes=None, finger_ids=None, session_ids=None):
    """Returns a set of Files for the specific query by the user.


    Parameters:

      protocol (:py:class:`str`, :py:class:`list`, optional): One or several
        of:

        * ``1vsall``
        * ``nom``
        * ``nomLeftRing``
        * ``nomLeftMiddle``
        * ``nomLeftIndex``
        * ``nomRightIndex``
        * ``nomRightMiddle``
        * ``nomRightRing``
	      * ``full``
        * ``fullLeftRing``
        * ``fullLeftMiddle``
        * ``fullLeftIndex``
        * ``fullRightIndex``
        * ``fullRightMiddle``
        * ``fullRightRing``

      purposes (:py:class:`str`, :py:class:`list`, optional): One or several
        of:

        * ``train``
        * ``enroll``
        * ``probe``

      model_ids (:py:class:`str`, :py:class:`list`, optional): Only retrieves
        the files for the provided list of model ids. If ``None`` is given
        (this is the default), no filter over the model_ids is performed.

      groups (:py:class:`str`, :py:class:`list`, optional): Groups the clients
        belong to. Should be one or several of:

        * ``world``
        * ``dev``
        * ``eval``

      classes (:py:class:`str`, :py:class:`list`, optional): The classes (types
        of accesses) to be retrieved (``client`` or ``impostor``) or a tuple
        with several of them.  If ``None`` is given (this is the default), it
        is considered the same as a tuple with all possible values.

      finger_ids (:py:class:`str`, :py:class:`list`, optional): Only retrieves
        the files for the provided list of finger ids.  If ``None`` is given
        (this is the default), no filter over the finger_ids is performed.

      session_ids (:py:class:`str`, :py:class:`list`, optional): Only retrieves
        the files for the provided list of session ids. If ``None`` is given
        (this is the default), no filter over the session_ids is performed.


    Returns:

      list: Containing the files which have the given properties.

    """

    protocols = self.check_parameters_for_validity(
        protocol, "protocol", self.protocol_names())
    purposes = self.check_parameters_for_validity(
        purposes, "purpose", self.purposes())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    classes = self.check_parameters_for_validity(
        classes, "class", ('client', 'impostor'))

    from six import string_types
    if model_ids is None:
      model_ids = ()
    elif isinstance(model_ids, string_types):
      model_ids = (model_ids,)
    import collections
    if finger_ids is None:
      finger_ids = ()
    elif not isinstance(finger_ids, collections.Iterable):
      finger_ids = (finger_ids,)
    if session_ids is None:
      session_ids = ()
    elif not isinstance(session_ids, collections.Iterable):
      session_ids = (session_ids,)

    # Now query the database
    retval = []
    if 'world' in groups:
      q = self.query(File).join((Protocol, File.protocols_train)).\
          filter(Protocol.name.in_(protocols))
      if finger_ids:
        q = q.filter(File.finger_id.in_(finger_ids))
      if session_ids:
        q = q.filter(File.session_id.in_(session_ids))
      q = q.order_by(File.client_id, File.finger_id, File.session_id)
      retval += list(q)

    if 'dev' in groups or 'eval' in groups:
      sgroups = []
      if 'dev' in groups:
        sgroups.append('dev')
      if 'eval' in groups:
        sgroups.append('eval')
      if 'enroll' in purposes:
        q = self.query(File).join(Client).join((Model, File.models_enroll)).join((Protocol, Model.protocol)).\
            filter(and_(Protocol.name.in_(protocols), Model.sgroup.in_(sgroups)))
        if model_ids:
          q = q.filter(Model.name.in_(model_ids))
        if finger_ids:
          q = q.filter(File.finger_id.in_(finger_ids))
        if session_ids:
          q = q.filter(File.session_id.in_(session_ids))
        q = q.order_by(File.client_id, File.finger_id, File.session_id)
        retval += list(q)

      if 'probe' in purposes:
        if 'client' in classes:
          q = self.query(File).join(Client).join((Model, File.models_probe)).join((Protocol, Model.protocol)).\
              filter(and_(Protocol.name.in_(protocols), Model.sgroup.in_(
                  sgroups), File.client_id == Model.client_id))
          if model_ids:
            q = q.filter(Model.name.in_(model_ids))
          if finger_ids:
            q = q.filter(File.finger_id.in_(finger_ids))
          if session_ids:
            q = q.filter(File.session_id.in_(session_ids))
          q = q.order_by(File.client_id, File.finger_id, File.session_id)
          retval += list(q)

        if 'impostor' in classes:
          q = self.query(File).join(Client).join((Model, File.models_probe)).join((Protocol, Model.protocol)).\
              filter(and_(Protocol.name.in_(protocols), Model.sgroup.in_(
                  sgroups), File.client_id != Model.client_id))
          if len(model_ids) != 0:
            q = q.filter(Model.name.in_(model_ids))
          if finger_ids:
            q = q.filter(File.finger_id.in_(finger_ids))
          if session_ids:
            q = q.filter(File.session_id.in_(session_ids))
          q = q.order_by(File.client_id, File.finger_id, File.session_id)
          retval += list(q)

    return list(set(retval))  # To remove duplicates

  def protocol_names(self):
    """Returns all registered protocol names"""

    l = self.protocols()
    retval = [str(k.name) for k in l]
    return retval

  def protocols(self):
    """Returns all registered protocols"""

    return list(self.query(Protocol))

  def has_protocol(self, name):
    """Tells if a certain protocol is available"""

    return self.query(Protocol).filter(Protocol.name == name).count() != 0

  def protocol(self, name):
    """Returns the protocol object in the database given a certain name. Raises
    an error if that does not exist."""

    return self.query(Protocol).filter(Protocol.name == name).one()

  def purposes(self):
    return ('train', 'enroll', 'probe')

