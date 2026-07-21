# Session Management

## Introduction

After begin logged in user provided with a session. Session is tracking your actions and checking if the action the user is trying to do is
allowed.

## What is Session Management?

Session management is the process of managing and ensuring the security of the sessions.

Because http protocol is stateless, session is used to track the user action throughout their use of web application.

### Session Management Lifecycle

There is 4 stages in the secure session management lifecycle.

Session Creation -> Session Tracking -> Session Expiry -> Session Termination

#### 1. Session Creation

This stage is tracking your authentification actions. With the finishing your logging in, you will receive sepcial session value.

How the session value is generated, used and stored is significant part of this stage.

#### 2. Session Tracking

With each new request after logging in, the user's session value is also send with the request. Because the HTTP protocol is stateless, this process is allowing the web application to track actions.

With each request made the web application can understand who the session belongs to and what permissions they have.

Attacks made for stealing or impersinating the session value is made because of problems in this stage.

#### 3. Session Expiry

When the user stops using the web application, the http protocol is stateless, so there is no way to know that the user is not using the application.

Session Value have it's own lifetime. Often time you can see it as a redirection to the login menu.

#### 4. Session Termination

When the user forces the logout process it should terminate the session automatically, even the session expiry shouldn't interupt the process. Otherwise the persistent control over the account is can be used.

## Authentication vs Authorisation

IAAA Model:

### IDENTIFICATION:

Who is the user? Web apps know who the person is by email or specific username.

### Authentication

Proof of the user, they say who they are. Password or sended message with key.

### Authorisation

Ensuring the user is using only the provided privilages. Session Traficking is crucial in this stage.

### Accountability

Process of creating list or record with all user actions. Should log all performed actions using specific session. Plays crucial role in incident response, to find the cause of the problem.

## Cookies vs Tokens

Cookies and Tokens are type of session being used. Each of them have their benefits and weaknesses.

### Cookie based session management

When web app wants to start tracking in creates Set-Cookie Header in cookie based session.

Additional categories can be created in this header: Secure, HTTPOnly, Expire, SameSite.

No additional js code needed from client side, the broswer will decide automatically when to send cookie with a request.

### Token based session management

Relies more on client side code. Stored in browser LocalStorage.

new request is made => javascript code loading token from storage => attaching it's as a header.

JWT tokent = JSON WEB TOKENS, passed through Authorization: Bearer header.

There are standards for using this management system but nothing is stoping for not using them.

### Benefits and drawbacks of each method

Cookie Based Session Management: each request automatically sends cookies without human interaction, Cookies attributes enhances the protection of themselves by browser.

Cookie session mangement are more vulnerable to the client side attacks, tricking the browser to sent requests on behalf of the user. And they are locked only in one domain, which makes them difficult to use in decentralized web apps.

Token Based Session Management: request from the client side js. Addionally tokent don't have auto security attributes, so they need to keep safe from information leakage.

Auto security attributes have positive side as it blocks in a core level CSRF attacks. Furthermore they often used in decentralized web apps because javascript have all information withing itself even for verification.

## Security the Session Lifecycle

Analyzing of the problems in each step or phase.

### Session Creation

This is the stage of the most of vulnerabilites for the whole lifecycle.

Couple of Session Creation Vulnerabilities.

#### WEAK Session Values

- weak session value - easy predictable token used by web server.

More and more the vulnerabilites are from weak session value, this is one is easy to detect but with the rise of popularity of an AI this vulnerabilies are becoming more common.

It is important to not use the easy or custom session creation encodings, because in the end the tokens could become guessable and predictable. For example using the **base64** encoding for session creation is a bad example. It can be reverse engineered with no flaws.

The cause of this vulnerability happening is taking over accounts of real users.
