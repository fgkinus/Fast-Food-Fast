//Declare global varialbles here
// a list of api endpoint urls
let urls;
urls = {
    "menulist": "https://fast-food-really-fast.herokuapp.com/api/v2/menu/",
};


// declare the Objects here with their attributes
// food items object
function FoodItem(id, name, price, image_url) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.image = image_url;
}


//Declare Generic reusable functions here
fetch_function = function (url, payload) {
    // a function to fetch and log all  requests
    // makes use of the fetch api

    // create a request object
    let myRequest = new Request(url, payload);
    // fetch the request response
    return fetch(myRequest)
        .then((result) => result.json())
        .then(function (data) {
            console.log(data);
            return data;
        })
        .catch(function (data) {
            console.log(data);
            throw new Error("Could not complete request!!!");
        });
};




// Declare all case specific functions here
// list all menu items in the DB
function showMenuList(destination) {
    // empty the destination object
    //get the template element:
    let temp = document.querySelector("#food-item2");

    // fetch the items list
    let request_body = {method: 'GET'};
    fetch_function(urls.menulist, request_body).then(menu_items => {
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

