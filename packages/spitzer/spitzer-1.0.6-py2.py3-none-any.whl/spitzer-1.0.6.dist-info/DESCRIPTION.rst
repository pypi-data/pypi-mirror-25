# Spitzer

Django-based multi-target migration tool

# Install requires
- Python 3.4+
- Django
- PyYAML
- terminaltables
- cymysql
- django-cymysq

```PHP
pip install rinzler
```

# Config

Place a copy of the sample [spitzer.yaml](https://github.com/feliphebueno/Spitzer/wiki/spitzer.yaml) at 
your app's root directory.

# Usage
```PHP
//Configure e install Spitzer
$ python -m spitzer install

//Create and register a new blank migration file
$ python -m spitzer create

//Register your self-created migration file
$ python -m spitzer make_migrations

//Execute migrations on the configured target
$ python -m spitzer migrate

//List your migrations
$ python -m spitzer show_migrations

//You will see something like this:
```
<img width="847" alt="captura de tela 2017-09-06 as 10 19 50" src="https://user-images.githubusercontent.com/6662338/30114124-41cbd75c-92ed-11e7-82ef-c05632c8e25a.png">


