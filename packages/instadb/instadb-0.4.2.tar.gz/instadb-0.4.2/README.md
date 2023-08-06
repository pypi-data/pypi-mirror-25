# instadb 🔌

A simple and light DB python package

## Features
- query from postgres and reshift
- load data into pandas dataframe
- query from sql or filename
- automatically setup connections from env variables
- automatic query annotation
- connect timeout retry with exponential backoff

### Installation

`pip install instadb`

### Basic Usage

```python
  import instadb
  db = instadb.Connection(url=database_url)
  df = db.dataframe("select * from users limit 10")
```

If you have env variables that match the pattern `<key>_DATABASE_URL` then you can directly do:

```python
  import instadb
  df = instadb.key.dataframe("select * from users limit 10")
```

### Query from file

```python
  df = instadb.key.dataframe(filename='./users.sql')
```

### Query from file with arguments

users.sql
```
select * from users where limit={limit}
```

```python
  df = instadb.key.dataframe(filename='./users.sql', limit=100)
```

## TODO
- [ ] load data to list
- [ ] insert and update queries
- [ ] caching
