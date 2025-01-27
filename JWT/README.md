## JWT Test Cases
BurpSuite Extension: JWT Editor
### (i). Lack of Signature Verification
### (ii). None Algorithm
### (iii). Weak Signing Key Bruteforcing
Works only for symmetric encryptuon algorithm (HS256)
Tool Reference: 
```bash
python jwt-cracker.py --token TOKEN --wordlist WORDLIST
```
### (iv). JWK parameter Injection (Asymetric)
Application does accept arbitrary injected JWK value and it works for  Asymmetric algorithm e.g. RS256. The JWT would be signed by equilvalent private key of the public key which we embedded in the JWT. Application would verify it from the public key again and provides us the access.
Generate RSA key using JWT Editor Extension and select Attack > Embedded JWK.
### (v). JKU parameter Injection (Asymetric)
From where the key would be fetched, we can include our own hosted keys,
Generate RSA Key and add public key to the attacker server and copy public key as JWK.
Inject JKU parameter in the JWT and change the payload accordingly, sign it using private key corresponding to the public key we added on attacker's server.
Attacker Server file:
```json
{
  "keys"=[PASTE_COPIED_KEY_HERE]
}
```
Modifying JWT
Change the kid of the key to the newly generated kid value which we just pasted on attacker's server.
Add jku prameter as
```
"jku": "https://example.com/keys"
```
Now Sign the token using the key and change the payload part accordingly.
### (vi). kid path traversal (Symetric algorithm)
Generate a Symettric key and change k value as AA==
Change the kid parameter as below in JWT and sign it.
```bash
"kid": "../../../../../../dev/null"
```
