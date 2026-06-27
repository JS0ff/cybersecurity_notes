# XSS INTRODUCTION

XSS (Cross-site scripting)

being used to steal sessions, deliver malware and escalate attacks withing the network.

## Important Terminalogies

Document Object Model (DOM) - browser's representation of the webpage, can be read and changed with JavaScript

URL Parameters - bits after `?` characters in a URL address that pass data to the site

JavaScript - is primary language in browser, xss payloads often are small JS code

Cookies - are used for storing data in the browser. `HttpOnly` flag is used to disallow js from reading cookies.

Escaping - transforming user input to the plain text. Used for bypassing input validation.

## XSS Payloads

XSS Payload is a JavaScript code that attacker injects to the web application that runs in other user's browser.

The browser may interpret the injection as the part of the website and run it without filtering.
