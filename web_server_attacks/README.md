# Web Server Attacks I

## Introduction

In the penetration testing if you are testing web application high chances to run into the web servers.

### Web servers for linux infrastructure:

1. Nginx
2. Python http server
3. Apache
4. Node.js Express application

Reconaissance and misconfiguration analyzes are good skill to acquire as penetration tester.

## Identifying Web Servers

It is a good practice to always look for application before enumeration phase.
Default configuration of web servers are tend to be verbose.
Most info gives the server header in http response.

`curl -sI http://ip:port`

-s suppresses the progress bar

-I sends a Head request and return only response headers.

output:

Date: Wed, 08 Apr 2026 13:59:00 GMT
Server: Apache/2.4.58 (Ubuntu)
Last-Modified: Fri, 03 Apr 2026 18:12:44 GMT
ETag: "29af-64e9243796aa2"
Accept-Ranges: bytes
Content-Length: 10671
Vary: Accept-Encoding
Content-Type: text/html

The server header gives info about the server and versions. Some of the serves could provide less or no information.
Every server have different default settings. And each other will give you different responses.

Additionally you can user browser tools: network section to see the same header.
Each servers default page will have different looks.

## Python HTTP Server

Python has built-in http server command:

`python3 http-server 8000`

This command will create an http-server in 8000 port.

What is used for:

1. test static websites
2. share files
3. transfer between two machines

The problem is that this server do not have authentication, no access-control, no logging in.

### What it servers

Basically everything that in the working directory can be downloaded.

Other type of servers can be configured that way to disallow access to certain directories but in python http server everything can be accessed.

### Directory Listing

Python automatically generates html page creating every file that it can see.

`curl -s http://ip_address:port/`

### Accessing dotfiles

.env file types are common target because developers are storing credentials for specific configuration in the app.

This filetype usually hidden in directory navigation linux, but python treats all file the same way.

`curl -s http://ip_address:port/.env`

### Downloading and Inspecting Archives

.zip .tar.gz could contain source code, database dumps and configuration files.

`curl -s http://ip_address:port/backup.zip -o backup.zip`
`unzip backup.zip -d backup_contents/`
`cat backup_contents/db_dump.sql`

### Why this matters

The python http server will be triggered without using exploits. The server functionality stays the same as designed.

The problem is using this server in the directory that should not be public.

## Apache2

Apache is very popular open source web-server in web infrastructure. By the default Apache server some settings are enabled which can cause information about server leaked.

_Three most popular settings to get information leaked_

1. directory listing
2. server status module
3. backup files

### Version Disclosure

Knowing the exact version of the web server allows you to find the CVE and what analyze it more deeply.

Command to find the version of Apache:
`curl -SI http:/ip_address:80 | grep -i server`

### Directory Listing

Apache's directory list will give the file name, size and last modified date, so it is easier to analyze.
Developer often leave sensitive data in files, as penetration tester it is important to read every file in the directory.

### The mod_status page

mod_status is a status page, if configured correctly should be accessible only from localhost otherwise it is accessible from any.

This status pages shows all request and what connection does the server have.

### Gobuster tool

Many of website content is hidden. Gobuster tool will help finding them by guessing the path with the wordlist.

`gobuster dir -u http://TARGET_IP -w /usr/share/wordlist/SecList/Discovery/Web-Content/common.txt -x bak,html,txt -t 20`

Always check for bak extension. Could contain config snippets, credentials, copies of source code.

.htpasswd could contain hashed passwords.

### Putting it together

Common pattern of action to analyze the Apache server:

1. Check the version header
2. Browse directories with listing
3. Look for /server-status
4. Use Gobuster to find unlinked files.

## Node.js

Node.js Express is more flexible than python and apache webserver, but that cause more problem.

The biggest problem with this web server is that the specific features may be enabled and attackers that could see the source code and what credentials it is using.

### Framework Fingerprinting

`curl -sI http:TARGET_IP:3000`

output:

root@ip-10-81-64-63:~# curl -sI http://Target_IP:3000
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: application/json; charset=utf-8
Content-Length: 56
ETag: W/"38-K8iCfm09rMr0MV0NsgqdAb94DAk"
Date: Sat, 11 Apr 2026 07:27:28 GMT
Connection: keep-alive
Keep-Alive: timeout=5

Check for X-Powered-By to see what is type of web server the application is using.

### Reading the application version

Mostly node.js express web servers use json for status response.

`curl -s http://TARGET_IP:3000`

output:

{"status":"ok","app":"company-portal","version":"1.2.0"}

### Triggering Verbose Errors.

Node.js have default error handler that do not shows the stack. Often developers use custom made handlers which can cause a stack traces exposed.

command:

`curl -s http://TARGET_IP:3000/api/users | python3 -m json.tool`

output:

`{
"error": "connect ECONNREFUSED 127.0.0.1:5432",
"stack": "Error: connect ECONNREFUSED 127.0.0.1:5432\n at /opt/nodeapp/app.js:16:15\n at Layer.handle [as handle_request] (/opt/nodeapp/node_modules/express/lib/router/layer.js:95:5)\n at next (/opt/nodeapp/node_modules/express/lib/router/route.js:149:13)\n at Route.dispatch (/opt/nodeapp/node_modules/express/lib/router/route.js:119:3)\n at Layer.handle [as handle_request] (/opt/nodeapp/node_modules/express/lib/router/layer.js:95:5)\n at /opt/nodeapp/node_modules/express/lib/router/index.js:284:15\n at Function.process_params (/opt/nodeapp/node_modules/express/lib/router/index.js:346:12)\n at next (/opt/nodeapp/node_modules/express/lib/router/index.js:280:10)\n at expressInit (/opt/nodeapp/node_modules/express/lib/middleware/init.js:40:5)\n at Layer.handle [as handle_request] (/opt/nodeapp/node_modules/express/lib/router/layer.js:95:5)",
"query": "SELECT \* FROM users"
}`

The stack trace is very important here. The attacker could see directories and what files are exist in the application.

### Enumerating Routes via Debug Endpoints

Misconfigured Express application could tell its own routes. This happens because of developers more convenient using listing routes and then they just forget to disable them.

command:

`curl -s http://TARGET_IP:3000/api/routes`

output:
[{"method":"GET","path":"/"},{"method":"GET","path":"/api/users"},{"method":"GET","path":"/api/routes"},{"method":"GET","path":"/api/debug/env"}]

This command will save you time of using gobuster.

!Important note: the response could differ because of different Express versions.

### Exposed Environmental Variables

Always check for environmental files. They contain database credentials, API keys and config flags.

`curl -s http://TARGET_IP:3000/api/debug/env`

output:

`{"NODE_ENV":"development","DB_PASSWORD":"NodeDBPass2024!","PORT":"3000","DB_HOST":"localhost:5432","APP_NAME":"company-portal"}`

Always document the credentials ---> "DB_PASSWORD"

### Static File Serving

express.static() middleware to serve frontend assets within express, if exists serves everything in a directory.

Client-side js often contains api endpoint URL's, internal hostnames, debug flags.

command:

`curl -s http://TARGET_IP/static/config.js`

output:

`// Client-side configuration
const API_BASE = 'http://internal-api.company.local:8080';
const DEBUG = true;
const VERSION = '1.2.0';
// flag: THM{node_debug_exposed}
`

### Putting it all together

Check for errors very cautiously. They hide within themselves important information about web application internals.
