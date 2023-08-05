import json
import os
import sqlite3
import subprocess
import unittest


class TestSQL(unittest.TestCase):
    def setUp(self):
        db_filepath = '/tmp/test1'
        with open(db_filepath, 'w'):
            pass
        self.db_filepath = db_filepath
        db = sqlite3.connect(db_filepath)
        c = db.cursor()
        c.execute('CREATE TABLE test_table1 (col1 text, col2 int);')
        c.execute("INSERT INTO test_table1 (col1, col2) VALUES ('test', 1);")
        c.execute("INSERT INTO test_table1 (col1, col2) VALUES ('test', 2);")
        c.execute("INSERT INTO test_table1 (col1, col2) VALUES ('test', 3);")
        db.commit()
        db.close()

    def tearDown(self):
        os.unlink(self.db_filepath)

    def run_recipe(self, taskname):
        c = subprocess.run([
            'python', '-m',
            'bamboo_crawler',
            '-r', 'tests/sql/recipe.yml',
            '-t', taskname],
            stdout=subprocess.PIPE)
        self.assertEqual(c.returncode, 0)
        return c

    def test_test1(self):
        c = self.run_recipe('test1')
        j = json.loads(c.stdout)
        self.assertEqual(j['col1'], 'test')
        self.assertEqual(j['col2'], 1)

    def test_test2(self):
        db = sqlite3.connect(self.db_filepath)
        c1, = db.execute('SELECT COUNT(*) FROM test_table1').fetchone()
        self.run_recipe('test2')
        db = sqlite3.connect(self.db_filepath)
        c2, = db.execute('SELECT COUNT(*) FROM test_table1').fetchone()
        self.assertEqual(c1 + 1, c2)

    def test_test3(self):
        c = self.run_recipe('test3')
        j = json.loads(c.stdout)
        self.assertEqual(j['col1'], 'test')
        self.assertEqual(j['col2'], 1)

    def test_test4(self):
        db = sqlite3.connect(self.db_filepath)
        c1, = db.execute('SELECT COUNT(*) FROM test_table1').fetchone()
        self.run_recipe('test4')
        db = sqlite3.connect(self.db_filepath)
        c2, = db.execute('SELECT COUNT(*) FROM test_table1').fetchone()
        self.assertEqual(c1 + 1, c2)
