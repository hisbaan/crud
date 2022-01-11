# CRUD

[CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) is a basic inventory management system built using React. CRUD stands for Create, Read, Update, and Delete.

## Frontend

The frontend is written in React + TypeScript. First go to the `frontend` directory and run the `npm start` command to start the frontend server. The frontend server will then be launched on [localhost:3000](http://localhost:3000).
<!-- ### `npm test` -->
<!---->
<!-- Launches the test runner in the interactive watch mode.\ -->
<!-- See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information. -->

<!-- ### `npm run build` -->
<!---->
<!-- Builds the app for production to the `build` folder.\ -->
<!-- It correctly bundles React in production mode and optimizes the build for the best performance. -->
<!---->
<!-- The build is minified and the filenames include the hashes.\ -->
<!-- Your app is ready to be deployed! -->
<!---->
<!-- See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information. -->

## Backend

The backend is written in Python + Flask. To start the backend server, go to the `backend` directory and run `python main.py`. This will start the server in development mode. The following are the HTTP calls available to accomplish a CRUD inventory system:

### GET (Read)

To get all items from the database, structure your query as follows:

```
http://localhost:5000/items
```

This will return the current state of the database in JSON format:

```json
{
    "code": 200,
    "data": [
        {
            "name": "red apple",
            "quant": 100,
            "tags": "apple red sweet"
        },
        {
            "name": "green apple",
            "quant": 199,
            "tags": "apple green sour"
        }
    ]
}
```

### POST (Create)

To create a new item in the database, structure your query as follows:

```
http://localhost:5000/items?name=<name of item>&quant=<quantity of item>&tags=<tags of item separated by spaces>
```

If the item is already in the database, then the server will return a 401 code. This query is only for adding to the database. If you would like to update or edit an item, use the PUT query instead.

If the item is not already in the database, then the server will add the item to the database and return the new database state.

### PUT (Update)

To update an item in the database, structure your query as follows:

```
http://localhost:5000/items?name=<name of item>&quant=<quantity of item>&tags=<tags of item separated by spaces>
```

If the item is in the database, then the server will update the `quant` and `tags` fields and return the new database state.. It is important to note that you cannot modify the `name` field as that is the "key" so to speak. If you would like to edit the name, delete and re-create the item with the new name.

If the item is not in the database, then the server will return a 404 error code.

### DELETE (Delete)

To delete an item from the database, structure your query as follows:

```
http://localhost:5000/items?name=<name of item>
```

If the item is in the database, then the server will delete the item from the database and return the new database state.

If the item is not in the database, then the server will return a 404 error code.
