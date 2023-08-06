# -*- coding: utf-8 -*- vim:fileencoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

# Copyright © 2010-2012 Greek Research and Technology Network (GRNET S.A.)
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHORS DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
'''
Unit tests for updates package
'''

from django.test.client import Client
from django.utils import unittest
from django.core.management import call_command

from puppet.models import Host, Resource, FactValue, Fact
from updates.models import Package, Update

# The following is an ugly hack for unit tests to work
# We force managed the unmanaged models so that tables will be created
Host._meta.managed = True
Resource._meta.managed = True
FactValue._meta.managed = True
Fact._meta.managed = True


class UpdatesTestCase(unittest.TestCase):
    '''
    A test case for updates app
    '''

    def setUp(self):
        '''
        Commands run before every test
        '''

        self.host1 = Host.objects.create(name='MyHost', ip='10.10.10.10')
        self.package1 = Package.objects.create(name='testpackage', sourcename='testsource')
        self.package2 = Package.objects.create(name='testpackage2', sourcename='testpackage2')
        self.update1 = Update.objects.create(
            package=self.package1, host=self.host1,
            installedVersion='1.1', candidateVersion='1.2',
            source='TestSource', origin='Debian')
        self.update2 = Update.objects.create(
            package=self.package2, host=self.host1,
            installedVersion='1.1', candidateVersion='1.2',
            source='TestSource', origin='Ubuntu')
        self.update3 = Update.objects.create(
            package=self.package2, host=self.host1,
            installedVersion='1.1', candidateVersion='1.2',
            source='TestSource', origin='None')

    def tearDown(self):
        '''
        Commands run after every test
        '''

        Host.objects.all().delete()
        Package.objects.all().delete()
        Update.objects.all().delete()

    # Tests start here
    def test_if_host_equal(self):
        self.assertEqual(self.update1.host.name, self.package1.hosts.all()[0].name)

    def test_unicode(self):
        self.assertIsInstance(str(self.host1), str)
        self.assertIsInstance(str(self.package1), str)
        self.assertIsInstance(str(self.package2), str)
        self.assertIsInstance(str(self.update1), str)
        self.assertIsInstance(self.update1.get_changelog_url(), str)
        self.assertIsInstance(str(self.update2), str)
        self.assertIsInstance(self.update2.get_changelog_url(), str)
        self.assertIsInstance(str(self.update3), str)
        self.assertIsNone(self.update3.get_changelog_url())


class ViewsTestCase(unittest.TestCase):
    '''
    Testing views class
    '''
    def setUp(self):
        '''
        Commands run before every test
        '''

        # Using hwdoc's test case in order to DRY and setup a proper env for
        # tests
        from hwdoc.tests import EquipmentTestCase
        EquipmentTestCase.dummy = lambda x: True
        self.etc = EquipmentTestCase('dummy')
        self.etc.setUp()

        self.package1 = Package.objects.create(name='testpackage', sourcename='testsource')
        self.package2 = Package.objects.create(name='testpackage2', sourcename='testsource')
        self.host1 = Host.objects.create(name='testservermonHost1', ip='10.10.10.10')
        self.host2 = Host.objects.create(name='testservermonHost2', ip='10.10.10.11')
        self.host3 = Host.objects.create(name='testservermonHost3', ip='10.10.10.12')
        self.fact1 = Fact.objects.create(name='interfaces')
        self.fact2 = Fact.objects.create(name='macaddress_eth0')
        self.fact3 = Fact.objects.create(name='ipaddress_eth0')
        self.fact4 = Fact.objects.create(name='netmask_eth0')
        self.fact5 = Fact.objects.create(name='ipaddress6_eth0')
        self.fact6 = Fact.objects.create(name='serialnumber')
        self.factvalue1 = FactValue.objects.create(
            value='eth0',
            fact_name=self.fact1, host=self.host1)
        self.factvalue2 = FactValue.objects.create(
            value='aa:bb:cc:dd:ee:ff',
            fact_name=self.fact2, host=self.host1)
        self.factvalue3 = FactValue.objects.create(
            value='10.10.10.10',
            fact_name=self.fact3, host=self.host1)
        self.factvalue4 = FactValue.objects.create(
            value='255.255.255.0',
            fact_name=self.fact4, host=self.host1)
        self.factvalue5 = FactValue.objects.create(
            value='dead:beef::1/64',
            fact_name=self.fact5, host=self.host1)
        self.factvalue6 = FactValue.objects.create(
            value='R123457',
            fact_name=self.fact6, host=self.host2)
        self.factvalue7 = FactValue.objects.create(
            value='G123456',
            fact_name=self.fact6, host=self.host3)
        self.update1 = Update.objects.create(
            package=self.package1, host=self.host1,
            installedVersion='1.1', candidateVersion='1.2',
            source='TestSource', origin='Debian')
        self.update2 = Update.objects.create(
            package=self.package2, host=self.host1, is_security=True,
            installedVersion='1.1', candidateVersion='1.2',
            source='TestSource', origin='Ubuntu')

    def tearDown(self):
        '''
        Commands run after every test
        '''
        Package.objects.all().delete()
        Update.objects.all().delete()
        Host.objects.all().delete()
        Fact.objects.all().delete()
        FactValue.objects.all().delete()
        self.etc.tearDown()

    def test_hostlist(self):
        c = Client()
        response = c.get('/hosts/')
        self.assertEqual(response.status_code, 200)

    def test_packagelist(self):
        c = Client()
        response = c.get('/packages/')
        self.assertEqual(response.status_code, 200)

    def test_empty_package(self):
        c = Client()
        data = ['']
        for d in data:
            response = c.get('/packages/%s' % d)
            # This is not an error since empty package means, due to
            # urls.py that we fallback to packagelist
            self.assertEqual(response.status_code, 200)

    def test_nonexistent_package(self):
        c = Client()
        data = ['nosuchpackage']
        for d in data:
            response = c.get('/packages/%s' % d)
            self.assertEqual(response.status_code, 404)

    def test_existent_package(self):
        c = Client()
        data = [self.package1.name, self.package2.name]
        for d in data:
            response = c.get('/packages/%s' % d)
            self.assertEqual(response.status_code, 200)

    def test_existent_package_plaintext(self):
        c = Client()
        data = [self.package1.name, self.package2.name]
        for d in data:
            response = c.get('/packages/%s' % d, {'plain': 'yes'})
            self.assertEqual(response.status_code, 200)

    def test_empty_host(self):
        c = Client()
        response = c.get('/hosts/%s' % '')
        # This should work because of urls fallback to hostlist
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_host(self):
        c = Client()
        response = c.get('/hosts/%s' % 'nosuchhost')
        self.assertEqual(response.status_code, 404)

    def test_existent_host(self):
        c = Client()
        data = [self.host1.name, self.host2.name, self.host3.name]
        for d in data:
            response = c.get('/hosts/%s' % d)
            self.assertEqual(response.status_code, 200)

    def test_existent_host_without_interfaces(self):
        c = Client()
        data = [self.host2.name]
        for d in data:
            response = c.get('/hosts/%s' % d)
            self.assertEqual(response.status_code, 200)


class CommandsTestCase(unittest.TestCase):
    '''
    A test case for django management commands
    '''

    def setUp(self):
        '''
        Commands run before every test
        '''
        self.package1 = Package.objects.create(name='testpackage', sourcename='testsource')
        self.package2 = Package.objects.create(name='testpackage2', sourcename='testsource2')
        self.host1 = Host.objects.create(name='testservermonHost1', ip='10.10.10.10')
        self.host2 = Host.objects.create(name='testservermonHost2', ip='10.10.10.11')
        self.fact1 = Fact.objects.create(name='interfaces')
        self.fact2 = Fact.objects.create(name='macaddress_eth0')
        self.fact3 = Fact.objects.create(name='ipaddress_eth0')
        self.fact4 = Fact.objects.create(name='netmask_eth0')
        self.fact5 = Fact.objects.create(name='ipaddress6_eth0')
        self.fact6 = Fact.objects.create(name='package_updates')
        self.factvalue1 = FactValue.objects.create(
            value='eth0',
            fact_name=self.fact1, host=self.host1)
        self.factvalue2 = FactValue.objects.create(
            value='aa:bb:cc:dd:ee:ff',
            fact_name=self.fact2, host=self.host1)
        self.factvalue3 = FactValue.objects.create(
            value='10.10.10.10',
            fact_name=self.fact3, host=self.host1)
        self.factvalue4 = FactValue.objects.create(
            value='255.255.255.0',
            fact_name=self.fact4, host=self.host1)
        self.factvalue5 = FactValue.objects.create(
            value='dead:beef::1/64',
            fact_name=self.fact5, host=self.host1)
        v = """<?xml version="1.0" ?>
            <host name="%s">
                <package current_version="1.0"
                         is_security="true"
                         name="testpackage"
                         new_version="1.1"
                         origin="Debian"
                         source_name="testsource"/>
                <package current_version="1.0"
                         is_security="true"
                         name="nosuchpackage"
                         new_version="1.1"
                         origin="Debian"
                         source_name="nosuchsource"/>
            </host>""" % self.host1
        self.factvalue6 = FactValue.objects.create(
            value=v,
            fact_name=self.fact6, host=self.host1)

    def tearDown(self):
        '''
        Commands run after every test
        '''

        Package.objects.all().delete()
        Host.objects.all().delete()
        Fact.objects.all().delete()
        FactValue.objects.all().delete()
        Package.objects.all().delete()

    def test_make_updates(self):
        call_command('make_updates')


class MigrationsTestCase(unittest.TestCase):
    '''
    A test case for migration testing
    '''

    def setUp(self):
        # Do a fake migration first to update the migration history.
        call_command('migrate', 'updates',
                     fake=True, verbosity=0, no_initial_data=True)
        # Then rollback to the start
        call_command('migrate', 'updates', '0001_initial',
                     verbosity=0, no_initial_data=True)

    def tearDown(self):
        # We do need to tidy up and take the database to its final
        # state so that we don't get errors when the final truncating
        # happens.
        call_command('migrate', 'updates',
                     verbosity=0, no_initial_data=True)

    def test_migrate_full_forwards(self):
        call_command('migrate', 'updates',
                     verbosity=0, no_initial_data=True)

    def test_migrate_full_backwards(self):
        call_command('migrate', 'updates', '0001_initial',
                     verbosity=0, no_initial_data=True)
