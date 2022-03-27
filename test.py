from contextlib import redirect_stderr
import os
import unittest
import sqlite3
from pathlib import Path
from prettytable import PrettyTable

#################################
# DON'T TOUCH THIS CODE. DON'T! #
#################################

class TestSqlQueries(unittest.TestCase):
    """ Class for grading SQL queries included in challenges directory
        Can be run with unittest or as __main__ to test without python errors."""

    @classmethod
    def setUpClass(cls):
        """Sets up an in-memory database fixture with a create script to be shared
           shared with all the tests
        """
        in_mem_db = sqlite3.connect(':memory:')
        # make each row searchable by column name
        in_mem_db.row_factory = TestSqlQueries.dict_factory
        in_mem_db.executescript(Path('musician.db.sql').read_text())
        cls._connection = in_mem_db

    @classmethod
    def tearDownClass(cls):
        """Close the db connection fixture before exiting
        """
        cls._connection.close()

    @staticmethod
    def dict_factory(cursor, row):
        """set the in-memory db's row_factory function to this method
           to allow each result row to be searched by column name 

        Args:
            cursor (Cursor): the connection cursor that has the column names
            row (Row): the current row the cursor is reading

        Returns:
            dict: the row represented as a dict 
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    @staticmethod
    def remove_duplicate_rows():
        pass

    def pretty_table(self, results, columns):
        """create a Pretty Table to display results

        Args:
            results (list[Any]): Will be a list of dataclass instances
            columns (list[str]): the column names to add as headers

        Returns:
            PrettyTable: the pretty table instance with the results and columns
        """
        pt = PrettyTable()
        pt.field_names = columns
        pt.add_rows(results)
        return pt

    def print_title(self, title):
        """Convenience method to pretty-print the title of each query result

        Args:
            title (str): whatever title you want to add to the printed result
        """
        print()
        print('-'*len(title))
        print(title)
        print('-'*len(title))

    def run_query(self, filepath):
        """Reads the SQL query file, executes the query, and catches any
           SQL errors

        Args:
            filepath (str): relative path to the query file

        Returns:
            Cursor: a db cursor to iterate over the results
        """
        txt = Path(filepath).read_text()
        cur = self._connection.cursor()
        results = None
        try:
            results = cur.execute(txt)
        except Exception as ex:
            print('Query caused following error -', ex)
            # still raise so the test gets graded
            raise
        return results
    
    def compare_results(self, raw_results, raw_columns, expected):
        """Assuming no SQL or missing columns, this method compares the expected
           rows to the actual rows returned from the db, and prints the results
           before raising if they don't match

        Args:
            raw_results (list[dict]): the raw results to make sure all the user's column's are printed
            raw_columns (list[str]): a list of the columns from the query in the event that the python class properties
            don't match the actual results
            expected (list[dict]): expected results to compare
        """
        try:
            self.assertEqual(raw_results, expected)
            print('Correct!')
        except AssertionError:
            print('Query is not quite right!')
            print()
            print('Your Results:')
            print(self.pretty_table([tuple(x.values()) for x in raw_results], raw_columns))
            print()
            print('Expected Results:')
            print(self.pretty_table([tuple(result.values()) for result in expected], expected[0].keys()))
            # still raise so the test can get graded 
            raise  
    
    def run_query_test(self, title, filepath, expected):
        """This is the method that will start each challenge

        Args:
            title (str): The header that will be printed with the results of a challenge
            filepath (str): the relative path to the sql query file
            expected (list[Any]): a list of Python objects of a type that can hold the row data
        """

        self.print_title(title)


        cursor = self.run_query(filepath)
        raw_results = cursor.fetchall()
        if (len(raw_results)):
            raw_columns = raw_results[0].keys()
        else:
            # if we don't have results, we have to get the columns from 
            # the description if an actual query was written but returned 
            # no rows
            if cursor.description is not None:
                raw_columns = set([x[0] for x in cursor.description])
            # or an empty list if the query hasn't been run yet
            else:
                raw_columns = []
        
        self.compare_results(raw_results, raw_columns, expected)
        
    def test_all(self):
        """We run all of the tests in one test method so that the program will stop
           executing as soon as one of the challenges is incorrect, to reduce the 
           amount of noise printed to the terminal every time the tests are run
        """
        self.run_query_test(
            title='#1: Get all musicians', 
            filepath='challenges/01select_star.sql',
            expected=[
                {'MusicianId':1, 'MusicianName': 'Sun Ra'},
                {'MusicianId':2, 'MusicianName': 'Weird Guy Down the Street'},
                {'MusicianId':3, 'MusicianName': 'Julie'}
            ])
        self.run_query_test(
            title = '#2: Get the Names of the Instruments played by "Julie"',
            filepath='challenges/02julies_instruments.sql',
            expected=[
                {'InstrumentName': 'Triangle'}, 
                {'InstrumentName': 'Upright Bass'}
                ])
        self.run_query_test(
            title='#3: Get the number of people that play Triangle',
            filepath='challenges/03num_trianglers.sql',
            expected=[{'NumberofTrianglers': 2}])
        self.run_query_test(
            title='#4 Get the musician with the id of 2',
            filepath='challenges/04musician_number_2.sql',
            expected=[{'MusicianId': 2, 'MusicianName': 'Weird Guy Down the Street'}]
        )
        self.run_query_test(
            title='#5 Get Instruments in alphabetical order',
            filepath='challenges/05instruments_in_order.sql',
            expected=[
                {'InstrumentId': 5, 'InstrumentName': 'Fiddle', 'DifficultyId': 2},
                {'InstrumentId': 1, 'InstrumentName': 'Recorder', 'DifficultyId': 1},
                {'InstrumentId': 2, 'InstrumentName': 'Triangle', 'DifficultyId': 1},
                {'InstrumentId': 3, 'InstrumentName': 'Trumpet', 'DifficultyId': 2},
                {'InstrumentId': 4, 'InstrumentName': 'Upright Bass', 'DifficultyId': 2}
            ]
        )

if __name__ == '__main__':
    # silence python errors when user runs program
    with open(os.devnull, 'w') as stderr, redirect_stderr(stderr):
        unittest.main()