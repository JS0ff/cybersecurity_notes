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
