from flask import Flask, send_from_directory, abort
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import sqlite3
import csv


# Setup flask settings.
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    """
    Create a dictionary from a row of SQLite data.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection() -> sqlite3.Connection:
    """
    Get the database connection and return it for use in the application.
    """
    connection = sqlite3.connect('items.db')
    connection.row_factory = dict_factory
    sqlite3.Row
    return connection


def id_exists(id: int, cursor: sqlite3.Cursor) -> bool:
    """
    Check if an item with the given ID exists in the database.
    """
    if cursor.execute(f"SELECT EXISTS(SELECT 1 FROM items WHERE id={id});").fetchone():
        return True
    else:
        return False


class Items(Resource):
    def get(self):
        """
        Get all items from the database.
        """
        # Read from the database.
        connection = get_db_connection()
        cursor = connection.cursor()
        data = cursor.execute('SELECT * FROM items;').fetchall()
        connection.close()

        # Return data and an okay code.
        return {'code': 200, 'data': data}


    def post(self):
        """
        Push an item to the database.
        """
        # Setup argument parser.
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('quant', required=True)
        parser.add_argument('tags', required=True)
        args = parser.parse_args()

        # Get database connection.
        connection = get_db_connection()
        cursor = connection.cursor()

        # Write the new item into the database.
        cursor.execute(
            "INSERT INTO items (name, quant, tags) VALUES (?, ?, ?);",
            (args['name'], int(args['quant']), args['tags'])
        )
        connection.commit()

        # Get the database state.
        data = cursor.execute('SELECT * FROM items;').fetchall()
        connection.close()

        # Return the current state of the database and a 200 code.
        return {'code': 200, 'data': data}


    def delete(self):
        """
        Delete an item from the database.
        """
        # Setup argument parser.
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        args = parser.parse_args()

        # Get database connection.
        connection = get_db_connection()
        cursor = connection.cursor()

        # If the item is in the database, delete it from the databse.
        # If it is not, return an error.
        if id_exists(args['id'], cursor):
            # Delete the item from the database.
            cursor.execute(f"DELETE FROM items WHERE id = {args['id']};")
            connection.commit()

            # Get the new state of the database.
            data = cursor.execute('SELECT * FROM items;').fetchall()
            connection.close()

            # Return the current state of the database and and okay code.
            return {'code': 200, 'data': data}
        else:
            connection.close()

            # Return an error code stating the item does not exist.
            return {'code': 404, 'message': "requested item not found"}


    def put(self):
        """
        Edit an item in the database.
        """
        # Setup argument parser.
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('quant', required=True)
        parser.add_argument('tags', required=True)
        args = parser.parse_args()

        # Get database connection.
        connection = get_db_connection()
        cursor = connection.cursor()

        # If the item is in the database, modify it.
        # If it is not, return an error.
        if id_exists(args['id'], cursor):
            # Modify the item in the databse.
            cursor.execute(
                f"UPDATE items SET name=?, quant=?, tags=? WHERE id=?;",
                (args['name'], int(args['quant']), args['tags'], args['id'])
            )

            connection.commit()

            # Get the new state of the database.
            data = cursor.execute('SELECT * FROM items;').fetchall()
            connection.close()

            # Return the current state of the database and and okay code.
            return {'code': 200, 'data': data}
        else:
            connection.close()

            # Return an error code stating the item does not exist.
            return {'code': 404, 'message': "requested item not found"}


    @app.route('/data')
    def get_csv():
        # Get data from database.
        connection = sqlite3.connect('items.db')
        cursor = connection.cursor()
        data = cursor.execute('SELECT * FROM items;').fetchall()

        # Create CSV from data.
        with open('data/items.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'quant', 'tags'])
            writer.writerows(data)

        # Send CSV to user.
        try:
            return send_from_directory('data', 'items.csv')
        except FileNotFoundError:
            abort(404)


# Setup API settings.
api = Api(app)
api.add_resource(Items, '/items') # '/items' is our entry point

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
