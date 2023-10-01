function confirmDelete(event) {
    event.preventDefault();
    var uid = event.target.getAttribute('data-uid');
    if (confirm("Really want to delete this message?")) {
        chatSocket.send(JSON.stringify({"uid": uid}));  
    }
    location.reload();
}