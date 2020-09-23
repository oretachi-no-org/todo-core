# ToDo - Core
Rest APIs for managing to-do lists and tasks including:

1. User account creation and authentication.
    - Note: no verification while creating user accounts.
2. Multiple lists containing tasks.

## Development Setup
Follow this for development setup. Optionally, you can use the included
dev.Dockerfile to create a docker image.

### Manual dev setup:

##### Virtual Environment
```shell script
python3 -m venv venv
source venv/bin/activate
```

##### Dependencies
Install the project dependencies in the virtual environment.
```shell script
pip install -U pip setuptools wheel
pip install -r requirement.txt
pip install ipython
```

##### Django Secret Key
The django secret key has been removed from plain text format.

Use the following command to open an interactive shell with the server.

```shell script
python manage.py shell
```

Inside the ipython shell we will create a django secret key.

```python
from django import utils
print(utils.get_random_secret_key())
```

Now set the output string as an environment variable. You can also set this
variable in ~/.bashrc or ~/.zshrc also.

```shell script
export TODO_CORE_SECRET_KEY='{output of previous step}'
```

##### Make Database Migrations
Make the SQL table structure required by running the following.
```shell script
python manage.py migrate
```

##### Run the Development server
Finally run the server using:
```shell script
python manage.py runserver localhost:8000
```

### Docker Dev setup

---
***WARNING***: DO NOT USE THE DEV DOCKERFILE IN PRODUCTION OR ON A
MACHINE WITH PUBLIC ACCESS. YOUR DATA WILL BE COMPROMISED.
---

If using docker simply run the following command:

```shell script
docker build --tag=todocore:dev -f dev.Dockerfile .
docker run -p 8000:8000/tcp -d todocore:dev
```

### Accessing REST API documentation

After successfully running the server go to 
[localhost:8000/api/swagger](http://0.0.0.0:8000/api/swagger)
for the complete API documentation.

---
BSD - 3 clause License.

