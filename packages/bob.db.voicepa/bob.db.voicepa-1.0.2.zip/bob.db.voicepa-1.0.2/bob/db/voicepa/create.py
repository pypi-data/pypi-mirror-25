#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu 6 Oct 21:43:22 2016

"""This script creates the AVSpoof database in a single pass.
"""

from __future__ import print_function

import glob

from .models import *


def add_clients(session, protodir, verbose):
    """Add clients to the voicepa database."""

    for client in open(os.path.join(protodir, 'clients-grandtest.txt'), 'rt'):
        splitline = client.strip().split(' ', 2)
        if not splitline: continue  # empty line
        id = int(splitline[0][1:])
        set = splitline[1]
        gender = 'female' if splitline[0][0] == 'f' else 'male'
        if verbose: print("Adding client %d, %s into '%s' set..." % (id, gender, set))
        session.add(Client(id, gender, set))
        session.flush()


def add_file(session, protocol, path, group, client_id, gender, recording_device, sess, speech,
             attack_data, attack_device, purpose, asv_device, environment):
    # if purpose == 'genuine':  # make sure we correctly set purpose in database
    #     purpose = 'real'
    db_client = session.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        db_client = Client(client_id, gender, group)
        session.add(db_client)

    db_file = session.query(File).filter(File.path == path).first()
    if db_file is None:
        db_file = File(db_client, path, recording_device, sess, speech, attack_data,
                       attack_device, asv_device, environment, purpose)
        session.add(db_file)

    # add find the correct protocol
    db_protocol = session.query(Protocol).filter(Protocol.name == protocol).first()
    if db_protocol is None:
        raise ValueError("Protocol %s should have been created before adding files to the database!" % (protocol))

    # link file and the protocol
    session.add(ProtocolFiles(db_protocol, db_file))


def add_protocol_samples(session, protodir, filename, protocol, group, purpose):
    recording_device_map = {'laptop': 'laptop', 'phone2': 'iphone3gs', 'phone1': 'samsungs3'}

    def parse_real_path(splitline):
        """Parses the RCD filename and break it in the relevant chunks."""

        client_id = int(splitline[2][1:])
        gender = splitline[1]
        sess = splitline[3]  # recording session
        recording_device = recording_device_map[splitline[4]]
        speech = splitline[5]
        return client_id, gender, recording_device, sess, speech

    def parse_attack_path(splitline):
        """Parses the RAD filename and break it in the relevant chunks."""

        # parse the line
        attack_parts = splitline[1].split('-')
        environment = attack_parts[0]
        asv_device = attack_parts[1]
        attack_data = attack_parts[2]
        attack_device = attack_parts[3]

        client_id = int(splitline[3][1:])
        gender = splitline[2]
        # speech synthesis is strangely generated, diff from all other files
        if attack_data == "ss":
            sstr = splitline[4].split('_')
            if "Sess" in sstr[1]:  # the string is Session#
                speech = "read"
                sess = "sess" + sstr[1][-1]
            elif "Pass" in sstr[1]:
                speech = "pass"
                sess = "sess2"  # it's not specified in the file name, so assume 2
            else:
                speech = "free"
                sess = "sess2"
            recording_device = "laptop"  # speech synthesis is from laptop data
        else:  # all the rest of the attacks
            sess = splitline[4]  # recording session
            # print (splitline)
            recording_device = recording_device_map[splitline[5]]
            speech = splitline[6]
        return client_id, gender, recording_device, sess, speech, attack_data, attack_device, asv_device, environment

    # read and add file to the database
    with open(os.path.join(protodir, filename)) as f:
        lines = f.readlines()

    for line in lines:
        # each line is a relative sample path, which contains all necessary information
        splitline = line.strip().split('/')
        if purpose == 'attack':
            client_id, gender, recording_device, sess, speech, attack_data, attack_device, asv_device, environment = \
                parse_attack_path(splitline)
        elif purpose == 'real':
            client_id, gender, recording_device, sess, speech = parse_real_path(splitline)
            attack_data = 'undefined'
            attack_device = 'undefined'
            asv_device = 'undefined'
            environment = 'undefined'
        else:
            raise ValueError("Incorrect purpose '%s' in file %s. Only 'attack' or 'real' purposes are accepted." %
                             (purpose, filename))

        # all the lines have the same format
        add_file(session, protocol, line.strip(), group, client_id, gender, recording_device,
                 sess, speech, attack_data, attack_device, purpose, asv_device, environment)


def init_database(session, protodir, protocol_file_list):
    """Defines all available protocols"""

    for filename in protocol_file_list:
        # skip hidden files
        # if filename.startswith('.'):
        #     continue
        # skip directories
        # if os.path.isdir(os.path.join(protodir, filename)):
        #     continue

        # a sample file name looks like this: attack-grandtest-allsupports-test.txt
        print("Processing file %s" % filename)
        # remove extension
        fname = os.path.splitext(os.path.basename(filename.strip()))[0]
        # parse the name
        splitline = fname.split('-')
        print("Basename %s" % fname)

        group = splitline[2]  # train, dev, or eval
        protocol = splitline[1]
        purpose = splitline[0]  # real or attack

        # add protocol only if it does not exist
        db_protocol = session.query(Protocol).filter(Protocol.name == protocol).first()
        if db_protocol is None:
            session.add(Protocol(protocol))
            session.flush()
        # add samples from the protocol file to the database
        add_protocol_samples(session, protodir, filename, protocol, group, purpose)


def create_tables(args):
    """Creates all necessary tables (only to be used at the first time)"""

    from bob.db.base.utils import create_engine_try_nolock

    engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))
    Client.metadata.create_all(engine)
    File.metadata.create_all(engine)
    Protocol.metadata.create_all(engine)
    ProtocolFiles.metadata.create_all(engine)


# Driver API
# ==========

def create(args):
    """Creates or re-creates this database"""

    # untar the protocol files first
    from pkg_resources import resource_filename
    if not args.prototar:
        args.prototar = resource_filename(__name__, 'protocols.tar.gz')

    import tarfile
    opener, mode = tarfile.open, 'r:gz'
    args.protodir = os.path.dirname(os.path.realpath(args.prototar))
    try:
        tar = opener(args.prototar, mode)
        try:
            tar.extractall(path=args.protodir)
        finally:
            tar.close()
    finally:
        # we assume that tarball with protocols is uncompressed into 'protocols' folder
        args.protodir = os.path.join(args.protodir, 'protocols')

    print (args.protodir)
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

    s = session_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))
    add_clients(s, args.protodir, args.verbose)

    # protocol files
    protocol_file_list = glob.glob(os.path.join(args.protodir, '*-*-*'))
    init_database(s, args.protodir, protocol_file_list)

    s.commit()
    s.close()

    # clean up protocols directory
    import shutil
    shutil.rmtree(args.protodir)

    return 0


def add_command(subparsers):
    """Add specific subcommands that the action "create" can use"""

    parser = subparsers.add_parser('create', help=create.__doc__)

    parser.add_argument('-R', '--recreate', action='store_true', default=False,
                        help="If set, I'll first erase the current database")
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Do SQL operations in a verbose way")
    # pavel - for now, store protocols in the same package
    parser.add_argument('-D', '--prototar', action='store',
                        default=None,
                        metavar='DIR',
                        help="Path to the tarball with all the protocols of voicePA database (defaults to %(default)s)")

    parser.set_defaults(func=create)  # action
