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
