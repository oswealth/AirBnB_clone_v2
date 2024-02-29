import unittest
from unittest.mock import patch
from io import StringIO


def test_create_state_command(self):
    """Test the create State command in the console"""
    # Get the current count of records in the 'states' table
    dbc = MySQLdb.connect(
        host=os.getenv('HBNB_MYSQL_HOST'),
        port=3306,
        user=os.getenv('HBNB_MYSQL_USER'),
        passwd=os.getenv('HBNB_MYSQL_PWD'),
        db=os.getenv('HBNB_MYSQL_DB')
    )
    cursor = dbc.cursor()
    cursor.execute('SELECT COUNT(*) FROM states;')
    old_count = cursor.fetchone()[0]
    cursor.close()
    dbc.close()

    # Execute the console command to create a new State
    with patch('sys.stdout', new=StringIO()) as cout:
        cons = HBNBCommand()
        cons.onecmd('create State name="California"')

    # Get the count of records in the 'states' table after the command
    dbc = MySQLdb.connect(
        host=os.getenv('HBNB_MYSQL_HOST'),
        port=3306,
        user=os.getenv('HBNB_MYSQL_USER'),
        passwd=os.getenv('HBNB_MYSQL_PWD'),
        db=os.getenv('HBNB_MYSQL_DB')
    )
    cursor = dbc.cursor()
    cursor.execute('SELECT COUNT(*) FROM states;')
    new_count = cursor.fetchone()[0]
    cursor.close()
    dbc.close()

    # Check if the difference is +1
    self.assertEqual(new_count, old_count + 1)
