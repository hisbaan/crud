import React from 'react';
import { useState, useEffect } from 'react';
import './App.css';

// Use GET https request on startup to get the state of the server.
function App() {
    const [items, setItems] = useState<Item[]>([]);

    useEffect(() => {
        get();
    }, [])

    const [addItemPopupState, setAddItemPopupState] = useState<boolean>(false);
    const [editItemPopupState, setEditItemPopupState] = useState<boolean>(false);

    const [id, setId] = useState(0);
    const [name, setName] = useState('');
    const [quant, setQuant] = useState(0);
    const [tags, setTags] = useState('');

    return (
        <div className="App">
            <header className="App-header">
                <h1 className="headline">CRUD! - Inventory Management</h1>
                <div className="outer-buttons">
                    <button onClick={() => {setName(""); setQuant(0); setTags(""); setAddItemPopupState(true)}} className="outer-button">
                    Add Item
                    </button>
                    <button onClick={() => get()} className="outer-button">
                    Refresh
                    </button>
                    <button onClick={() => window.open("http://localhost:5000/data", "_blank")} className="outer-button">
                    Download CSV
                    </button>
                </div>

                <div className="inventory-container">
                    {items.map((item) => {
                        return (
                            <div key={item.name + item.quant+ item.tags} className="card">
                                <ul>
                                    <li className="name">
                                        <div className="heading">Name: </div>
                                        <div>{item.name}</div>
                                    </li>
                                    <li className="quant">
                                        <div>Quantity: </div>
                                        <div>{item.quant}</div>
                                        <button className="square-button" onClick={() => minusOne(item)}>-</button>
                                        <button className="square-button" onClick={() => plusOne(item)}>+</button>
                                    </li>
                                    <li className="tags">
                                        <div>Tags:  </div>
                                        <div>{item.tags}</div>
                                    </li>
                                </ul>
                                <div className="buttons">
                                    <button onClick={() => deleteItem(item)}>
                                    Delete
                                    </button>
                                    <button onClick={() => editItemInput(item)}>
                                    Edit
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
                {addItemPopupState &&
                    <div className="modal">
                        <div className="popup">
                            <form onSubmit={addItem}>
                                <div className="form">
                                    <h1 className="form-header">Add Item</h1>
                                    <label> Name: </label>
                                    <input className="field" type="text" name="name" key="name" value={name} onChange={e => setName(e.target.value)} />
                                    <label> Quantity: </label>
                                    <input className="field" type="number" name="quant" key="quant" value={quant} onChange={e => setQuant(Number(e.target.value))} />
                                    <label> Tags (separated by spaces): </label>
                                    <input className="field" type="text" name="tags" key="tags" value={tags} onChange={e => setTags(e.target.value)} />
                                </div>
                                <br />
                                <div className="row">
                                    <button className="flex-1" onClick={() => setAddItemPopupState(false)}>Cancel</button>
                                    <input className="button flex-1" type="submit" value="Submit" />
                                </div>
                            </form>
                        </div>
                    </div>
                }
                {editItemPopupState &&
                    <div className="modal">
                        <div className="popup">
                            <form onSubmit={editItem}>
                                <div className="form">
                                    <h1 className="form-header">Edit Item</h1>
                                    <label> Name: </label>
                                    <input className="field" type="text" name="name" key="name" value={name} onChange={e => setName(e.target.value)} />
                                    <label> Quantity: </label>
                                    <input className="field" type="number" name="quant" key="quant" value={quant} onChange={e => setQuant(Number(e.target.value))} />
                                    <label> Tags (separated by spaces): </label>
                                    <input className="field" type="text" name="tags" key="tags" value={tags} onChange={e => setTags(e.target.value)} />
                                </div>
                                <br />
                                <div className="row">
                                    <button className="flex-1" onClick={() => setEditItemPopupState(false)}>Cancel</button>
                                    <input className="button flex-1" type="submit" value="Submit" />
                                </div>
                            </form>
                        </div>
                    </div>
                }
            </header>
        </div>
    );

    function get() {
        fetch("http://localhost:5000/items",
            {
                "method": "GET",
            }
        )
            .then(response => response.json())
            .then(response => {
                setItems(response['data'])
            })
            .catch(err => {
                console.log(err);
            });
    }

    function addItem() {
        // Send name, quant, tags with POST request to server then update the local list
        fetch("http://localhost:5000/items?name=" + name + "&quant=" + quant + "&tags=" + tags,
            {
                "method": "POST",
            }
        )
            .then(response => response.json())
            .then(response => {
                if (response['code'] === 200) {
                    setItems(response['data'])
                } else {
                    alert("Error 401: The item '" + name + "' you are trying to add is already in the database")
                }
            })
            .catch(err => {
                console.log(err);
            });

        setAddItemPopupState(false)
    }

    function deleteItem(item: Item) {
        // Send DELETE request to server with 'name' and update the local list
        fetch("http://localhost:5000/items?id=" + item.id,
            {
                "method": "DELETE",
            }
        )
            .then(response => response.json())
            .then(response => {
                console.log(response)
                if (response['code'] === 200) {
                    setItems(response['data'])
                } else {
                    alert("Error 404: The item '" + item.name + "'is not in the database")
                }
            })
            .catch(err => {
                console.log(err);
            });
    }

    function editItemInput(item: Item) {
        setId(item.id)
        setName(item.name);
        setQuant(item.quant);
        setTags(item.tags);

        setEditItemPopupState(true);
    }

    function editItem() {
        // Send name, quant, tags with PUT request to server then update the local list
        fetch("http://localhost:5000/items?id=" + id + "&name=" + name + "&quant=" + quant + "&tags=" + tags,
            {
                "method": "PUT",
            }
        )
            .then(response => response.json())
            .then(response => {
                if (response['code'] === 200) {
                    setItems(response['data'])
                } else {
                    alert("Error 404: The item '" + name + "'is not in the database")
                }
            })
            .catch(err => {
                console.log(err);
            });

        setEditItemPopupState(false)
    }

    function plusOne(item: Item) {
        // Update the item by adding 1 to the quantity
        fetch("http://localhost:5000/items?id=" + item.id + "&name=" + item.name + "&quant=" + String(item.quant + 1) + "&tags=" + item.tags,
            {
                "method": "PUT",
            }
        )
            .then(response => response.json())
            .then(response => {
                if (response['code'] === 200) {
                    setItems(response['data'])
                } else {
                    alert("Error 404: The item '" + item.name + "'is not in the database")
                }
            })
            .catch(err => {
                console.log(err);
            });
    }

    function minusOne(item: Item) {
        // Update the item by subtracting 1 from the quantity
        fetch("http://localhost:5000/items?id=" + item.id + "&name=" + item.name + "&quant=" + String(item.quant - 1) + "&tags=" + item.tags,
            {
                "method": "PUT",
            }
        )
            .then(response => response.json())
            .then(response => {
                if (response['code'] === 200) {
                    setItems(response['data'])
                } else {
                    alert("Error 404: The item '" + item.name + "'is not in the database")
                }
            })
            .catch(err => {
                console.log(err);
            });
    }

}

interface Item {
    id: number;
    name: string;
    quant: number;
    tags: string;
}

export default App;
