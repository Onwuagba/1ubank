# 1UBank

Question responses can be found in **responses.md**

## Getting started
Clone the repository:

```sh
[] $ git clone https://github.com/Onwuagba/1ubank/
[] $ cd 1ubank
```
Create a virtual environment to install dependencies and activate it:

``` sh
$ python -m venv <name_of_virtual_environment> e.g. 'venv'
$ venv/Scripts/activate
```

Install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
The `(venv)` prefix tells that the virtual environment is active.

Once `pip` has finished installing all dependencies:
```sh
(venv)$ cd 1ubank
(venv)$ python manage.py makemigrations
(venv)$ python manage.py migrate
```

Rename `.env.copy` to `.env` and update with the relevant credentials 
```sh
(venv)$ python manage.py runserver
```

Setup complete. Navigate to `http://127.0.0.1:8000/docs` to see the list of available endpoints.