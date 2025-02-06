# CSRF Test Cases
## 1. No CSRF Token
## 2. Empty CSRF Token
## 3. Accepting Random CSRF Token
## 4. CSRF token validation depeneds on request method
## 5. CSRF token is not Tied to user's session
## 6. CSRF where token is duplicated in cookie
Usually this type of implementation checks whether the cookie value is equal to CSRF token to perform the validation that is getting passed in the request. This is known as double submit cookie and can be used as a mitigation against CSRF vulnerability.<br>
Try inserting cookies in user's browser using vulnerability such as HTTP Header Injection to bypass such kind of implementation.
## 7. CSRF where Referer validation depends on header being present
Delete the Referer header entirely and observe that the request is  getting accepted or not. Include the below while creating CSRF PoC using Burp. It would prevent sending Referer header in the request.
```
meta name="referer" content="never"
```
## 8. CSRF with Broken Referer Validation
Include the below code in your PoC to check if Refere header can be bypassed. Remember to set Referrer:unsafe-url on attacker server.
```bash
history.pushstate("","","/?[Whitelisted_Domain]")
```
## 9. Same Site Lax Bypass via Method Override
Same Site Lax value doesn't allow cookie to be passed in cross request using POST method as it can trigger sensitive actions. However, if we change the request method to GET then we could possibly bypass this implementation. Also try adding __method=POST in GET request as some frameworks supports this parameter.
