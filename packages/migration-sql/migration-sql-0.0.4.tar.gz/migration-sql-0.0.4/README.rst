## Installation

To install this library, please put `git+ssh://git@bitbucket.org/work-well/migration-sql.git` into the requirements file or use this command:

> pip install git+ssh://git@bitbucket.org/work-well/migration-sql.git

In the future the lib can be made available on PyPi and it can be installed directly via `pip install migration-sql`


## Library structure

The library is composed mainly of 2 classes `DB`, `Version` and method `migrate()`:

- `DB`: represents a database connection. To create this object, you need to provide the database host, port, username, password and database name

- `Version`: represents a migration version that will be recorded in the database when the migration is applied successfully. It has the unique `version_code`, a `comment` that is usually migration purpose and `sql_text` which is the SQL query that will be applied to the database

- `migrate(versions, dbs)`: this main method will apply necessary version on all databases listed in `dbs`. To avoid discrepancies between the database, if the migration fails on any of the database the whole migration process will be aborted and the database will stay intact.  

## How to use

Here is a code snippet on how to apply migrations on a database

```python
from migration_sql import DB, Version, migrate

all_versions = [
    Version("v0", "just to init", "select 1"),
    Version("v1", "just for testing", "select 2"),
    Version("v2", "create a table", """
CREATE TABLE `my_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `json_column` json DEFAULT NULL,
  `string_column` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
"""),
]

dbs = [
    DB("127.0.0.1", 3306, "root", "root", "master")    
]

migrate(all_versions, dbs)


```
