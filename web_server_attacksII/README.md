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
