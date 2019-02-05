Hitlog Reader
=============

When a user visit a page in the website, a record is created in a hitlog file which shows the detail of the visit.
This file is available for Data Team on daily basis.
We want to find out top 3 Telegraph articles which lead users to the registration.

As an example if we have these three different journeys for three different users

user1: article#1 -> article#2 -> article#3 -> registration
user2: article#1 -> registration
user3: article#2 -> article#1 -> registration

article#1 is the most influential article with total number of 3 as it was part of all journeys.


Install
=======

Create and activate your virtual environment either using `conda` or `virtualenv`

Install package and cli tool

```bash
$ python setup.py
```

Use the software
================

To use hitlog, run the following command

```bash
$ hitlog input_file output_file
```

Test
====

To run the unittest please run the following commands.

```bash
$ pip install -r dev-requirements.txt
4 pytest tests/

