# CRUD

[CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) is a basic inventory management system built using React. CRUD stands for Create, Read, Update, and Delete.

The **additional feature** I chose to create was "Press a button to export product data to a CSV"

## Docker Installation

### Setup

The frontend and backend are both dockerized. Ensure that docker is installed and enabled following these [instructions](https://docs.docker.com/get-docker/). Then do the following:

1. Clone the repository and go to where you cloned it. (`git clone https://github.com/hisbaan/crud; cd crud`)
2. Go to the `backend` directory (`cd backend`).
3. Run the following docker command:

```sh
docker compose up -d
```
4. Repeat steps 2 and 3 for the `frontend` directory.
5. Open [localhost:3000](http://localhost:3000)

The following script will do all of the above:

```bash
git clone https://github.com/hisbaan/crud
cd crud/backend
docker compose up -d
cd ../frontend
docker compose up -d
```

This will setup and start the docker containers. To learn how to start and stop them after this, read the next section, `Start and Stop`.

### Start and Stop

To start the docker containers run the following command:

```bash
docker start crud-backend crud-frontend
```

To stop the docker containers run the following command:

```bash
docker stop crud-backend crud-frontend
```

## Developer Installation

### Frontend

The frontend is written in React + TypeScript. First go to the `frontend` directory and install all the node dependencies with `npm install`. Then, run the `npm start` command to start the frontend server. The frontend server will then be launched on [localhost:3000](http://localhost:3000).

### Backend

The backend is written in Python + Flask. First, initialize the database. To do this, go to the `backend` directory and run `python init_db.py`. This will create a file `items.db` which is the database for the application. Next, start the backend server. Go to the `backend` directory (if you aren't already in it) and run `python main.py`. This will start the server in development mode. The following are the HTTP calls available to accomplish a CRUD inventory system:

#### GET (Read)

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

#### POST (Create)

To create a new item in the database, structure your query as follows:

```
http://localhost:5000/items?name=<name of item>&quant=<quantity of item>&tags=<tags of item separated by spaces>
```

If the item is already in the database, then the server will return a 401 code. This query is only for adding to the database. If you would like to update or edit an item, use the PUT query instead.

If the item is not already in the database, then the server will add the item to the database and return the new database state.

#### PUT (Update)

To update an item in the database, structure your query as follows:

```
http://localhost:5000/items?id=<id of item>&name=<new name of item>&quant=<new quantity of item>&tags=<new tags of item separated by spaces>
```

If the item is in the database, then the server will update the `quant` and `tags` fields and return the new database state.

If the item is not in the database, then the server will return a 404 error code.

#### DELETE (Delete)

To delete an item from the database, structure your query as follows:

```
http://localhost:5000/items?id=<id of item>
```

If the item is in the database, then the server will delete the item from the database and return the new database state.

If the item is not in the database, then the server will return a 404 error code.
