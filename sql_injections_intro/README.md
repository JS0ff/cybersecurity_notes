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
