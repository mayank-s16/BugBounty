# JWT Test Cases
BurpSuite Extension: JWT Editor
## 1. Lack of Signature Verification
## 2. None Algorithm
## 3. Weak Signing Key Bruteforcing (Symmetric)
Works only for symmetric encryption algorithm (HS256)<br>
*Tool Reference: https://github.com/mayank-s16/BugBounty/blob/main/JWT/jwt_cracker.py*
```bash
python jwt_cracker.py --token TOKEN --wordlist WORDLIST
```
## 4. JWK parameter Injection (Asymmetric)
* Application does accept arbitrary injected JWK value and it works for  Asymmetric algorithm e.g. RS256. 
* The JWT would be signed by equilvalent private key of the public key which we embedded in the JWT.
* Application would verify it from the public key again and provides us the access.
* Generate RSA key using JWT Editor Extension and select Attack > Embedded JWK.
## 5. JKU parameter Injection (Asymmetric)
### Setting up Attacker Server
* From where the key would be fetched, we can include our own hosted keys.
* Generate RSA Key copy public key as JWK.
* Add public key to the attacker server.<br>
Attacker Server file:
```javascript
{
  "keys"=[PASTE_COPIED_KEY_HERE]
}
```
### Modifying JWT
* Change the kid of the key to the newly generated kid value which we just pasted on attacker's server.
* Add jku parameter as
```javascript
"jku": "https://example.com/keys"
```
Now Sign the token using the key and change the payload part accordingly.
## 6. kid path traversal (Symmetric algorithm)
* Generate a Symmetric key and change k value as AA==
* Change the kid parameter as below in JWT and sign it.
```javascript
"kid": "../../../../../../dev/null"
```
## 7. Algorithm Confusion
* In case of asymetric algorithm such as RS256, private key is used for signing the token and public used for verification.
* This attack arises in case algorithm is asymmetric such as RSA(RS256). We will modify it to symmetric algorithm and will be using public key for signing and verification purpose.
* Change the payload part and endpoint.
* Change algorithm as:
```javascript
"alg": "HS256"
```
We know that the verification is being done via Public Key in the backend so we will now sign the token using public key. But how do we find the public key? It is meant to be public and sometimes expose via common endpoints such as *jwks.json* in root directory. Just browse it directly from the browser.<br>
Copy
```javascript
{"kty":....}
```
* In JWT Editor Extension > Generate New RSA key.
* Paste the value copied earlier in key area.
* Right click > Copy the Public Key as PEM.
* Encode this in base64 format.
* Copy the encoded value, in JWT Editor Extension Generate a new Symmetric Key > Generate and replace k parameter with our copied value.
* Go back to repeater > Sign the token and send the request.
### 8. JWT authentication bypass via algorithm confusion with no exposed key
We can drive the public key if we have more than one JWT token. (can be of same account) using a tool called rsa_sign2n (https://github.com/silentsignal/rsa_sign2n). Generate two JWT tokens and execute the below command to drive the public key. Always do it in Linux.
 ```
cd rsa_sign2n\standalone
jwt_forgery.py TOKEN1 TOKEN2
 ```
* You might get multiple public keys. Copy the tampered token one by one and see which one is working. Now copy the content of correspodning .pem file(enter at last). Base64 encode the content.
* Generate a symettric key in JWT editor extension and change the value of the k param to the base64 string we generated in previous step.
* Go the the request which contains the normal JWT token. Modify the alg as HS256 from RS256, modify the username in payload, sign the token using the generated symettric key and tries to acess /admin endpoint.
### 9. CVE-2026-23993: Authentication Bypass via unknown algorithm in HarbourJwt
**Ref**: https://pentesterlab.com/blog/cve-2026-23993-harbourjwt-unknown-alg-jwt-bypass<br>
1. Change the alg parameter to any unknown value such as xxxxxxx
2. Change the username in payload part to any user.
3. Remove the signature part from token leaving . at start of signature

