Paste
=====

Opensiurce paste service

* __Author__: Ondrej Sika, <http://ondrejsika.com>, <ondrej@ondrejsika.com>
* __GitHub__: <https://github.com/ondrejsika/paste>


Documentation
-------------

### Installation

```
git clone https://github.com/ondrejsika/paste.git
cd paste
virtualenv env
./env/bin/pip install -r requirements
./manage.py syncdb
./manage.py migrate
```

### Run

```
./manage.py runserver
```
