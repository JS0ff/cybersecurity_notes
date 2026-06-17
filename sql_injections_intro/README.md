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
