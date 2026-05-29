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

## Practicing CSRF vulnerabilities with html forms

In the html_script folder provided two scripts. One is the example of post command that is vulnerable. And the other script is javascript code that will change the address to the attacker@evilmail.thm.

Essentially is needed to change the value of an input value to the chosen mail address.

## Practicing CSRF vulnerabilities with weak tokens

Check for the encoding of the token. Some of them only seems to have good protection, but actually using the basic encoding techniques.

In the weak_token_exploit.html shows the script with event listener set to the onmouseover, that triggers the request to change the role with the using of user session cookie.

## Important Practices

1. Always check for the state-changing requests: password updates, email updates, changing user preferences.
2. Analyze the CSRF tokens. If there is no token or the token is not changing, the application most likely to be vulnerable.
3. Check for HTTP methods. Most of the time important data is uses POST requests. If it uses the GET method it will be easier to exploit, using links or images.
4. Try to use the request outside the application: Use external HTML page to send the same request. If the requests passes the target is likely to be vulnerable
5. Analyze the session cookies. Check if the authentication relies solely on the session-cookie. And if the web-application gets the request without security checking where did the request came from, the attack is possible.
