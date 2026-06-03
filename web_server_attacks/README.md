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
