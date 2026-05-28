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

## Why this attack is dangerous?

Attacker can easily change and take an action on any possible activities on the application.

- Money transaction
- Account Settings
- Changing the login credentials
- Privacy or security preferences

## Why CSRF attack works?

The attack exploits primarily the trust between the user browser and the application.

Browsers initially were setup to trust for request. The actual problem is when the web application rely too much on this request without checking them.

Session cookie automatically creates every time the user logins. It works like an identity card for the website.

Actual problem is browser automatically send cookies with request to the same domain. it doesn't check if the request came from the legit page or malicious one.

The application needs to check every request where did it triggered from.

### Conditions for the CSRF attacks.

1. The victim should be authenticated on the webpage.
2. The webpage should perform any request that modifies data(state changing action).
3. The application should not perform a scan from where did the request came from.

## Finding the CSRF vulnerabilities

To find the vulnerability it very helpful to ask: "Can this action be triggered without verifying that the actual request came from the user?"

POST and GET requests are both vulnerable to this attack.

These are actions that are most likely to be vulnerable to the CSRF attack:

- Changing the email address
- Updating the login password
- Editing the profile info
- Alter payment info
- Updating the payment credentials
- Submit user preference form
