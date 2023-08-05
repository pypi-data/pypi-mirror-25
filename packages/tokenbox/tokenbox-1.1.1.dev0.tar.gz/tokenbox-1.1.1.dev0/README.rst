
# tokenbox
RESTful API token management utility 

### Description
RESTful APIs require you to manage and refresh authorization tokens. When starting out with a new API, you don't really want to mess with that stuff; you just want the tokens to go somewhere you can get them whenever you need them and ignore them the rest of the time. `tokenbox` is designed to facilitate putting them somewhere, like a nice neat little box in the corner.

Tokenbox will ensure that there is only 1 row in any database that it manages, so you don't need to worry about databases taking up unnecessary disk space.

With no configuration, `tokenbox` is capable of generating SQLite databases. Here is a description the arguments that an instance of TokenBox expects from `tokenbox.py`

* `db_user (string)`: user of db login role (must be capable of creating a PG database)
* `db_password (string)`: password of db login role
* `db_name (string)`: name of database to be created/managed
* `use_sqlite (bool)`: whether or not to use sqlite
* `metadata (sqlalchemy.MetaData)`: metadata used in table definitions 
* `kwargs (sqlalchemy.Table)`: names of Tables and corresponding definitions 

Below is an example of creating an SQLite database for multiple tokens. These tables were designed for use with the Bullhorn api.


```python
from sqlalchemy import Table, MetaData, Column, Integer, String
from tokenbox import TokenBox

metadata = MetaData()

table_definitions = {
    "login_token": Table("login_token", metadata,
        # primary key must be in the format '{table_name}_pk`
        Column("login_token_pk", Integer, primary_key=True),
        Column('access_token', String(45), nullable=False),
        Column('expires_in', Integer, nullable=False),
        Column('refresh_token', String(45), nullable=False),
        Column('token_type', String(45), nullable=False),
        Column('expiry', Integer, nullable=False),
    ),
    "access_token": Table("access_token", metadata,
        # primary key must be in the format '{table_name}_pk`                      
        Column("access_token_pk", Integer, primary_key=True),
        Column('rest_token', String(45), nullable=False),
        Column('rest_url', String(60), nullable=False)
    )
}

use_sqlite = True

tokenbox = TokenBox('db_user', 'db_pass', 'tokenbox_test', use_sqlite, metadata, **table_definitions)
# Creates a database corresponding to the arguments passed during TokenBox initialization
tokenbox.create_database()
# Updates (or inserts) the row into the 'login_token' table (there can only be one row!)
tokenbox.update_token('login_token', access_token="12341234123asdfasdf4", expires_in=300,
                      refresh_token="asdfkk23784987123khjga", token_type="login", expiry=12312312)
# Updates (or inserts) the row into the 'access_token' table (there can only be one row!)
tokenbox.update_token('access_token', rest_token="12341234123asdfasdf4", rest_url="asdfkk23784987123khjga")
# Gets the row from the 'login_token' table (there's only one row in storage!)
login_token = tokenbox.get_token('login_token')
print(login_token.items())
# Gets the row from the 'access_token' table (there's only one row in storage!)
access_token = tokenbox.get_token('access_token')
print(access_token.items())

tokenbox.destroy_database()
```

    [('login_token_pk', 1), ('access_token', '12341234123asdfasdf4'), ('expires_in', 300), ('refresh_token', 'asdfkk23784987123khjga'), ('token_type', 'login'), ('expiry', 12312312)]
    [('access_token_pk', 1), ('rest_token', '12341234123asdfasdf4'), ('rest_url', 'asdfkk23784987123khjga')]
    This will destroy the database named tokenbox_test. Perform Keyboard Interrupt to abort.
    tokenbox_test dropped successfully.


Hope this does you some good!
