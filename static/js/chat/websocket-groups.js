// variable
let chatMessageInput = document.querySelector("#chatMessageInput");
chatMessageInput.focus();

let chatMessageSend = document.querySelector("#chatMessageSend");
let chatLog = document.querySelector("#chatLog");
let chatLog_container = document.getElementById('chatLog-container');

let chatSocket3 = null;
let hidden_container = document.querySelector("#hidden-container");
let hidden_container1 = document.querySelector("#hidden-container1");
let hidden_container2 = document.querySelector("#hidden-container2");
let hidden_container3 = document.querySelector("#hidden-container3");

var group_uid = hidden_container.innerHTML.trim().toString();
var cur_user = hidden_container1.innerHTML.trim().toString();
var cur_user_img_url = hidden_container2.innerHTML.trim().toString();
var user_img_urls = JSON.parse(hidden_container3.innerHTML);

// add message
function add_message(user, message){
    img_url = user_img_urls[user];
    var flag = 0;
    if (img_url == undefined && flag == 0) {
        location.reload();
        flag = 1;
    }
    if (user != cur_user){
        chatLog.innerHTML += `<li><div class="conversation-list" style="max-width: 40%";>
        <!-- HIS OR HER AVATAR -->
        <div class="chat-avatar"><img src=${img_url} alt=""></div>
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
    </div></li>`
    }
    else{        
        chatLog.innerHTML += `<li class="right"><div class="conversation-list" style="max-width: 40%;">
        <!-- HIS OR HER AVATAR -->
        <div class="chat-avatar"><img src=${img_url} alt=""></div>
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
    var hostname = window.location.host;
    var protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    chatSocket3 = new WebSocket(protocol + hostname + "/ws/chat/groups/" + group_uid + "/");
    // connect the WebSocket
    chatSocket3.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }
    // deal with connection error
    chatSocket3.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };
    // deal with message error 
    chatSocket3.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket3.close();
    }

    // send message
    chatSocket3.onmessage = function(e) {
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
    chatMessageInput.value = "";
    chatSocket3.send(JSON.stringify({"message": content}));  
})


// connect and actions
connect();
chatLog_container.scrollTop = chatLog.scrollHeight;

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};





