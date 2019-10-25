var mac_address = document.querySelector('#macAddress').innerHTML;
console.log(mac_address);
var chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/monitoring/' + mac_address + '/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector('#chat-log').value += (message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
    document.querySelector('#chat-log').value += ('CATRACA DISCONECTADA' + '\n');

};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    };
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    setInterval(function(){
        chatSocket.send(JSON.stringify({'message': message}));
    }, 1000);
    messageInputDom.value = '';
};


