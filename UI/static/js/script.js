//Declare global varialbles here
// a list of api endpoint urls
// let domain = "https://fast-food-really-fast.herokuapp.com";
let domain = "http://localhost:5000";

let urls = {
    "menulist": domain + "/API/v2/menu/",
    // "menulist": "http://localhost:5000/API/v2/menu/",
    "login": domain + "/API/v2/auth/login",
    "login": domain + "/API/v2/auth/login",
    "signup": domain + "/API/v2/auth/signup",
    'signup_admin': domain + "/API/v2/auth/register-admin",
    'add_order': domain + "/API/v2/orders/",
    'edit_order': domain + "/API/v2/orders/",
    'delete_order': domain + "/API/v2/orders/",
    'history': domain + "/API/v2/orders/history",
    'get_all_statuses': "/API/v2/orders/response"
};

let status_key;

let order_responses;

// declare the Objects here with their attributes
// food items object
function FoodItem(id, name, price, image_url) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.image = image_url;
}

// alert box close
close_alerts = function () {
    let close = document.getElementsByClassName("closebtn");
    let i;
    // #loop through close buttons closing them
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            let div = this.parentElement;
            div.style.opacity = "0";
            setTimeout(function () {
                div.style.display = "none";
            }, 600);
        }

    }
};
alerter = function (message, alerts_destination) {
    let temp = document.getElementById('alert-box');
    let alertbox = document.importNode(temp.content, true);
    let alertbox_clone = alertbox.cloneNode(true);
    let text_content = alertbox_clone.querySelector('p');
    text_content.textContent = message;
    let alerts = document.getElementById(alerts_destination);
    alerts.innerHTML = "";
    alerts.appendChild(alertbox_clone);
    close_alerts();
};

fetch_function_v2 = function (url, payload, alerts_destination) {
    // a function to fetch and log all  requests
    // makes use of the fetch api

    // create a request object
    let myRequest = new Request(url, payload);
    // fetch the request response
    return fetch(myRequest)
        .then(function (result) {
                if (result.ok) {
                    return result.json();
                } else {
                    let temp = result.json().then(function (res) {
                            alerter(res.message, alerts_destination);
                            throw new Error(res.message);
                        }
                    )
                }

            }
        )
        .then(function (data) {
            // console.log(data);
            return data;
        })
        .catch(function (data) {
            console.log(data);
            alerter(data.message);
        });
};

fetch_function_v3 = function (url, payload, alerts_destination) {
    // a function to fetch and log all  requests
    // makes use of the fetch api

    // create a request object
    let myRequest = new Request(url, payload);
    // fetch the request response
    return fetch(myRequest)
        .then(function (result) {
                if (result.ok) {
                    return result.json();
                } else {
                    let temp = result.json().then(function (res) {
                            alerter(res.message, alerts_destination);
                            if (res.hasOwnProperty('errors') || res.hasOwnProperty('Error')) {
                                console.log(res);
                                if (res.errors.hasOwnProperty('email')) {
                                    alerter(res.errors.email, alerts_destination);
                                }
                                if (res.errors.hasOwnProperty('password')) {
                                    alerter(res.errors.password, alerts_destination);
                                }
                            }
                            throw new Error(res.message);
                        }
                    )
                }

            }
        )
        .then(function (data) {
            // console.log(data);
            return data;
        })
        .catch(function (data) {
            console.log("request exception caught!!!");
            console.log(data);
            alerter(data.message);
        });
};

function setCookie(cname, cvalue, exdays) {
    let d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// function checkCookie(cname) {
//     let username = getCookie(cname);
//     if (username != "") {
//         alert("Welcome again " + username);
//     } else {
//         username = prompt("Please enter your name:", "");
//         if (username != "" && username != null) {
//             setCookie("username", username, 365);
//         }
//     }
// }

// Declare all case specific functions here
// list all menu items in the DB
async function showMenuList(destination, alerts_destination) {

    // empty the destination object
    //get the template element:
    let temp = document.querySelector("#food-item2");

    // show loading modal
    pop_up('popup-loader');
    // fetch the items list
    let request_body = {method: 'GET'};
    await fetch_function_v2(urls.menulist, request_body, alerts_destination).then((data) => {
        // items
        let items = create_items(data.items);
        foodItems = data.items;
        // console.log(foodItems);
        let keys = Object.keys(items);
        console.log(items);

        //for each item in image folder
        for (let i = 0; i < keys.length; i++) {
            //get the element from the template:
            let clone = document.importNode(temp.content, true);
            // create a new node based on the item
            let image = clone.querySelector("img");
            image.src = items[keys[i]].image;

            let name = clone.querySelector("h5");
            name.textContent = items[keys[i]].name;

            let cost = clone.querySelector("p");
            cost.textContent = items[keys[i]].price;

            let button = clone.querySelector("#details");
            button.setAttribute("id", 'item-' + items[i].id);
            //append item to list
            // add_to_list(destination, clone, 'item-' + i);

            add_to_div(destination, clone, 'item-' + i);
        }

    }).finally(function () {
        //close modal
        close_pop_up('popup-loader');
    });


}

function create_items(items_list) {
    //create menu item objects and append them to a list
    let items = [];
    items_list.forEach(item => {
        let name = item.name;
        let price = item.price;
        let url = "../static/img/" + name + ".jpg";
        let new_item = new FoodItem(item.id, name, price, url);
        items.push(new_item)
    });
    return items;

}

// authenticate and register new users

// #login user
async function login() {

    let username = document.getElementById('username');
    let password = document.getElementById('password');
    let data = {
        email: username.value,
        password: password.value
    };

    let request_body = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    };
    // create an acess token cookie
    pop_up('popup-loader');
    await fetch_function_v3(urls.login, request_body, "errors").then(request_response => {
        console.log(request_response);
        // create an access token cookie
        setCookie('auth', request_response.access_token, 1);
        setCookie('username', request_response.details.username, 1);
        console.log(getCookie('auth'));
        console.log(getCookie('username'));
        document.querySelector('form').submit();
        if (request_response.details.isadmin) {
            window.location.href = 'admin-dashboard.html'
        } else {
            window.location.href = 'user-dashboard.html'
        }
    }).finally(function () {
        //close modal
        close_pop_up('popup-loader');
    });


}

// signup new user
function signup() {
    let username = document.getElementById('username');
    let password = document.getElementById('password');
    let first_name = document.getElementById('first-name');
    let second_name = document.getElementById('second-name');
    let email = document.getElementById('email');
    let confirm_password = document.getElementById('confirm-password');

    // validate that both emails are the same
    if (!(password.value === confirm_password.value)) {
        alerter("The passwords entered do not match", 'errors');
        return
    }

    // body
    data = {
        username: username.value,
        password: password.value,
        first_name: first_name.value,
        second_name: second_name.value,
        email: email.value,
        confirm_password: confirm_password.value,
        surname: username.value
    };
    console.log(data);

    // request body
    let request_body = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        },
    };

    // make the request to the sever
    fetch_function_v3(urls.signup, request_body, "errors").then(request_response => {
        alerter(request_response.Message, 'errors');
        // redirect to login page
        window.location.href = 'login.html'    // redirect to login page
    });

}


//register new admin
function signup_admin() {
    let username = document.getElementById('username');
    let password = document.getElementById('password');
    let first_name = document.getElementById('first-name');
    let second_name = document.getElementById('second-name');
    let email = document.getElementById('email');

    // body
    data = {
        username: username.value,
        password: password.value,
        first_name: first_name.value,
        second_name: second_name.value,
        email: email.value,
        surname: username.value
    };
    console.log(data);

    let request_body = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };
    console.log(request_body);
    pop_up('popup-loader');
    // make the request to the sever
    fetch_function_v3(urls.signup_admin, request_body, "errors").then(request_response => {
        alerter(request_response.Message, 'errors');
        // redirect to login page
        alerter("new admin added", 'errors');
        // window.location.href = '#'    // redirect to login page
    }).finally(function () {
        close_pop_up('popup-loader');
    });

}

// add order
async function add_new_order(order) {
    let data = {
        item: get_item_by_id(order.item_id).id,
        quantity: order.quantity,
        location: order.location
    };
    let request_body = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };
    await fetch_function_v3(urls.add_order, request_body, "order_alerts").then(request_response => {
        console.log(request_response);
    }).finally(function () {
        console.log("order added");
    })
}

//checkout
async function checkout() {
    // show loading modal
    pop_up('popup-loader');
    if (Orders.length <= 0) {
        alerter("There are no orders to display.Please add some", 'order_alerts');
        console.log("No orders in the log!!!");
        close_pop_up('popup-loader');
        return
    }
    await Orders.forEach(function (order) {
        add_new_order(order).then(function () {
            // remove order from orders array
            let index = Orders.indexOf(order);
            if (index !== -1) Orders.splice(index, 1);
        })
    });

    //now empty the checkout list
    let tb = document.getElementById('List-orders');
    while (tb.rows.length > 1) {
        tb.deleteRow(1);
    }
    close_pop_up('popup-loader');
    alerter("Your orders have been made", 'order_alerts');
    alert("Orders made");
};

// view order history
function fetch_order_history() {
    let request_body = {
        method: 'GET',
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };

    pop_up('popup-loader');
    // make the request to the sever
    fetch_function_v3(urls.history, request_body, "history_alerts").then(request_response => {
        // console.log(request_response);
        let History = request_response.history;
        ShowOrdersHistory('List-prev-orders', History);

    }).finally(function () {
        close_pop_up('popup-loader');
    });
}

function ShowOrdersHistory(destination, History) {
    // empty the destination
    let tb = document.getElementById(destination);
    while (tb.rows.length > 1) {
        tb.deleteRow(1);
    }

    let temp = document.querySelector("#order");
    let item_id_sub = 'item-';
    // items
    for (let i = 0; i < History.length; i++) {
        let history = History[i];

        //get the element from the template:
        let clone = document.importNode(temp.content, true);
        // get all table columns
        let cols = clone.querySelectorAll("td");


        // assign value
        cols[0].textContent = history.id;
        cols[1].textContent = item_id_sub + history.item;
        cols[2].textContent = get_item_by_id(item_id_sub + history.item).name;
        cols[3].textContent = history.quantity;
        cols[4].textContent = history.location;
        cols[5].textContent = '';
        cols[6].textContent = history.created;

        // wrap action in an inline span
        let sp = document.createElement('span');

        // add buttons
        let btn1 = document.createElement('button');
        btn1.setAttribute("class", "btn1");
        btn1.setAttribute("id", "his" + history.id);
        btn1.setAttribute("onclick", 'cancelOrder2(this.id);');
        btn1.textContent = 'delete';

        //
        let btn2 = document.createElement('button');
        btn2.setAttribute("class", "btn1");
        btn2.textContent = 'edit';

        // apdend buttons to span
        // sp.appendChild(btn1);
        // sp.appendChild(btn2);

        //
        cols[7].appendChild(btn1);
        cols[7].appendChild(btn2);

        add_to_table(destination, clone, 'order-' + i);
    }

}

//add new menu item
async function add_menu_item() {

    let name = document.getElementById('item-name');
    let price = document.getElementById('price');

    let data = {
        name: name.value,
        price: price.value
    };

    let request_body = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };
    // create an acess token cookie
    console.log(data);
    console.log(request_body);

    pop_up('popup-loader');
    await fetch_function_v3(urls.menulist, request_body, "add_item_alerts").then(request_response => {
        console.log(request_response);

    }).finally(function () {
        //close modal
        close_pop_up('popup-loader');
    });


}

//
// view order history
function fetch_orders() {
    let request_body = {
        method: 'GET',
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };

    pop_up('popup-loader');
    // make the request to the sever
    fetch_function_v2(urls.add_order, request_body, "history_alerts").then(request_response => {
        let Orders = request_response.orders;
        console.log(Orders);
        ShowAllOrders('orders_list', Orders);

    }).finally(function () {
        close_pop_up('popup-loader');
    });
}

function ShowOrders(destination, orders = Orders) {
    // empty the destination
    let tb = document.getElementById(destination);
    let temp_name;
    while (tb.rows.length > 1) {
        tb.deleteRow(1);
    }

    let temp = document.querySelector("#order");
    let item_id_sub = 'item-';

    // items
    for (let i = 0; i < orders.length; i++) {
        let history = orders[i];
        console.log(history);

        // now check that object has attribute
        if (history.hasOwnProperty('item')) {
            console.log(item_id_sub + history.item);
            temp_name = item_id_sub + history.item;
        } else if (history.hasOwnProperty('item_id')) {
            temp_name = history.item_id;
            console.log(temp_name);
        }
        if (history.hasOwnProperty('time')) {
            history.created = history.time;
        }

        //get the element from the template:
        let clone = document.importNode(temp.content, true);
        // get all table columns
        let cols = clone.querySelectorAll("td");


        // assign value
        cols[0].textContent = history.id;
        cols[1].textContent = temp_name;
        cols[2].textContent = get_item_by_id(temp_name).name;
        cols[3].textContent = history.quantity;
        cols[4].textContent = history.location;
        cols[5].textContent = history.status;
        cols[6].textContent = history.created;
        cols[7].textContent = '';

        btn1 = document.createElement('button');
        btn1.setAttribute("class", "btn");
        btn1.setAttribute("id", "btn" + history.id);
        btn1.setAttribute("onclick", 'cancelOrder(this.id);');
        btn1.textContent = 'cancel';
        cols[7].appendChild(btn1);

        add_to_table(destination, clone, 'order-' + i);
    }

}

function ShowAllOrders(destination, orders = Orders) {
    // empty the destination
    let tb = document.getElementById(destination);
    let temp_name;
    while (tb.rows.length > 1) {
        tb.deleteRow(1);
    }

    let temp = document.querySelector("#order");
    let item_id_sub = 'item-';

    // items
    for (let i = 0; i < orders.length; i++) {
        let history = orders[i];
        // console.log(history);

        // now check that object has attribute
        if (history.hasOwnProperty('item')) {
            // console.log(item_id_sub + history.item);
            temp_name = item_id_sub + history.item;
        } else if (history.hasOwnProperty('item_id')) {
            temp_name = history.item_id;
            console.log(temp_name);
        }
        if (history.hasOwnProperty('time')) {
            history.created = history.time;
        }

        //get the element from the template:
        let clone = document.importNode(temp.content, true);
        // get all table columns
        let cols = clone.querySelectorAll("td");


        // assign value
        cols[0].textContent = history.id;
        cols[1].textContent = temp_name;
        cols[2].textContent = get_item_by_id(temp_name).name;
        cols[3].textContent = history.quantity;
        cols[4].textContent = history.location;
        cols[5].textContent = history.status;
        cols[6].textContent = history.created;
        cols[7].textContent = '';

        let sp = document.createElement('span');
        sp.setAttribute("class", "three_buttons");

        let btn1 = document.createElement('button');
        btn1.setAttribute("class", "btn1");
        btn1.setAttribute("id", "pro" + history.id);
        btn1.setAttribute("onclick", 'submit_response(this.id);');
        btn1.textContent = 'processing';

        let btn2 = document.createElement('button');
        btn2.setAttribute("class", "btn1");
        btn2.setAttribute("id", "can" + history.id);
        btn2.setAttribute("onclick", 'submit_response(this.id);');
        btn2.textContent = 'cancel';

        let btn3 = document.createElement('button');
        btn3.setAttribute("class", "btn1");
        btn3.setAttribute("id", "app" + history.id);
        btn3.setAttribute("onclick", 'submit_response(this.id);');
        btn3.textContent = 'approve';

        cols[7].appendChild(btn1);
        cols[7].appendChild(btn2);
        cols[7].appendChild(btn3);


        // cols[7].appendChild(sp);

        add_to_table(destination, clone, 'order-' + i);
    }

}

// delete the order
async function deleteOrder(order_id) {
    let data = {
        order_id: order_id
    };
    let request_body = {
        method: 'DELETE',
        body: JSON.stringify(data),
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };

    let res = prompt("are you sure you want to delete the menu Item \n enter Yes to delete", "Yes");
    if (res === "Yes") {
        // make the request
        await fetch_function_v3(urls.delete_order + data.order_id, request_body, "history_alerts").then(request_response => {
            console.log(request_response);
        }).finally(function () {
            console.log("order deleted");
            alerter("order deleted.", "history_alerts");
        })
    } else {
        throw new Error("Order Not deleted!!!");
    }
}

function cancelOrder(btn_id) {
    let button = document.getElementById(btn_id);
    let cell = button.parentNode;
    let row = cell.parentNode;

    // now remove the order from the list
    let name = button.getAttribute('id');
    let number = parseInt(name.substring(3));
    Orders.splice(number - 1, 1);

    // remove the row from the display
    row.remove();
}

function cancelOrder2(btn_id) {
    let button = document.getElementById(btn_id);
    let cell = button.parentNode;
    let row = cell.parentNode;

    let order_id, cells;
    cells = row.children;
    order_id = cells[0].textContent;
    order_id = parseInt(order_id);

    // delete the order from the database
    deleteOrder(order_id).then(function () {
        // remove the row from the display
        row.remove();
    }).catch(function () {
        console.log("Not deleted!!!")
    });

}


// log out the authenticated user
function logOut() {
    let token = getCookie('auth');
    setCookie('auth', null, 0);
    alert("Good bye . Thank you for choosing us")
}

// fetch all order responses
async function get_all_status() {
    let request_body = {
        method: 'GET',
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };

    // get urls
    await fetch_function_v3(urls.get_all_statuses, request_body, "page_alerts").then(request_response => {
        // console.log(request_response);
        order_responses = request_response.responses;
        // console.log(order_responses);
    }).finally(function () {
        console.log("all order status fetched!!!")
    })
}

// get order_status by id
function get_order_status_id(id) {
    let response;
    order_responses.forEach(function (res) {
        if (res.id === id) {
            response = res;
        }
    });
    return response;
}

function get_order_status_desc(desc) {
    let response;
    order_responses.forEach(function (res) {
        if (res.description === desc) {
            response = res;
        }
    });
    return response;
}

//submit response
async function submit_response(btn_id) {
    let button = document.getElementById(btn_id);
    let cell = button.parentNode;
    let row = cell.parentNode;

    let order_id, cells;
    cells = row.children;
    order_id = cells[0].textContent;
    order_id = parseInt(order_id);

    // the request payload
    let status = status_key[btn_id.substring(0, 3)];
    let data = {
        response: status,
        order_id: order_id
    };
    console.log(data);

    let request_body = {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: new Headers(
            {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + getCookie('auth'),
            }
        ),
    };

    pop_up('popup-loader');
    await fetch_function_v3(urls.edit_order + data.order_id, request_body, "page_alerts").then(request_response => {
        console.log(request_response);

    }).finally(function () {
        //close modal
        close_pop_up('popup-loader');
        fetch_orders()
    });

}

// call onsubmit event handlers scripts
try {
    document.querySelector('#login-form2').onsubmit = function () {
        try {
            console.log("attempting login!");
            login();
            console.log("logged in!!")
        } catch (e) {
            // just trying again for the sake of it
            login()
        }
    };
} catch (e) {
    console.log()
}

try {
    document.querySelector('#registration_form').onsubmit = function () {
        try {
            console.log("attempting registration");
            signup();
            console.log("registered")
        } catch (e) {
            // just trying again for the sake of it
            signup()
        }
    };
}
catch (e) {
    console.log()
}

try {
    document.querySelector('#register_admin').onsubmit = function () {
        try {
            console.log("attempting registration");
            signup_admin();
            console.log("registered")
        } catch (e) {
            // just trying again for the sake of it
            signup_admin()
        }
    };
}
catch (e) {
    console.log()
}

try {
    document.querySelector('#add_menuitem_form').onsubmit = function () {
        try {
            console.log("attempting to add menuitem");
            add_menu_item();
        } catch (e) {
            // just trying again for the sake of it
            add_menu_item();
        }
    };
}
catch (e) {
    console.log()
}

try {
    window.onload = function () {
        get_all_status().then(function () {
            status_key = {
                'pro': get_order_status_desc('Processing').id,
                'app': get_order_status_desc("Approved").id,
                'can': get_order_status_desc("Cancelled").id
            };
        });
    }
} catch (e) {
    console.log()
}