# CSRF Notes

## What is CSRF

- Cross Site Request Forgery - is an attack of abusing the user session cookie.
- Session-Cookie - is used for application or website to recognise the user activities in the future.

An attacker can exploit the csrf without knowing the login credentials.

## How it works

1. The user logins to the actual website with credentials.
2. Attacker tricks the user to visit malicious webpage with crafted request.
3. Finally the user browser will send a request to the target application, additionally with session-cookie of the user.

Because request have an actual and legit session-cookie the website will pass it as true.
