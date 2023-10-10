// variable
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let chatLog = document.querySelector("#chatLog");
let chatLog_container = document.getElementById('chatLog-container');

let hidden_container = document.querySelector("#hidden-container");
let hidden_container1 = document.querySelector("#hidden-container1");
let hidden_container2 = document.querySelector("#hidden-container2");
let hidden_container3 = document.querySelector("#hidden-container3");
let hidden_container4 = document.querySelector("#hidden-container4");

let chatSocket2 = null;
var friend_img_url = hidden_container.innerHTML.trim().toString();
var friend_name = hidden_container1.innerHTML.trim().toString();
var cur_user_img_url = hidden_container2.innerHTML.trim().toString();
var cur_user = hidden_container3.innerHTML.trim().toString();
var fr_uid = hidden_container4.innerHTML.trim().toString();


// add message
function add_message(user, message){
    if (user != cur_user){
        chatLog.innerHTML += `<li><div class="conversation-list" style="max-width: 40%;">
        <!-- HIS OR HER AVATAR -->
        <div class="chat-avatar"><img src=${friend_img_url} alt=""></div>
        <!-- HIS OR HER AVATAR -->
        <!-- CONTENT MAIN -->
        <div class="user-chat-content" style="max-width: 100%;">
            <div class="ctext-wrap">
                <!-- CONTENT & TIME -->
                <div class="ctext-wrap-content" style="max-width: 100%;">
                    <p class="mb-0" style="word-break:break-all;">${message}</p>
                </div>
                <!-- CONTENT & TIME -->
            </div>
            <!-- HIS OR HER NAME -->
            <div class="conversation-name">${user}</div>
        </div>
        <!-- CONTENT -->
    </div></li>`}
    else{        
        chatLog.innerHTML += `<li class="right"><div class="conversation-list" style="max-width: 40%;">
        <!-- HIS OR HER AVATAR -->
        <div class="chat-avatar"><img src=${cur_user_img_url} alt=""></div>
        <!-- HIS OR HER AVATAR -->
        <!-- CONTENT MAIN -->
        <div class="user-chat-content" style="max-width: 100%;">
            <div class="ctext-wrap">
                <!-- CONTENT & TIME -->
                <div class="ctext-wrap-content" style="max-width: 100%;">
                    <p class="mb-0" style="word-break:break-all; text-align: left;">${message}</p>
                </div>
                <!-- CONTENT & TIME -->
            </div>
            <!-- HIS OR HER NAME -->
            <div class="conversation-name">${user}</div>
        </div>
        <!-- CONTENT -->
    </div></li>`
    }
}


// connect
function connect() {
    chatSocket2 = new WebSocket("ws://" + window.location.host + "/ws/chat/chat/" + friend_name);
    // connect the WebSocket
    chatSocket2.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }
    // deal with connection error
    chatSocket2.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };
    // deal with message error 
    chatSocket2.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket2.close();
    }

    // send message
    chatSocket2.onmessage = function(e) {
        const data = JSON.parse(e.data);
        switch (data.type) {
            case "chat_message":
                add_message(data.user, data.message);
                break;
            default:
                console.error("Unknown message type!");
                break;
        }
        chatLog_container.scrollTop = chatLog.scrollHeight;
    }
    
}


// send if the button click
chatMessageSend.addEventListener('click', function(event){
    event.preventDefault();
    var content = chatMessageInput.value;
    console.log(content);
    chatMessageInput.value = "";
    chatSocket2.send(JSON.stringify({"message": content}));  
})


// connect and actions
connect();
chatLog_container.scrollTop = chatLog.scrollHeight;
chatMessageInput.focus();
// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};





