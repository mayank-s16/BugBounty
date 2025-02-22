# OAuth Vulnerabilities
## Authentication bypass via OAuth implicit flow
When we get the token from the Oauth provider, this token along with the username/email would get passed to Client Application.<br>
Change the userid/email keeping the token same and repeat this request in repeater.<br>
If don't get any error and session idenfitiers are provided by the client app means it was vulnerable(Show response in browser).
