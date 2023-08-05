# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import os
import shutil
import sys
import tempfile
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import pkg_resources
import psycopg2

from . import testing


class BaseTestCase(unittest.TestCase):
    @property
    def target(self):
        from ..cli import main
        return main

    def tearDown(self):
        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS schema_migrations')


class VersionTestCase(BaseTestCase):
    def test(self):
        version = pkg_resources.get_distribution('db-migrator').version
        with testing.captured_output() as (out, err):
            self.assertRaises(SystemExit, self.target, ['-V'])

        stdout = out.getvalue()
        stderr = err.getvalue()
        if sys.version_info[0] == 3:
            self.assertEqual(stdout.strip(), version)
        else:
            self.assertEqual(stdout, '')
            self.assertEqual(stderr.strip(), version)


class VerboseTestCase(BaseTestCase):
    @mock.patch('dbmigrator.logger.debug')
    def test(self, debug):
        from .. import logger

        with testing.captured_output() as (out, err):
            self.target(['-v', '--config', testing.test_config_path, 'init'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(1, debug.call_count)
        self.assertTrue(debug.call_args[0][0].startswith('args: {'))

        self.assertEqual('Schema migrations initialized.\n', stdout)
        self.assertEqual('', stderr)


class ListTestCase(BaseTestCase):
    def test_no_migrations_directory(self):
        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['init'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(stdout, """\
version        | name            | is applied | date applied
----------------------------------------------------------------------\n""")
        self.assertEqual(stderr, """\
context undefined, using current directory name "['db-migrator']"
migrations directory undefined\n""")

    @mock.patch('dbmigrator.logger.warning')
    def test_no_table(self, warning):
        cmd = ['--config', testing.test_config_path]
        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
version        | name            | is applied | date applied
----------------------------------------------------------------------\n""",
                         stdout)

        warning.assert_called_with(
            'You may need to create the schema_migrations table: '
            'dbmigrator init --help')
        self.assertEqual('', stderr)

    def test(self):
        testing.install_test_packages()

        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['init'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['-v', '--context', 'package-a', 'list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
version        | name            | is applied | date applied
----------------------------------------------------------------------
20160228202637   add_table         False        \

20160228212456   cool_stuff        False        \
\n""", stdout)
        self.assertEqual('', stderr)

    def test_wide(self):
        testing.install_test_packages()

        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['init'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['-v', '--context', 'package-a',
                               'list', '--wide'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
version        | name       | is applied | date applied
----------------------------------------------------------------------
20160228202637   add_table    False        \

20160228212456   cool_stuff   False        \
\n""", stdout)
        self.assertEqual('', stderr)


class InitTestCase(BaseTestCase):
    def test_multiple_contexts(self):
        testing.install_test_packages()

        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['--context', 'package-a', '--context', 'package-b',
                           'init'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', '--context',
                               'package-b', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         True', stdout)
        self.assertIn('20160228210326   initial_data      True', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)


class MarkTestCase(BaseTestCase):
    def test_missing_t_f_d_option(self):
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init'])

        with self.assertRaises(Exception) as cm:
            self.target(cmd + ['--context', 'package-a', 'mark',
                               '20160228212456'])

        self.assertEqual('-t, -f or -d must be supplied.', str(cm.exception))

    def test_mark_as_true(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a',
                               'mark', '-t', '20160228212456'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228212456 marked as completed\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         False', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

    def test_mark_as_true_already_true(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a',
                               'mark', '-t', '20160228212456'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228212456 marked as completed\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         True', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

    def test_migration_not_found(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        with self.assertRaises(SystemExit) as cm:
            self.target(cmd + ['mark', '-t', '012345'])
        self.assertEqual('Migration 012345 not found', str(cm.exception))

        with self.assertRaises(SystemExit) as cm:
            self.target(cmd + ['mark', '-f', '012345'])
        self.assertEqual('Migration 012345 not found', str(cm.exception))

    def test_mark_as_false(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string,
               '--context', 'package-a']

        self.target(cmd + ['init'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['mark', '-f', '20160228202637'])

        stdout = out.getvalue()
        self.assertIn('Migration 20160228202637 marked as not been run',
                      stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         False', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

    def test_mark_as_false_already_false(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'mark', '-f',
                               '20160228202637'])

        stdout = out.getvalue()
        self.assertIn('Migration 20160228202637 marked as not been run',
                      stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         False', stdout)
        self.assertIn('20160228212456   cool_stuff        False', stdout)

    def test_mark_as_deferred(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        # mark migration as deferred
        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'mark', '-d',
                               '20160228202637'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228202637 marked as deferred\n',
                         stdout)

        # check list output
        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         deferred', stdout)
        self.assertIn('20160228212456   cool_stuff        False', stdout)

        # try running migrations
        self.target(cmd + ['--context', 'package-a', 'migrate'])

        # check that the table is not created by the migration
        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute("""\
SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'a_table'""")
                table_exists = cursor.fetchone()
        self.assertEqual(None, table_exists)

        # check list output again
        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         deferred', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

        # check that rollback does not rollback a deferred migration
        self.target(cmd + ['--context', 'package-a', 'rollback', '--step=2'])

        # check list output again
        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         deferred', stdout)
        self.assertIn('20160228212456   cool_stuff        False', stdout)

    def test_deferred(self):
        md = os.path.join(testing.test_data_path, 'md')
        cmd = ['--db-connection-string', testing.db_connection_string,
               '--migrations-directory', md]

        self.target(cmd + ['init', '--version', '0'])

        # check list output
        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        self.assertIn('20170810124056   empty             deferred', stdout)

        # mark a deferred migration as completed
        with testing.captured_output() as (out, err):
            self.target(cmd + ['mark', '-t', '20170810124056'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20170810124056 marked as completed\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        self.assertIn('20170810124056   empty             deferred*    20',
                      stdout)

        # mark a deferred migration as not not been run
        with testing.captured_output() as (out, err):
            self.target(cmd + ['mark', '-f', '20170810124056'])

        stdout = out.getvalue()
        self.assertIn('Migration 20170810124056 marked as not been run',
                      stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        self.assertIn('20170810124056   empty             deferred', stdout)


class GenerateTestCase(BaseTestCase):
    @mock.patch('dbmigrator.utils.timestamp')
    def test(self, timestamp):
        timestamp.return_value = '20160423231932'
        filename = '{}_a_new_migration.py'.format(timestamp())
        expected_path = os.path.join(
            testing.test_migrations_directories[0], filename)

        def cleanup():
            if os.path.exists(expected_path):
                os.remove(expected_path)
        self.addCleanup(cleanup)

        testing.install_test_packages()

        with testing.captured_output() as (out, err):
            self.target(['--context', 'package-a', 'generate',
                         'a_new_migration'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(
            'Generated migration script "dbmigrator/tests/data/package-a/'
            'package_a/migrations/{}"\n'.format(filename),
            stdout)
        self.assertEqual('', stderr)

        self.assertTrue(os.path.exists(expected_path))

        with open(expected_path, 'r') as f:
            content = f.read()

        self.assertIn('# -*- coding: utf-8 -*-', content)
        self.assertIn('def up(cursor):', content)
        self.assertIn('def down(cursor):', content)

    def test_no_migrations_directory(self):
        with self.assertRaises(Exception) as cm:
            self.target(['generate', 'a_new_migration'])

        self.assertEqual('migrations directory undefined',
                         str(cm.exception))

    def test_multiple_migrations_directory(self):
        tmp_dir = tempfile.gettempdir()
        tmp_dir2 = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp_dir2)
        with self.assertRaises(Exception) as cm:
            self.target(['--migrations-directory', tmp_dir,
                         '--migrations-directory', tmp_dir2,
                         'generate', 'a_new_migration'])

        self.assertEqual('more than one migrations directory specified',
                         str(cm.exception))

    @mock.patch('dbmigrator.utils.timestamp')
    def test_migrations_directory_does_not_exist(self, timestamp):
        timestamp.return_value = '20160423231932'
        filename = '{}_a_new_migration.py'.format(timestamp())
        tmp_dir = tempfile.gettempdir()
        directory = '{}/dbmigrator-tests/m'.format(tmp_dir)
        expected_path = os.path.join(directory, filename)

        self.addCleanup(shutil.rmtree, directory)

        self.target(['--migrations-directory', directory,
                     'generate', 'a_new_migration'])

        self.assertTrue(os.path.exists(expected_path))


class MigrateTestCase(BaseTestCase):
    def test(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        def cleanup():
            with psycopg2.connect(testing.db_connection_string) as db_conn:
                with db_conn.cursor() as cursor:
                    cursor.execute('DROP TABLE IF EXISTS a_table')

        self.addCleanup(cleanup)

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'migrate'])

        stdout = out.getvalue()
        self.assertIn('+CREATE TABLE a_table', stdout)

        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute("""\
                    SELECT table_name FROM information_schema.tables
                        WHERE table_name = 'a_table'""")
                self.assertEqual([('a_table',)], cursor.fetchall())

    def test_repeat(self):
        md = os.path.join(testing.test_data_path, 'md')
        cmd = ['--db-connection-string', testing.db_connection_string,
               '--migrations-directory', md]

        def cleanup():
            if os.path.exists('insert_data.txt'):
                os.remove('insert_data.txt')
            with psycopg2.connect(testing.db_connection_string) as db_conn:
                with db_conn.cursor() as cursor:
                    cursor.execute('DROP TABLE IF EXISTS a_table')

        self.addCleanup(cleanup)

        self.target(cmd + ['init', '--version', '0'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        stdout = out.getvalue()
        self.assertIn('+CREATE TABLE a_table', stdout)
        self.assertIn('Skipping migration 20170810093943', stdout)

        # Run the repeat migration by creating this file
        with open('insert_data.txt', 'w') as f:
            f.write('三好')

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        stdout = out.getvalue()
        self.assertIn('Running migration 20170810093943', stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        stdout = out.getvalue()
        self.assertIn('Running migration 20170810093943', stdout)

        # Make sure data has been inserted twice
        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('SELECT name FROM a_table')
                self.assertEqual([('三好',), ('三好',)],
                                 cursor.fetchall())

        # Mark the repeat migration as deferred
        self.target(cmd + ['mark', '-d', '20170810093943'])

        # The deferred repeat migration should not run
        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        stdout = out.getvalue()
        self.assertIn('Skipping deferred migration 20170810124056 empty',
                      stdout)

    def test_deferred(self):
        md = os.path.join(testing.test_data_path, 'md')
        cmd = ['--db-connection-string', testing.db_connection_string,
               '--migrations-directory', md]

        def cleanup():
            if os.path.exists('insert_data.txt'):
                os.remove('insert_data.txt')
            with psycopg2.connect(testing.db_connection_string) as db_conn:
                with db_conn.cursor() as cursor:
                    cursor.execute('DROP TABLE IF EXISTS a_table')

        self.addCleanup(cleanup)

        self.target(cmd + ['init', '--version', '0'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        stdout = out.getvalue()
        self.assertIn('+CREATE TABLE a_table', stdout)
        self.assertIn('Skipping deferred migration 20170810124056 empty',
                      stdout)

        # Run the repeat migration by creating this file
        with open('insert_data.txt', 'w') as f:
            f.write('三好')

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        stdout = out.getvalue()
        self.assertIn('Running migration 20170810093943', stdout)

        # Mark the deferred migration as not not been run
        self.target(cmd + ['mark', '-f', '20170810124056'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate', '--run-deferred'])
        stdout = out.getvalue()
        self.assertIn('Running migration 20170810124056', stdout)

        # Mark the deferable as deferred
        self.target(cmd + ['mark', '-d', '20170810124056'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate', '--run-deferred'])

        stdout = out.getvalue()
        self.assertIn('Running migration 20170810124056', stdout)


class RollbackTestCase(BaseTestCase):
    @mock.patch('dbmigrator.utils.timestamp')
    def test(self, timestamp):
        timestamp.return_value = '20160423231932'

        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string,
               '--context', 'package-a']

        def cleanup():
            with psycopg2.connect(testing.db_connection_string) as db_conn:
                with db_conn.cursor() as cursor:
                    cursor.execute('DROP TABLE IF EXISTS a_table')
            path = os.path.join(
                testing.test_migrations_directories[0],
                '{}_new_one.py'.format(timestamp()))
            if os.path.exists(path):
                os.remove(path)

        self.addCleanup(cleanup)

        self.target(cmd + ['init', '--version', '0'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        # Generate a new migration that is not yet run
        self.target(cmd + ['generate', 'new_one'])

        # Rollback once, the table should still be there
        with testing.captured_output() as (out, err):
            self.target(cmd + ['rollback'])
        stdout = out.getvalue()
        self.assertIn('Rolling back migration 20160228212456', stdout)

        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute("""\
SELECT table_name FROM information_schema.tables
    WHERE table_name = 'a_table'""")
                self.assertEqual('a_table', cursor.fetchone()[0])

        # Rollback the migration that created the table
        with testing.captured_output() as (out, err):
            self.target(cmd + ['rollback'])
        stdout = out.getvalue()
        self.assertIn('Rolling back migration 20160228202637', stdout)

        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute("""\
SELECT table_name FROM information_schema.tables
    WHERE table_name = 'a_table'""")
                self.assertEqual(None, cursor.fetchone())

        # Migrate again
        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        # Rollback three migrations
        with testing.captured_output() as (out, err):
            self.target(cmd + ['rollback', '--steps', '3'])
        stdout = out.getvalue()
        self.assertIn('Rolling back migration 20160228212456', stdout)
        self.assertIn('Rolling back migration 20160228202637', stdout)

        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute("""\
SELECT table_name FROM information_schema.tables
    WHERE table_name = 'a_table'""")
                self.assertEqual(None, cursor.fetchone())

    def test_repeat(self):
        md = os.path.join(testing.test_data_path, 'md')
        cmd = ['--db-connection-string', testing.db_connection_string,
               '--migrations-directory', md]

        def cleanup():
            if os.path.exists('insert_data.txt'):
                os.remove('insert_data.txt')
            with psycopg2.connect(testing.db_connection_string) as db_conn:
                with db_conn.cursor() as cursor:
                    cursor.execute('DROP TABLE IF EXISTS a_table')

        self.addCleanup(cleanup)

        self.target(cmd + ['init', '--version', '0'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate', '--run-deferred'])

        # Run the repeat migration by creating this file
        with open('insert_data.txt', 'w') as f:
            f.write('三好')

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        with open('insert_data.txt', 'w') as f:
            f.write('ジョーカーゲーム')

        with testing.captured_output() as (out, err):
            self.target(cmd + ['migrate'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        self.assertIn('20170810093842   create_a_table    True ', stdout)
        self.assertIn('20170810093943   repeat_insert_d   True*', stdout)
        self.assertIn('20170810124056   empty             deferred*', stdout)

        # Version wise, the empty migration is more recent, but the repeat
        # migration is the last migration applied, so rollback should rollback
        # the repeat migration.
        with testing.captured_output() as (out, err):
            self.target(cmd + ['rollback'])
        stdout = out.getvalue()
        self.assertIn('Rolling back migration 20170810093943', stdout)

        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('SELECT name FROM a_table')
                self.assertEqual([('三好',)], cursor.fetchall())

        # Next, rollback the empty migration
        with testing.captured_output() as (out, err):
            self.target(cmd + ['rollback'])
        stdout = out.getvalue()
        self.assertIn('Rolling back migration 20170810124056', stdout)
