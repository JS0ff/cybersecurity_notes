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
