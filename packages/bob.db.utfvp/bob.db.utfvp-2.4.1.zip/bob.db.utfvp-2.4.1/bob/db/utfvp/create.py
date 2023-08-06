#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""This script creates the UTFVP database in a single pass.
"""

import os

from .models import *

def nodot(item):
  """Can be used to ignore hidden files, starting with the . character."""
  return item[0] != '.'

def add_files(session, imagedir, verbose):
  """Add files (and clients) to the UTFVP database."""

  def add_file(session, subdir, filename, client_dict, verbose):
    """Parse a single filename and add it to the list.
       Also add a client entry if not already in the database."""

    v = os.path.splitext(os.path.basename(filename))[0].split('_')
    subclient_id = int(v[0])
    finger_id = int(v[1])
    ### 1 = Left ring finger
    ### 2 = Left middle finger
    ### 3 = Left index finger
    ### 4 = Right index finger
    ### 5 = Right middle finger
    ### 6 = Right ring finger
    client_id = "%d_%d" % (subclient_id, finger_id)
    if not (client_id in client_dict):
      c = Client(client_id, subclient_id)
      session.add(c)
      session.flush()
      session.refresh(c)
      client_dict[client_id] = True
    session_id = int(v[2])
    base_path = os.path.join(subdir, os.path.basename(filename).split('.')[0])
    if verbose>1: print("  Adding file '%s'..." %(base_path, ))
    cfile = File(client_id, base_path, finger_id, session_id)
    session.add(cfile)
    session.flush()
    session.refresh(cfile)

    return cfile

  if verbose: print("Adding files...")
  subdir_list = list(filter(nodot, os.listdir(imagedir)))
  client_dict = {}
  file_list = []
  for subdir in subdir_list:
    filename_list = list(filter(nodot, os.listdir(os.path.join(imagedir, subdir))))
    for filename in filename_list:
      filename_, extension = os.path.splitext(filename)
      if extension == '.png':
        file_list.append(add_file(session, subdir, os.path.join(imagedir, filename), client_dict, verbose))

  return file_list

def add_protocols(session, file_list, verbose):
  """Adds protocols"""

  # 2. ADDITIONS TO THE SQL DATABASE
  protocol_list = ['1vsall', 'nom','nomLeftRing','nomLeftMiddle','nomLeftIndex','nomRightIndex','nomRightMiddle','nomRightRing', 'full', 'fullLeftRing', 'fullLeftMiddle', 'fullLeftIndex', 'fullRightIndex', 'fullRightMiddle', 'fullRightRing']
  for proto in protocol_list:
    p = Protocol(proto)
    # Add protocol
    if verbose: print("Adding protocol %s..." % (proto))
    session.add(p)
    session.flush()
    session.refresh(p)

    if proto == '1vsall':
      # Helper function 
      def isWorldFile(f_file):
        return f_file.client.subclient_id <= 35 and f_file.finger_id == ((f_file.client.subclient_id-1) % 6) + 1 # defines what it means for file to belong to "world" class

      model_dict = {} # dictionary of models
      for f_file in file_list: # for every file in the database
        if not isWorldFile(f_file): # if the file does not belong to the "world" class, then continue processing it
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)  # the ID of the model as personID_finger_ID_session_ID
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:  # if we haven't already stored the model in the model dictionary ...
            model = Model(model_id, f_file.client_id, 'dev')  # create a model for this particular file
            p.models.append(model)  # add the model to the list of models for this particular protocol
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list: # for every file in the database
              if f_pfile.id != f_file.id and not isWorldFile(f_pfile):  # if the file is not the same as the current model file and it is not in the "world" group ...
                model.probe_files.append(f_pfile) # add the file to the list of probe files for this particular model
                if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
            model_dict[model_id] = model # add this model to the model dictionary, indexed by its model id
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)  # add the enrollment files associated with this model
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()

        else:
          p.train_files.append(f_file)  # if the file is part of the "world" group then add it to the training set
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))


    if proto == 'nom':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))


    if proto == 'nomLeftRing':

      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 1)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 1)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 1)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 1)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        #import ipdb; ipdb.set_trace()
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 1:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))

    if proto == 'nomLeftMiddle':

      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 2)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 2)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 2)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 2)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 2:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))

    if proto == 'nomLeftIndex':

      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 3)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 3)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 3)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 3)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 3:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))

    if proto == 'nomRightIndex':

      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 4)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 4)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 4)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 4)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 4:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))


    if proto == 'nomRightMiddle':

      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 5)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 5)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 5)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 5)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 5:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))


    if proto == 'nomRightRing':

      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 6)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 6)

      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 6)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 6)

      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))

        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 6:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))


    if proto == 'full': # calculate match score between every client (model) and every probe (no training/world set)
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
        if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
        if not model_id in model_dict:
          model = Model(model_id, f_file.client_id, 'dev')
          p.models.append(model)
          session.add(model)
          session.flush()
          session.refresh(model)
          # Append probe files
          for f_pfile in file_list:
            if f_pfile.id != f_file.id:
              model.probe_files.append(f_pfile)
              if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
          model_dict[model_id] = model
        # Append enrollment file
        model_dict[model_id].enrollment_files.append(f_file)
        if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
        session.flush()


    if proto == 'fullLeftRing': # calculate match score between every client (model) and every probe (no training/world set) using only the Left Ring fingers
      model_dict = {}
      for f_file in file_list:
        if f_file.finger_id == 1: # ensures only Left Ring fingers are used
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.finger_id == 1:
                if f_pfile.id != f_file.id:
                  model.probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              elif f_pfile.finger_id != 1:
                continue
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()
        elif f_file.session_id != 1:
          continue


    if proto == 'fullLeftMiddle': # calculate match score between every client (model) and every probe (no training/world set) using only the Left Middle fingers
      model_dict = {}
      for f_file in file_list:
        if f_file.finger_id == 2: # ensures only Left Middle fingers are used
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.finger_id == 2:
                if f_pfile.id != f_file.id:
                  model.probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              elif f_pfile.finger_id != 2:
                continue
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()
        elif f_file.session_id != 2:
          continue


    if proto == 'fullLeftIndex': # calculate match score between every client (model) and every probe (no training/world set) using only the Left Index fingers
      model_dict = {}
      for f_file in file_list:
        if f_file.finger_id == 3: # ensures only Left Index fingers are used
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.finger_id == 3:
                if f_pfile.id != f_file.id:
                  model.probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              elif f_pfile.finger_id != 3:
                continue
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()
        elif f_file.session_id != 3:
          continue


    if proto == 'fullRightIndex': # calculate match score between every client (model) and every probe (no training/world set) using only the Right Index fingers
      model_dict = {}
      for f_file in file_list:
        if f_file.finger_id == 4: # ensures only Right Index fingers are used
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.finger_id == 4:
                if f_pfile.id != f_file.id:
                  model.probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              elif f_pfile.finger_id != 4:
                continue
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()
        elif f_file.session_id != 4:
          continue


    if proto == 'fullRightMiddle': # calculate match score between every client (model) and every probe (no training/world set) using only the Right Middle fingers
      model_dict = {}
      for f_file in file_list:
        if f_file.finger_id == 5: # ensures only Right Middle fingers are used
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.finger_id == 5:
                if f_pfile.id != f_file.id:
                  model.probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              elif f_pfile.finger_id != 5:
                continue
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()
        elif f_file.session_id != 5:
          continue


    if proto == 'fullRightRing': # calculate match score between every client (model) and every probe (no training/world set) using only the Right Ring fingers
      model_dict = {}
      for f_file in file_list:
        if f_file.finger_id == 6: # ensures only Right Ring fingers are used
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.finger_id == 6:
                if f_pfile.id != f_file.id:
                  model.probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              elif f_pfile.finger_id != 6:
                continue
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enroll'))
          session.flush()
        elif f_file.session_id != 6:
          continue


def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  Base.metadata.create_all(engine)

# Driver API
# ==========

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
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  file_list = add_files(s, args.imagedir, args.verbose)
  add_protocols(s, file_list, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way')
  parser.add_argument('-D', '--imagedir', metavar='DIR', default='/idiap/resource/database/UTFVP/data', help="Change the relative path to the directory containing the images of the UTFVP database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action

