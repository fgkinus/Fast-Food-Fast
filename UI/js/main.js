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
    let temp = document.getElementsByTagName("template")[0];
    //get the img element from the template:
    item = temp.content.querySelector("img");

    //for each item in image folder
    for (let i=0;i<foodItems.length;i++){
        // create a new node based on the item
        let image = document.importNode(item,true);
        image.src =  path+foodItems[i]+'.jpg';
        //append item to list
        add_to_list(destination,image,'item-'+i)

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