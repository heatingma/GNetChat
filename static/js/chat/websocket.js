// variable
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");
let a_cur_room = document.querySelector("#cur_room_name");
let chatLog = document.querySelector("#chatLog");
let chatLog_container = document.getElementById('chatLog-container');
let hidden_container = document.querySelector("#hidden-container");
let hidden_container2 = document.querySelector("#hidden-container2");
let chatSocket = null;
var room_name = a_cur_room.textContent.trim().toString();
var user_img_urls = JSON.parse(hidden_container.innerHTML);
var cur_user = hidden_container2.innerHTML.trim().toString()


// add message
function add_message(user, message){
    img_url = user_img_urls[user];
    var flag = 0;
    if (img_url == undefined && flag == 0) {
        location.reload();
        flag = 1;
    }
    if (user != cur_user){
        chatLog.innerHTML += `<li><div class="conversation-list">
        <!-- HIS OR HER AVATAR -->
        <div class="chat-avatar"><img src=${img_url} alt=""></div>
        <!-- HIS OR HER AVATAR -->
        <!-- CONTENT MAIN -->
        <div class="user-chat-content">
            <div class="ctext-wrap">
                <!-- CONTENT & TIME -->
                <div class="ctext-wrap-content">
                    <p class="mb-0">${message}</p>
                </div>
                <!-- CONTENT & TIME -->
                <!-- MESSAGE TOOLS -->
                <div class="dropdown align-self-start">
                    <a class="dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="ri-more-2-fill"></i>
                    </a>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="#">Copy <i class="ri-file-copy-line float-right text-muted"></i></a>
                        <a class="dropdown-item" href="#">Save <i class="ri-save-line float-right text-muted"></i></a>
                        <a class="dropdown-item" href="#">Forward <i class="ri-chat-forward-line float-right text-muted"></i></a>
                        <a class="dropdown-item" href="#">Delete <i class="ri-delete-bin-line float-right text-muted"></i></a>
                    </div>
                </div>
                <!-- MESSAGE TOOLS -->
            </div>
            <!-- HIS OR HER NAME -->
            <div class="conversation-name">${user}</div>
        </div>
        <!-- CONTENT -->
    </div></li>`}
    else{        
        chatLog.innerHTML += `<li class="right"><div class="conversation-list">
        <!-- HIS OR HER AVATAR -->
        <div class="chat-avatar"><img src=${img_url} alt=""></div>
        <!-- HIS OR HER AVATAR -->
        <!-- CONTENT MAIN -->
        <div class="user-chat-content">
            <div class="ctext-wrap">
                <!-- CONTENT & TIME -->
                <div class="ctext-wrap-content">
                    <p class="mb-0">${message}</p>
                </div>
                <!-- CONTENT & TIME -->
                <!-- MESSAGE TOOLS -->
                <div class="dropdown align-self-start">
                    <a class="dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="ri-more-2-fill"></i>
                    </a>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="#">Copy <i class="ri-file-copy-line float-right text-muted"></i></a>
                        <a class="dropdown-item" href="#">Save <i class="ri-save-line float-right text-muted"></i></a>
                        <a class="dropdown-item" href="#">Forward <i class="ri-chat-forward-line float-right text-muted"></i></a>
                        <a class="dropdown-item" href="#">Delete <i class="ri-delete-bin-line float-right text-muted"></i></a>
                    </div>
                </div>
                <!-- MESSAGE TOOLS -->
            </div>
            <!-- HIS OR HER NAME -->
            <div class="conversation-name">${user}</div>
        </div>
        <!-- CONTENT -->
    </div></li>`
    }
}


// onlineUsersSelectorAdd
function onlineUsersSelectorAdd(user){
    if (document.querySelector("option[value='" + user + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = user;
    newOption.innerHTML = user;
    onlineUsersSelector.appendChild(newOption);
}


// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(user) {
    let oldOption = document.querySelector("option[value='" + user + "']");
    if (oldOption !== null) oldOption.remove();
}

// connect
function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + room_name + "/");
    // connect the WebSocket
    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }
    // deal with connection error
    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };
    // deal with message error 
    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
    // send message
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        switch (data.type) {
            case "chat_message":
                add_message(data.user, data.message);
                break;
            case "user_list":
                for (let i = 0; i < data.users.length; i++) 
                    onlineUsersSelectorAdd(data.users[i]);
                break;
            case "user_join":
                onlineUsersSelectorAdd(data.user);
                break;
            case "user_leave":
                onlineUsersSelectorRemove(data.user);
                break;
            case "private_message":
                chatLog.value += "PM from " + data.user + ": " + data.message + "\n";
                break;
            case "private_message_delivered":
                chatLog.value += "PM to " + data.target + ": " + data.message + "\n";
                break;
            default:
                console.error("Unknown message type!");
                break;
        }
        chatLog_container.scrollTop = chatLog.scrollHeight;
    }
    
}

connect();
chatLog_container.scrollTop = chatLog.scrollHeight;

chatMessageInput.focus();
// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// send if the button click
chatMessageSend.addEventListener('click', function(event){
    event.preventDefault();
    var content = chatMessageInput.value;
    chatMessageInput.value = "";
    chatSocket.send(JSON.stringify({"message": content,}));  
})




