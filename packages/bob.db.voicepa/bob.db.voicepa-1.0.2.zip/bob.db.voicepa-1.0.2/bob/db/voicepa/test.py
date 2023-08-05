#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu 6 Oct 21:43:22 2016
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the voicepa attack database.
"""

import unittest
from .query import Database
from .models import *

def db_available(test):
    """Decorator for detecting if OpenCV/Python bindings are available"""
    from bob.io.base.test_utils import datafile
    from nose.plugins.skip import SkipTest
    import functools

    @functools.wraps(test)
    def wrapper(*args, **kwargs):
        dbfile = datafile("db.sql3", __name__, None)
        if os.path.exists(dbfile):
            return test(*args, **kwargs)
        else:
            raise SkipTest(
                "The database file '%s' is not available; did you forget to run 'bob_dbmanage.py %s create' ?" %
                (dbfile, 'voicepa'))

    return wrapper


class VoicePADatabaseTest(unittest.TestCase):
    """Performs various tests on the voicePA attack database."""

    @db_available
    def queryGroupsProtocolsTypes(self, protocol, cls, Ntrain, Ndev, Neval):

        db = Database()
        f = db.objects(cls=cls, protocol=protocol)

        self.assertEqual(len(f), Ntrain+Ndev+Neval)
        for k in f[:10]:  # only the 10 first...
            if cls == 'attack':
                attack_name = k.get_attack()
                self.assertNotEqual(attack_name, 'undefined-undefined-undefined-undefined')
                self.assertTrue(k.is_attack())
            else:
                self.assertTrue(k.is_real())

        train = db.objects(cls=cls, groups='train', protocol=protocol)
        self.assertEqual(len(train), Ntrain)

        dev = db.objects(cls=cls, groups='dev', protocol=protocol)
        self.assertEqual(len(dev), Ndev)

        eval = db.objects(cls=cls, groups='eval', protocol=protocol)
        self.assertEqual(len(eval), Neval)

        # tests train, dev, and test files are distinct
        s = set(train + dev + eval)
        self.assertEqual(len(s), Ntrain+Ndev+Neval)

    @db_available
    def test01_queryRealGrandtest(self):
        self.queryGroupsProtocolsTypes('grandtest',  'real', 4973, 4995, 5576)

    def test02_queryRealSmalltest(self):
        self.queryGroupsProtocolsTypes('smalltest',  'real', 395, 345, 339)

    @db_available
    def test03_queryAttacksGrandtest(self):
        self.queryGroupsProtocolsTypes('grandtest', 'attack', 115730, 115740, 129988)

    @db_available
    def test04_queryAttacksSmalltest(self):
        self.queryGroupsProtocolsTypes('smalltest', 'attack', 9810, 9810, 9810)

    @db_available
    def test05_queryRealAvspoofPA(self):
        self.queryGroupsProtocolsTypes('avspoofPA',  'real', 4973, 4995, 5576)

    @db_available
    def test06_queryRealMobile(self):
        self.queryGroupsProtocolsTypes('mobile',  'real', 4973, 4995, 5576)

    @db_available
    def test07_queryAttacksAvspoofPA(self):
        self.queryGroupsProtocolsTypes('avspoofPA',  'attack', 38580, 38580, 43320)

    @db_available
    def test08_queryRealMobile(self):
        self.queryGroupsProtocolsTypes('mobile',  'attack', 77150, 77160, 86668)


    @db_available
    def queryEnrollments(self, protocol, N):

        db = Database()
        f = db.objects(cls='enroll', protocol=protocol)
        self.assertEqual(len(f), N)
        for k in f[:10]:  # only the 10 first...
            self.assertTrue(k.is_real())

    @db_available
    def test09_queryEnrollmentsGrandtest(self):
        self.queryEnrollments('grandtest', 2418)

    @db_available
    def test10_queryEnrollmentsAvspoofPA(self):
        self.queryEnrollments('avspoofPA', 2418)

    @db_available
    def test11_queryEnrollmentsMobile(self):
        self.queryEnrollments('mobile', 2418)

    @db_available
    def test12_queryEnrollmentsSmalltest(self):
        self.queryEnrollments('smalltest', 164)

    @db_available
    def test13_queryClients(self):

        db = Database()
        f = db.clients()
        self.assertEqual(len(f), 44)  # 44 clients
        self.assertTrue(db.has_client_id(3))
        self.assertFalse(db.has_client_id(0))
        self.assertTrue(db.has_client_id(21))
        self.assertFalse(db.has_client_id(45))
        self.assertFalse(db.has_client_id(100))
        self.assertTrue(db.has_client_id(18))

        f = db.clients(gender='male')
        self.assertEqual(len(f), 31)  # 31 male clients
        clients = []
        for c in f:
            clients.append(c.id)
        self.assertIn(1, clients)
        self.assertNotIn(3, clients)
        self.assertIn(30, clients)
        self.assertNotIn(43, clients)

        f = db.clients(gender='female')
        self.assertEqual(len(f), 13)  # 13 female clients
        clients = []
        for c in f:
            clients.append(c.id)
        self.assertNotIn(1, clients)
        self.assertIn(3, clients)
        self.assertNotIn(30, clients)
        self.assertIn(43, clients)

    @db_available
    def test14_queryAudioFile(self):

        db = Database()
        o = db.objects(clients=(1,))[0]
        o.audiofile()

    @db_available
    def test15_manage_files(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('voicepa files'.split()), 0)

    @db_available
    def test16_manage_dumplist_1(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('voicepa dumplist --self-test'.split()), 0)

    @db_available
    def test17_manage_dumplist_2(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main(
            'voicepa dumplist --class=attack --group=dev --protocol=grandtest --self-test'.split()), 0)

    @db_available
    def test18_manage_dumplist_client(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('voicepa dumplist --client=23 --self-test'.split()), 0)

    @db_available
    def test19_manage_checkfiles(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('voicepa checkfiles --self-test'.split()), 0)

    # attack_data_choices = ('undefined', 'laptop', 'iphone3gs', 'samsungs3', 'ss', 'vc')
    # """Types of attacks data, i.e., what medium was used to create the attacks"""
    #
    # attack_device_choices = ('undefined', 'laptop', 'hqspeaker', 'iphone3gs', 'samsungs3', 'iphone6s')
    # """Types of devices that used to playback the attack data"""

    @db_available
    def queryAttackType(self, protocol, attack_data, attack_device, N, environment=None):

        db = Database()
        f = db.objects(cls='attack', attack_data=attack_data, attack_devices=attack_device,
                       protocol=protocol, environments=environment)
        self.assertEqual(len(f), N)
        for k in f[:10]:  # only the 10 first...
            if attack_data:
                self.assertEqual(attack_data, k.attack_data)
            if attack_device:
                self.assertEqual(attack_device, k.attack_device)

    @db_available
    def test20_queryiphone3gsAttacks(self):
        self.queryAttackType('grandtest', None, 'iphone3gs', 6600)

    @db_available
    def test21_queryiphone3gsAttacksMobile(self):
        self.queryAttackType('mobile', None, 'iphone3gs', 4400)

    @db_available
    def test22_queryiphone3gsAvspoofPA(self):
        self.queryAttackType('mobile', 'iphone3gs', None, 4400)

    @db_available
    def test23_queryiphone6s(self):
        self.queryAttackType('grandtest', None, 'iphone6s', 232160)

    @db_available
    def test24_querysyntheticVC(self):
        self.queryAttackType('synthetic', 'vc', None, 325800)

    @db_available
    def test25_querysyntheticVCLaptop(self):
        self.queryAttackType('synthetic', 'vc', 'laptop', 54300)

    @db_available
    def test26_querygrandtestHQspeaker(self):
        self.queryAttackType('grandtest', None, 'hqspeaker', 58040)

    @db_available
    def test27_queryiphone3gs(self):
        self.queryAttackType('avspoofPA', None, 'iphone3gs', 2200)

    @db_available
    def test28_querysamsungs3(self):
        self.queryAttackType('avspoofPA', None, 'samsungs3', 2200)

    @db_available
    def test29_queryAvspoofPALaptop(self):
        self.queryAttackType('avspoofPA', 'vc', 'laptop', 54300)

    @db_available
    def test30_queryAvspoofPAHQspeaker(self):
        self.queryAttackType('avspoofPA', 'ss', 'hqspeaker', 1540)

    @db_available
    def test32_queryAttacksMobile(self):
        self.queryAttackType('mobile', None, None, 240978)

    @db_available
    def test33_queryAttacksMobileLaptop(self):
        self.queryAttackType('mobile', 'laptop', None, 8800)

    @db_available
    def test34_queryAttacksMobileSS(self):
        self.queryAttackType('mobile', 'ss', None, 6160)

    @db_available
    def test35_queryAttacksMobileVC(self):
        self.queryAttackType('mobile', 'vc', 'iphone6s', 217200)

    @db_available
    def test36_queryAttacksReplay(self):
        self.queryAttackType('replay', None, None, 26418)

    @db_available
    def test37_queryAttacksReplayLaptop(self):
        self.queryAttackType('replay', 'laptop', None, 13200)

    @db_available
    def test38_queryAttacksiphone3gs(self):
        self.queryAttackType('iphone3gs', None, None, 120498)

    @db_available
    def test39_queryAttackssamsungs3(self):
        self.queryAttackType('samsungs3', None, None, 120480)

    @db_available
    def test40_queryAttacksr106(self):
        self.queryAttackType('r106', None, None, 120489)

    @db_available
    def test41_queryAttacksseboffice(self):
        self.queryAttackType('seboffice', None, None, 120489)

    @db_available
    def test42_queryAttacksMobiler106(self):
        self.queryAttackType('mobile', None, None, 120489, environment='r106')

    @db_available
    def test43_queryAttacksMobileseboffice(self):
        self.queryAttackType('mobile', None, None, 120489, environment='seboffice')

    @db_available
    def test44_queryAttacksGrandtestr107(self):
        self.queryAttackType('grandtest', None, None, 120480, environment='r107')

    @db_available
    def test45_queryAttacksavspoofPA(self):
        self.queryAttackType('avspoofPA', None, None, 120480)
