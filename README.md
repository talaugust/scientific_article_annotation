# Science News Annotation

## Purpose
This repo holds to code for running a server that supports annotations on science news articles. The interface is used in the publication:

  Tal August, Lauren Kim, Katharina Reinecke, and Noah Smith ''Writing Strategies for Science Communication: Data and Computational Analysis'', Conference on Empirical Methods in Natural Language Processing (EMNLP) 2020.


## Prerequisites 
This project is built with [Django](https://www.djangoproject.com/) and uses [annotator.js](http://annotatorjs.org/) for annotations. 

You also need a database to connect to. See here for [setting up a database with Django](https://docs.djangoproject.com/en/3.1/ref/databases/).

Note that we used mysql for our database.

Once your dataset is set up, export the connection parameters with (assuming you are doing this on a local environment):

```
export DBNAME=""
export DBHOST="localhost" 
export DBUSER=""
export DBPASS=""
export PROD_KEY=""
export WEBSITE_SITE_NAME="127.0.0.1"
```



## Installation
Begin by creating a new virtual environment and installing required packages 
(here using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))

`conda env create -f environment.yml`

And activate it 

`conda activate sci-comm`


Migrate the django models to the database

`python manage.py migrate`

And run the server

`python manag.py runserver`

You can access the site at http://localhost:8000/home/. Note that we do not provide any articles to populate the database, but you can access the original article urls used in the paper at https://github.com/talaugust/scientific-writing-strategies. 

## Annotation API

To enable annotations, we use [annotator.js](http://annotatorjs.org/) and connect it to the backend with the [Django REST Framework](https://www.django-rest-framework.org/). The file `/annotationAPI/static/annotationAPI/js/annotation.js` sets up the annotator frontend and connects it to the django backend. 
