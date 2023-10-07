function confirmDelete(event) {
    event.preventDefault();
    var uid = event.target.getAttribute('data-uid');
    if (confirm("Really want to delete this message?")) {
        chatSocket.send(JSON.stringify({"uid": uid}));  
    }
    location.reload();
}


let fr_uid_input = document.querySelector("#fr-uid-input");
let delete_fr_button = document.querySelector("#submit-fr-uid");

function confirmDelete2(event) {
    event.preventDefault();
    var fr_uid = event.currentTarget.getAttribute('fr-uid');
    if (confirm("Really want to delete this request?")) {
        fr_uid_input.value = fr_uid;
        delete_fr_button.click();
    };
}