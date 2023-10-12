function confirmDelete(event) {
    event.preventDefault();
    var uid = event.target.getAttribute('data-uid');
    if (confirm("Really want to delete this message?")) {
        chatSocket.send(JSON.stringify({"uid": uid}));  
    }
    location.reload();
}


function confirmDelete2(event) {
    let fr_uid_input = document.querySelector("#fr-uid-input");
    let delete_fr_button = document.querySelector("#submit-fr-uid");
    event.preventDefault();
    var fr_uid = event.currentTarget.getAttribute('fr-uid');
    if (confirm("Really want to delete this request?")) {
        fr_uid_input.value = fr_uid;
        delete_fr_button.click();
    };
}


function confirmDelete3(event) {
    let delete_friend_input = document.querySelector("#delete-friend-name");
    let delete_friend_button = document.querySelector("#submit-delete-friend");
    event.preventDefault();
    var friend_name = event.currentTarget.getAttribute('friend-name');
    if (confirm("Really want to delete this request?")) {
        delete_friend_input.value = friend_name;
        delete_friend_button.click();
    };
}


function confirmDelete4(event) {
    event.preventDefault();
    var uid = event.currentTarget.getAttribute('friend-message-uid');
    if (confirm("Really want to delete this message?")) {
        chatSocket2.send(JSON.stringify({"uid": uid}));  
    }
    location.reload();
}


function confirmDelete5(event) {
    let delete_link_url_input = document.querySelector("#delete-link-url");
    let delete_link_button = document.querySelector("#submit-delete-link");
    event.preventDefault();
    var link_url = event.currentTarget.getAttribute('link-url');
    if (confirm("Really want to delete this link?")) {
        delete_link_url_input.value = link_url;
        delete_link_button.click();
    };
}