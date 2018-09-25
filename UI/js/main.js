// a function to set open tabs
function openTab(evt, tabName) {
    // variables
    let i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tab_titles");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// set default tab on page load
function set_active_tab(ID) {
    // set the active tab by selecting it on page load
    document.getElementById(ID).click()
}

// a list of all food items
var foodItems = {
    "burgerFriesSoda": 2000, "drumsticks": 350, 'fries': 200, "meatballs": 350, "pie": 900, "pizza": 1500, "rools": 750,
    "sandwich": 150, "vege_burger": 250
};

// load templates to make them visible
function showContent(destination) {
    // empty the destination object
    //get the template element:
    let temp = document.querySelector("#food-item2");

    // items
    let items = create_items(foodItems);
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

        // document.body.appendChild(image);

    }
    // let clon = temp.content.cloneNode(true)
}

function showFoodlist(destination) {
    //get the template element:
    let temp = document.querySelector("#MenuItem");

    // items
    let items = create_items(foodItems);
    let keys = Object.keys(items);
    //for each item in image folder
    for (let i = 0; i < keys.length; i++) {
        //get the element from the template:
        let clone = document.importNode(temp.content, true);
        // create a new node based on the item
        let cols = clone.querySelectorAll("td");

        cols[0].textContent = i;

        let image = document.createElement('img');
        image.src = items[keys[i]].image;
        cols[1].appendChild(image);

        let name = cols[2];
        name.textContent = items[keys[i]].name;

        let cost = cols[3];
        cost.textContent = items[keys[i]].price;

        let button = document.createElement("button");
        button.setAttribute("id", 'item-' + i);
        button.setAttribute('onClick', 'pop_up("popup2")');
        cols[4].appendChild(button);
        //append item to list
        add_to_table(destination, clone, 'item-' + i);

        // document.body.appendChild(image);

    }
    // let clon = temp.content.cloneNode(true)
}

// an array of all orders
let Orders = [];

function ShowOrders(destination) {
    let temp = document.querySelector("#order");
    // items
    for (let i = 0; i < Orders.length; i++) {
        let order = Orders[i];

        //get the element from the template:
        let clone = document.importNode(temp.content, true);
        // get all table columns
        let cols = clone.querySelectorAll("td");

        // assign value
        cols[0].textContent = order.id;
        cols[1].textContent = order.item_id;
        cols[2].textContent = Object.keys(foodItems)[order.item_id[5]];
        cols[3].textContent = order.quantity;
        cols[4].textContent = order.location;
        cols[5].textContent = order.time;

        btn = document.createElement('button');
        btn.setAttribute("class", "btn");
        cols[6].appendChild(btn);

        add_to_table(destination, clone, 'order-' + i);
    }

}

// append items to list
function add_to_list(ListID, item, itemID) {
    let ul, li;
    ul = document.getElementById(ListID);
    li = document.createElement('li')
    li.appendChild(item);
    li.setAttribute("id", itemID);
    ul.appendChild(li);
}

function add_to_table(TableID, item, itemID) {
    let table, tr;
    table = document.getElementById(TableID);
    tr = document.createElement('tr');
    tr.appendChild(item);
    tr.setAttribute("id", itemID);
    table = table.querySelector("tbody");
    table.appendChild(tr);
}

function add_to_div(DivID, item, itemID) {
    let div1, div2;
    div1 = document.getElementById(DivID);
    div2 = document.createElement('div');
    div2.appendChild(item);
    div2.setAttribute("id", itemID);
    div1.append(div2);
}


// food object constructor
function FoodItem(id, name, price, image_url) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.image = image_url;
}

// Order object constructor
function Order(id, item_ID, quantity, location) {
    this.id = id;
    this.item_id = item_ID;
    this.quantity = quantity;
    this.location = location;
    this.time = Date();
}

// order status object
function Order_status(ID, order_id, status) {
    this.id = ID;
    this.order_ID = order_id;
    this.status = staus;
    this.time = Date();
}

function create_items(items_list) {
    let items = [];
    let keys = Object.keys(items_list);
    for (let i = 0; i < keys.length; i++) {
        let name = keys[i];
        let price = items_list[name];
        let url = "../img/" + name + ".jpg";
        let item = new FoodItem(i, name, price, url);
        items.push(item)
    }
    return items;
}

// add orders to the Orders array
function AddOrder(Id) {
    let location;
    // prompt for location
    let quantity = prompt("Please enter your order quantity", '1');
    // validate input
    if (isNullOrWhitespace(quantity) || isNaN(parseInt(quantity))) {
        alert("please enter a valid quantity!!");
        return;
    }

    // parse to integer
    quantity = parseInt(quantity);
    // COLLECT DELIVERY LOCATION
    if (quantity >= 1 || !isNaN(quantity)) {
        location = prompt("Where will the delivery be made?");
    }
    // validate input
    if (isNullOrWhitespace(location)) {
        alert("enter a valid location!!");
        return;
    }

    let order_id = Orders.length + 1;


    let order = new Order(order_id, Id, quantity, location);
    Orders.push(order);
    return Orders;
}

// checks that input is Null or whitespace
function isNullOrWhitespace(input) {
    return !input || !input.trim();
}

// modal pop up
function pop_up(Id) {
    let item = document.getElementById(Id);
    item.style.display = "block";
}

// close popup
function close_pop_up(ID) {
    let item = document.getElementById(ID);
    item.style.display = "none";
}