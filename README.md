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

[![Run collection in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/7261954-cbee5ee6-6201-4ca5-a8c6-316b94bab831?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D7261954-cbee5ee6-6201-4ca5-a8c6-316b94bab831%26entityType%3Dcollection%26workspaceId%3D21eb856b-3287-46ec-951c-824c21f61034)