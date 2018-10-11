//Declare global varialbles here
// a list of api endpoint urls
let urls;
urls = {
    "menulist": "https://fast-food-really-fast.herokuapp.com/API/v2/menu/",
    // "menulist": "http://localhost:5000/API/v2/menu/",
    // "login": "https://fast-food-really-fast.herokuapp.com/API/v2/auth/login",
    "login": "http://localhost:5000/API/v2/auth/login",
    "signup": "http://localhost:5000/API/v2/auth/signup"
};


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
function showMenuList(destination, alerts_destination) {
    // empty the destination object
    //get the template element:
    let temp = document.querySelector("#food-item2");

    // fetch the items list
    let request_body = {method: 'GET'};
    fetch_function_v2(urls.menulist, request_body, alerts_destination).then(menu_items => {
        // items
        let items = create_items(menu_items.items);
        let keys = Object.keys(items);

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
            button.setAttribute("id", 'item-' + i);
            //append item to list
            // add_to_list(destination, clone, 'item-' + i);

            add_to_div(destination, clone, 'item-' + i);
        }

    });


    // let clon = temp.content.cloneNode(true)
}

function create_items(items_list) {
    //create menu item objects and append them to a list
    let items = [];
    items_list.forEach(item => {
        let name = item.name;
        let price = item.price;
        let url = "../img/" + name + ".jpg";
        let new_item = new FoodItem(item.id, name, price, url);
        items.push(new_item)
    });
    return items;

}

// authenticate and register new users

// #login user
function login() {
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
    fetch_function_v3(urls.login, request_body, "errors").then(request_response => {
        console.log(request_response);
        // create an acess token cookie
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
        alerter("The passwords entered do not match", 'errors')
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

// call scripts
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