from flask import Flask, send_from_directory, abort
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class Items(Resource):
    def get(self):
        """
        Get all items from the database.
        """
        # Read the database.
        data = pd.read_csv('./data/items.csv')

        # Return data and an okay code.
        return {'code': 200, 'data': data.to_dict('records')}


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

        # Read the database.
        data = pd.read_csv('data/items.csv')

        if args['name'] in list(data['name']):
            # If the item is in the database, return a message saying it already exists.
            return {'code': 404, 'message': f"'{args['name']}' already exists."}
        else:
            # If the item is not in the database, add it to the database.
            new_data = pd.DataFrame({
                'name': args['name'],
                'quant': int(args['quant']),
                'tags': args['tags'],
            }, index=[0])
            data = data.append(new_data, ignore_index=True)

            # Return the current state of the database and and okay code.
            data.to_csv('data/items.csv', index=False)
            return {'code': 200, 'data': data.to_dict('records')}


    def delete(self):
        """
        Delete an item from the database.
        """
        # Setup argument parser.
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        # Read the database.
        data = pd.read_csv('data/items.csv')

        if args['name'] in list(data['name']):
            data.drop(data.loc[data['name'] == args['name']].index, inplace=True)

            # Return the current state of the database and and okay code.
            data.to_csv('data/items.csv', index=False)
            return {'code': 200, 'data': data.to_dict('records')}
        else:
            # If the item is not in the database, return a message stating that it is not
            # in the database and return a 404, not found error code.
            return {'code': 404, 'message': f"item '{args['name']}' not found"}


    def put(self):
        """
        Edit an item in the database.
        """
        # Setup argument parser.
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('quant', required=True)
        parser.add_argument('tags', required=True)
        args = parser.parse_args()

        # Read the database.
        data = pd.read_csv('data/items.csv')

        if args['name'] in list(data['name']):
            # If the item is in the database, remove the item from the database.
            data.loc[data['name'] == args['name'], 'quant'] = int(args['quant'])
            data.loc[data['name'] == args['name'], 'tags'] = args['tags']

            # Return the current state of the database and and okay code.
            data.to_csv('data/items.csv', index=False)
            return {'code': 200, 'data': data.to_dict('records')}
        else:
            # If the item is not in the database, return a message stating that it is not
            # in the database and return a 404, not found error code.
            return {'code': 404, 'message': f"item '{args['name']}' not found"}


    @app.route('/data')
    def get_csv():
        try:
            return send_from_directory('data', 'items.csv')
        except FileNotFoundError:
            abort(404)


api = Api(app)
api.add_resource(Items, '/items') # '/items' is our entry point
app.run(port=5000)
