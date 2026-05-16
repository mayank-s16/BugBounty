### Basic password reset poisoning
Observe that you can change the Host header to an arbitrary value and still successfully trigger a password reset. Set Host header to the attacker server address and change the email to victim's email. The email would be triggered to victim's user with password reset link with host as attacker address. Once the victim clicks on the link attacker gets to know about the password reset token through wehich can reset the password of user.
### Host header authentication bypass
* Try and browse to /admin. You do not have access, but notice the error message, which reveals that the panel can be accessed by local users.
* Send the GET /admin request to Burp Repeater.
* In Burp Repeater, change the Host header to localhost and send the request. Observe that you have now successfully accessed the admin panel, which provides the option to delete different users.
