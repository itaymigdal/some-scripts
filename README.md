# intro
This repo contains some Cyber Security related scripts i have written over time (since i was a nooby to present) 


### ARP_Network_Scanner.py

Scan local network for live hosts by ARP Requests (uses Scapy package).


### ARP_Spoof.py

Spoof victim's ARP cache by fake ARP responses (uses Scapy package).  
Supply target to spoof (by IP or MAC), and Spoofed IP to use.  
The Crafted Packet will bind the Spoofed IP with your real MAC address.


### Base64.ps1

Base64 strings encoder and decoder.  
Can iterate (e.g. encode "some string" 4 iterations).


### Byte_Decoder_Bruter.py

Single-Byte decoder / brute-forcer.  
Supports 4 inputs: string, file, hex string, file contains hex string.
Supports XOR and ADD operations.  
Use case example:  
you have some XORed data and don't know the key?  
This script wil Brute-Force it for you and HexDump all results (Don't forget to output into file, so you could search strings easily).  
if you want to decode - use Byte_Encoder.py.  

 
### Byte_Encoder.py

Hex key Encoder.  
Supply input, operation and key.  
Supports 4 inputs: string, file, hex string, file contains hex string.  
Supports XOR and ADD operations.


### CobaltStrike_Server_Auditor.py

Audit Cobalt Strike teamserver and listeners for default settings.


### DNS_Enum.py

DNS Zone Transfer audit and Subdomain Enumaration.  
Supply domain and subdomains wordlist file.


### Entropy_Calculator

Calculate shannon entropy for a given file.
for PE files calculates for each section.


### Find-String.ps1

Find specific string in files.  
Supply string to search and base path, the script will search string occurances recursively in all files, and will print where it was found.  
Usage example:  
.\Find-String.ps1 -string password -path C:\Users\Owner\Desktop


### FTP_Bruter.py

Brute-Force FTP login.  
Supply Target, user to brute-force and passwords wordlist.  


### FTP_Discover.py

Discover open FTP servers with Anonymous login (uses Scapy package).  
This script will generate 50 threads by default, each of them will:  
	+ generate random public IP address	  
	+ probe port 21 using single SYN packet  
	+ if port is open - try to connect to FTP server  
	+ if connected successfuly - try to login with anonymous user  
	+ if login successfuly - try to list files in current directory (to avoid FP's)  
	+ if found - Print server :)
	

### Get-ExecutedProgramsFromRegistry.ps1

List Executed programs on a windows machine from known registry paths.


### GDE.pyw (Google Dorks Explorer)

GUI Program for google dorking without open the browser :)  
Uses the great python package googlesearch.


### HTTP_Enum.py

Enumarate HTTP files and directories (Forced-browse).  
Supply base URL and wordlist.


### HTTP_Extract_HTML_Comments.py

Extract HTML comments from web page.  
Supply URL.


### HTTP_PUT_Discover.py

Discover HTTP servers with PUT method enabled (uses Scapy package).  
This script will generate 50 threads by default, each of them will:  
	+ generate random public IP address  	
	+ probe port 80 using single SYN packet  
	+ if port is open - send HTTP OPTIONS request to see available methods  
	+ if PUT method in response - try to put /index.txt (empty file)  
	+ if PUTed successfuly - print server :)
	

### Inject_DLL.py

Inject DLL to a target process. 
Supply DLL path and target PID.
make sure the python process, the dll, and the target process are in same architecture (32/64).


### IOC_Parser.py

Parse network IOC's from a text file (like dumped strings from ProcessHacker).  
Search for IPV4's, domains, URL's, emails.


### NimWrap.py

Wrap a windows shell command with compiled binary using nim.
Nim + Winim package should be installed. 
to encrypt shell command (-e option) nim-strenc should be installed as well.


### Out-MiniDump.ps1

MiniDump any process (by PID or by name) using comsvcs.dll.
Default is Lsass.exe.


### PassAmplifyer.py

Create passwords wordlist for a user.  
Supply small wordlist file of possible strings (like name, hobby, or favourite pet), and define which functions to use in order to amplify wordlist.


### Persist-SilentProcessExit.ps1

Persist Thru registry using this awsome technique: https://oddvar.moe/2018/04/10/persistence-using-globalflags-in-image-file-execution-options-hidden-from-autoruns-exe/


### Powershell_Obfuscator.py

Obfuscator for powershell scripts.
Can remove comments, add garbage comments, rename function names and variables, output CMD oneliner for executing encoded powershell scriptblock, and more.


### Privesc_Unquoted_Service.py

Checks for Unquoted service vulnerability on windows os.


### Remcos_Config_Decrypter.py

Decrypt Remcos RAT config.  
make sure you are looking at the unpacked binary which has "SETTINGS" resource (RC4 encrypted).  
Extract this resource (with Pestudio \ Resource hacker \ any other tool) and supply it as an argument to this script which will decrypt it for you :)


### RTLO-File.ps1

Right To Left Override social engineering attack. make evil files look innocent.


### Shodanski.py

Simple script to interact with Shodan API (uses the official Shodan package for python).  
Edit the script to add your Shodan API key.


### Sniffer.py

Simple sniffer (uses Scapy package).  
Prints transportation protocol, source IP, destination IP, and finally print statistics when interrupted.  


### Speak.ps1
 
Simple script to speak using the SpVoice interface.  
Great for Post-Exploitation :)


### TCP_Connect_Scanner.py

Smart TCP Port scanner & Banner grabber.


### TCP_Listener.py

Simple TCP listener, logs connections and data sent to it.


### TCP_Random_Server.py

Discover TCP servers (uses Scapy package).  
This script will generate 50 threads by default, each of them will:  
	+ generate random public IP address  	
	+ probe one of the TCP ports supplied using single SYN packet  
	+ if port is open - print the server :)  
	+ optional: print geolocation for each of them  
 

### TCP_SYN_Scanner.py
 
Simple TCP SYN scanner (uses Scapy package).  


### UDP_Scanner.py

Simple UDP Scanner (uses Scapy package).


### VT_Checker.py

Check file against VirusTotal database (using its sha256 hash), and print results (uses vt official python package).  
Edit the script to add your VT API key.
 
 
### Xor-File.ps1

Simple XORing of files.
 

