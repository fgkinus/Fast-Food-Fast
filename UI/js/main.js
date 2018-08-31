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
    let path = '../img/';

    //get the template element:
    let temp = document.querySelector("#food-item");

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
        cost.textContent  = items[keys[i]].price;
        //append item to list
        add_to_list(destination, clone, 'item-' + i)

        // document.body.appendChild(image);

    }
    // let clon = temp.content.cloneNode(true)
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

// food object constructor
function FoodItem(id, name, price, image_url) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.image = image_url;
}

// Order object constructor
function Order(id, item_ID, quntity, location) {
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


// test function
console.log(create_items(foodItems));