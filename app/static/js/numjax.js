function eventListeners(){
    document.getElementById("user-input").addEventListener("submit", function(e) {
        e.preventDefault();
        nameInput = document.getElementsByName("name")[0].value;
        dateInput = document.getElementsByName("dob")[0].value;
        if (nameInput == '' && dateInput == '') {
            c = confirm("Both fields are empty. Continue?");
        }
        else if (dateInput == '') {
            c = confirm("Birthdate is empty. Continue?");
        }
        else if (nameInput == '') {
            c = confirm("Name field is empty. Continue?");
        } else {
            c = true;
        }
        if(c){
            this.submit();
        }
    });
}

function showKin(el){
    if (el.nextElementSibling.style.display == 'none') {
        el.nextElementSibling.style.display = 'grid';
    } else {
        el.nextElementSibling.style.display = 'none';
    }
}

window.onload = eventListeners();