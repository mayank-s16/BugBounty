# JWT Test Cases
BurpSuite Extension: JWT Editor
## 1. Lack of Signature Verification
## 2. None Algorithm
## 3. Weak Signing Key Bruteforcing (Symmetric)
Works only for symmetric encryptuon algorithm (HS256)
Tool Reference: 
```
python jwt_cracker.py --token TOKEN --wordlist WORDLIST
```
## 4. JWK parameter Injection (Asymmetric)
Application does accept arbitrary injected JWK value and it works for  Asymmetric algorithm e.g. RS256. The JWT would be signed by equilvalent private key of the public key which we embedded in the JWT. Application would verify it from the public key again and provides us the access.
Generate RSA key using JWT Editor Extension and select Attack > Embedded JWK.
## 5. JKU parameter Injection (Asymmetric)
### Setting up Attacker Server
From where the key would be fetched, we can include our own hosted keys.<br>
Generate RSA Key copy public key as JWK.<br>
Add public key to the attacker server.<br>
Attacker Server file:
```
{
  "keys"=[PASTE_COPIED_KEY_HERE]
}
```
### Modifying JWT
Change the kid of the key to the newly generated kid value which we just pasted on attacker's server.<br>
Add jku parameter as
```
"jku": "https://example.com/keys"
```
Now Sign the token using the key and change the payload part accordingly.
## 6. kid path traversal (Symmetric algorithm)
Generate a Symmetric key and change k value as AA==<br>
Change the kid parameter as below in JWT and sign it.
```
"kid": "../../../../../../dev/null"
```
## 7. Algorithm Confusion
Symmetric: One Key is used for signing and verification of token<br>
Asymmetric: Private key is used for signing the token and public used for verification<br>
This attack arises in case algorithm is asymmetric such as RSA(RS256). We will modify it to symmetric algorithm and will be using public key for signing and verification purpose.<br>
Change the payload part and endpoint.
Change algorithm as
```
"alg": "HS256"
```
We know that the verification is being done via Public Key in the backend so we will now sign the token using public key. But how do we find the public key? It is meant to be public and sometimes expose via common endpoints such as jwks.json in root directory. Just browse it directly from the browser.
Copy
```
{"kty":....}
```
In JWT Editor Extension > Generate New RSA key
Paste the value copied earlier in key area.
Right click > Copy the Public Key as PEM.
Encode this in base64 format.
Copy the encoded value, in JWT Editor Extension Generate a new Symmetric Key > Generate and replace k parameter with our copied value.
Go back to repeater > Sign the token and send the request.
