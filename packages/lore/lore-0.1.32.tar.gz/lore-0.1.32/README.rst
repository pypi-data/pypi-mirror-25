======
 Lore
======

Lore is a python data science framework to design, fit, and exploit data science
models from development to production. It codifies best practices to
simplify collaborating and deploying models developed on a laptop with jupyter
notebook, into high availability distributed production data centers.


Example
=======

::

$ pip install lore

$ lore new my_project  #  create file structure & virtualenv
$ lore workon my_project  #  change working directory & virtualenv
$ lore install my_project  #  get dependencies (including raw data snapshots)

$ lore generate my_model  #  create a model

$ lore task fit my_model  #  train the model

$ lore serve all &  # start a default api process

$ curl -X POST -d '{"feature_1": "true"}' http://0.0.0.0:3000/my_model
  {class: "positive"}


Features
========

* **Repeatable:** Lore allows developers to work on multiple projects with
  different versions of dependencies without conflict, while preserving
  similarity with production. It removes manual handling of anaconda, brew,
  apt-get, pyenv, virtualenv, docker et al.

* **Sharp::** Lore is as simple as you want it to be. Getting started takes a
  handful of commands, but you've just unlocked the full depth of cutting edge
  machine learning.

* **Scalable:** Lore projects are horizontally scalable, but start with
  vertical scalability in a single thread to ease into the learning curve.

* **Transparent:** Lore doesn't wrap or hide or abstract the libraries you've
  already learned how to use. It's goal is to remove boiler plate and
  inconsistency from a typical workflow, without reinventing the wheel.

* **Efficient:** Lore adds minimal overhead while gluing all of the underlying
  libraries together. We test for <1% performance impact during critical phases,
  such as fitting models on production size datasets.

* **Mature:** Lore has all the bells and whistles you expect to work out of
  the box in every environment. IO (csv, sql, pickle...), logging, tracking,
  reporting, timing, testing, deploying are all available safe and secure w/
  minimal configuration.


Lore stands on the shoulders giants
===================================

Lore is designed to be as fast and powerful as the underlying libraries.
It seamlessly supports workflows that utilize:

* airflow
* tensorflow
* keras
* scikit-learn
* pandas
* numpy
* sqlalchemy
* psychopg
* protobuf
* gunicorn
* hub
* mani
* virtualenv, pyenv, python (2.7, 3.3+)


Commands
========

$ lore new
$ lore install
$ lore update
$ lore workon
$ lore generate [**all**, api, model, notebook, task] NAME
$ lore task
$ lore console
$ lore serve
$ lore start
$ lore stop


Project Structure
=================

::

├── .env.template            <- Template for environment variables for developers (mirrors production)
├── .python-version          <- keeps dev and production in sync (pyenv)
├── README.md                <- The top-level README for developers using this project.
├── requirements.txt         <- keeps dev and production in sync (pip)
│
├── docs/                    <- generated from src
│
├── notebooks/               <- explorations of data and models
│       └── my_exploration/
│            └── exploration_1.ipynb
│
├── src/
│   ├── __init__.py          <- loads the various components (makes this a module)
│   │
│   ├── api/                 <- external entry points to runtime models
│   │   └── __init__.py      <- loads the various components (makes this a module)
│   │
│   ├── config/              <- environment, logging, exceptions, metrics initializers
│   │   └── __init__.py      <- loads the various components (makes this a module)
│   │
│   ├── tasks/               <- run manually, cron or aiflow
│   │   ├── __init__.py      <- loads the various components (makes this a module)
│   │   └── my_model/
│   │       ├── etl.py
│   │       └── train.py
│   │
│   ├── data/                <- Scripts to move data between sources
│   │   ├── __init__.py      <- loads the various components (makes this a module)
│   │   └── etl/             <- etl sql between DBs (local/production too)
│   │       └── table_name.sql
│   │
│   ├── features/            <- abstractions for dealing with processed data
│   │   ├── __init__.py      <- loads the various components (makes this a module)
│   │   └── my_features.py
│   │
│   └── models/              <- Code that make predictions
│       ├── __init__.py      <- loads the various components (makes this a module)
│       └── my_objective/
│           ├── deep_model.py
│           └── linear_model.py
│
└── tests/
    ├── api/
    ├── tasks/
    └── models/



Design Philosophies & Inspiration
=================================

* Personal Pain
* Minimal Abstraction
* No code is better than no code (https://blog.codinghorror.com/the-best-code-is-no-code-at-all/)
* Convention over configuration (https://xkcd.com/927/)
* Sharp Tools (https://www.schneems.com/2016/08/16/sharp-tools.html)
* Rails (https://en.wikipedia.org/wiki/Ruby_on_Rails)
* Cookie Cutter Data Science (https://drivendata.github.io/cookiecutter-data-science/)
* Gene Roddenberry (https://www.youtube.com/watch?v=0JLgywxeaLM)
