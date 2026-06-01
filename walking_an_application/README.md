# Walking an application

## Reviewing the website content.

When visiting the website always look up for interactive actions: button, inputs, forms.
Check for the page source --> will hide inside some request that user did to the website.

## Developer Toolkit:

Three main tools are: Inspector, Debugger, Network sections.

### Inspector

In the Inspector section you can see html, css, js and even interact with them. This section useful because you can see every elements and see how they work interacting with the website.

### Debugger

For penetration tester the Debugger section is the main section where javascript is deeply analyzed.

Breakpoints - are used to force some js code to stop in the browser.

### Network

Network section is used to track all the external request made to the website.

AJAX - Asynchronous Javascript and xml. ---> allows web pages to communicate with the server in the background.

### Storage

In the Storage there is an information about the user: authentication, user preferences, session cookie.
There are multiple section in the storage: session storage,local storage, cookies, cache storage.

local storage: always stores the data and when the browser is also turned off.
session storage: stores data only for one session and then deletes it. no persistent saving.
cookies: small data sent by the web-app and stored in the browser: used for authentication and session cookie.
cache storage: stores images, scripts, api responses for quick loading. --> this section is used when the website will open again and it will finish uploading quicker.
