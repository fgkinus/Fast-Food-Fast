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
var foodItems = ["burgerFriesSoda", "drumsticks", 'fries', "meatballs", "pie", "pizza", "rools",
    "sandwich", "vege_burger"];

// load templates to make them visible
function showContent(destination) {
    let path  = '../img/';

    //get the template element:
    let temp = document.querySelector("#food-item");

        // temp.content.querySelector("img");

    //for each item in image folder
    for (let i=0;i<foodItems.length;i++){
        //get the element from the template:
        let item = document.importNode(temp.content,true);
        // create a new node based on the item
        let image = item.querySelector("img");
        image.src =  path+foodItems[i]+'.jpg';

        let name= item.querySelector("h5");
        name.textContent = foodItems[i];

        let cost = item.querySelector("p");
        // cost.textContent  = "";
        //append item to list
        add_to_list(destination,item,'item-'+i)

        // document.body.appendChild(image);

    }
    // let clon = temp.content.cloneNode(true)
}

// append items to list
function add_to_list(ListID,item,itemID) {
    let ul,li;
    ul  =document.getElementById(ListID);
    li  = document.createElement('li')
    li.appendChild(item);
    li.setAttribute("id",itemID);
    ul.appendChild(li);
}