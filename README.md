# Django Project Setup

http://drksephy.github.io/2015/07/16/django/


## Initial installations

Here working with *python 2.7*
```
python get-pip.py
[sudo] pip install Django
[sudo] pip install virtualenv
[sudo] pip install pip-save (saves dependencies in requirements.txt, like npm install --save)
```

### Start new  project
```
django-admin startproject myproject
cd myproject
```

### Activate virtual environment

Use *virtualenv* to create an environment that has its own installation directories, that doesn’t share libraries with other virtual environments (and optionally doesn’t access the globally installed libraries either).

```
virtualenv ENV
source ENV/bin/activate`
```

### Create applications within projects

`python manage.py startapp myapp`

In settings.py, add myapp to installed apps
```
INSTALLED_APPS = [ …
    myapp,
]
```

## Install npm
In Mac OS X 
Install NVM follow these instructions
[https://gist.github.com/nijicha/e5615548181676873118df79953cb709](https://gist.github.com/nijicha/e5615548181676873118df79953cb709)

Install version 4.2.0
`nvm install 4.2.0`


## Setup Database (MySQL)

Requires MySQL-python and mysqlclient (already in requirement.txt)

If using XAMPP , add xampp’s mysql to path
`export PATH=${PATH}:/Applications/XAMPP/xamppfiles/bin`

### Import database (empty DB should exist)
`mysql -u root -p colloquia < /Users/cdisciascio/Data/colloquia.sql`

Config in *[myproject]/settings.py*
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'colloquia', #or colloquia-dev
        'USER': cecidisi,
        'PASSWORD': 'asdf',
        'HOST':  'localhost',
        'PORT': '3306'
    }
}
```

###Legacy DB: Auto-generate the models
[https://docs.djangoproject.com/en/dev/howto/legacy-databases/](https://docs.djangoproject.com/en/dev/howto/legacy-databases/)

Django comes with a utility called inspectdb that can create models by introspecting an existing database. You can view the output by running this command:
python manage.py inspectdb

Save this as a file by using standard Unix output redirection (models.py must be inside an app, not in project root):
`python manage.py inspectdb > myapp/models.py`

Save this as a file 
`python manage.py check`


Always add these lines after overwriting models.py with inspectdb
```
fusertag_id1 = models.ForeignKey(Usertag, models.DO_NOTHING, db_column='fusertag_id1', blank=True, null=True, related_name = 'usertag1')
fusertag_id2 = models.ForeignKey(Usertag, models.DO_NOTHING, db_column='fusertag_id2', blank=True, null=True, related_name = 'usertag2')
```


###Migrating models to DB
When working with django models instead of a legacy DB.

####Generate migrations
./manage.py makemigrations [app_name]

####Apply changes go DB
./manage.py migrate [--database db_name] [app_name]

db_name = as appears in settings.py

####Troubleshooting:
If migrate fails add flag `--fake`

###Adding JSON fields to MySQL with Django:

https://stackoverflow.com/questions/37007109/django-1-9-jsonfield-in-models -> check answer by aboutaron user (Important: Django 1.9+ and MySQL 5.7+)

More information on: https://django-mysql.readthedocs.io/en/latest/model_fields/json_field.html#jsonfield


##Task automation
Using webpack and django-webpack-loader. 
Followed this tutorial to setup →  http://owaislone.org/blog/webpack-plus-reactjs-and-django/

###Generate bundles
npm run webpack --config webpack.config.js

###Update static folder
./manage.py collectstatic -c --noinput



###Troubleshooting

```
pip install - locale.Error: unsupported locale setting
export LC_ALL=C
source .bashrc
```

MySQL on OSX: Library not loaded: *libmysqlclient.18.dylib*

`sudo ln -s /Applications/XAMPP/xamppfiles/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.18.dylib`

comet_urank.LocationCopy.location: (mysql.E001) MySQL does not allow unique CharFields to have a max_length > 255.

`LocationCopy.location → max_length = 300  250`

Check if debug is set to True (only for development)
```
./manage.py shell 
>>> from django.conf import settings
>>> settings.DEBUG
```

##Setup Apache WSGI (in production)
Followed this post to configure in pawscomp2.sis.pitt.edu (/etc/httpd/conf.d/000-conf-navigator.conf.save)
https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7
```
Alias /urank_static /home/cecidisi/comet_urank_project/static

<Directory /home/cecidisi/comet_urank_project/static>
    #Order deny,allow
    #Allow from all
    Require all granted
</Directory>

WSGIDaemonProcess comet_urank_project  python-home=/home/cecidisi/comet_urank_project/ENV python-path=/home/cecidisi/comet_urank_project
WSGIProcessGroup comet_urank_project
WSGIApplicationGroup %{GLOBAL}

WSGIScriptAlias /urank /home/cecidisi/comet_urank_project/comet_urank_project/wsgi.py

<Directory /home/cecidisi/comet_urank_project/comet_urank_project>
    <Files wsgi.py>
        Options All
        AllowOverride All
        Require all granted
        #Order deny,allow
        #Allow from all
    </Files>
</Directory>
```

To run 2 or more projects simultaneously on apache read here (/etc/httpd/conf.d/000-django-projects.conf)
https://stackoverflow.com/questions/9581197/two-django-projects-running-simultaneously-and-mod-wsgi-acting-werid


## ElasticSearch
In local machine (Mac OSX)

Install
```
brew update
brew install elasticsearch
```
Run
`elasticsearch`
In server (Centos)
See here → https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-centos-7

```
mkdir elasticsearch
cd elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.1.rpm
sudo rpm -ivh elasticsearch-5.1.1.rpm
```
### Troubleshooting

#### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
```
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
```

#### You can start elasticsearch service by executing
`sudo systemctl start elasticsearch.service`

## UPMC Preparation (to run locally)

####Update project from git (and submodule urank_ui)
```
git pull
if above fails git reset --hard and pull again
git submodule update --init --recursive
```

####Activate virtual environment
`source ENV/bin/activate`

####Migrations to DB
```
./manage.py makemigrations upmc
./manage.py migrate --database upmcdb upmc
```
NOTE: If the last one fails run as `./manage.py migrate --database upmcdb upmc --fake and repeat without --fake flag`

####Download nltk data
```
./manage.py shell
>> import nltk()
>> nltk.download()
```
In the UI set Download Directory (wherever, can be outside of project folder), then select: 
(Corpora) brown, words, stopwords
(Models) averaged_perceptron_tagger, maxent_ne_chunker, maxent_treebbank_pos_tagger, punkt 

Fetch data from pubmed, extract keywords and create ElasticSearch index
```
./manage.py runscript --traceback upmc-entrez
./manage.py runscript --traceback kwext
./manage.py runscript --traceback create-year-facets
./manage.py runscript --traceback upmc-bulk-indexing
```

###Run (one terminal window each)
`elasticsearch`
`npm run watch (cd to comet_urank_project first)`
	If fails, make sure you have installed webpack globally: `npm i -g webpack`
`./manage.py runserver` (with virtual env activated, i.e. source ENV/bin/activate)

###Open in browser http://localhost:8000/urank/upmc
