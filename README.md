# Harvestly
Welcome to Harvestly! Our mission is to provide a platform for farmers and customers to get together and do business. Harvestly makes it easy for farmers to advertise when, what, and where they're selling, and helps them get together for market events. The markets that the farmers create then get shown to customers that come looking for high-quality produce that you just can't get from a grocery store. Whether you're looking to sell or to buy, let us be the first to welcome you to a thriving community of people looking to share the joy of fresh produce that's made with heart.

## CS 4300-001 Fall 2023 Group 2
### Contributors
* Samuel Adamson (sadamson@uccs.edu)
* Evan Anderson (eander17@uccs.edu)
* Victor Eckert (veckert@uccs.edu)
* Matthew Gibbons (mgibbon2@uccs.edu)
* Jesse Roberts (jroberts@uccs.edu)
* Keegan Shry (kshry@uccs.edu)



## Usage

### Replit
Below is a link to the project.

```
https://replit.com/@sadamsoncpt/CS4300-Fall2023-Group2
```

In replit, run the application by clicking the green `Run` button at the center of the screen. Note that a small `Webview` window will open when the application boots up. __Please do not use the `Webview` window!__ Instead, open the application web link in a web browser:

```
https://cs4300-fall2023-group2.sadamsoncpt.repl.co
```

This link is only live whilst the application is running!

### Local Environment
#### Install Dependencies
Ensure that you are using Python version `>= 3.8`. Before running the application make sure to install all required python packages. It is recommended that you use a _python virtual environment_, although this is  optional.

Create and activate a virtual environment using:
```
python3 -m venv <ENVIRONMENT NAME>
source <PATH TO ENVIRONMENT>/bin/activate
```

Install dependencies using:
```
pip install -r requirements.txt
```

#### Set up SECRET_KEY for Django
Before running the application, ensure that you have configured a `SECRET_KEY` for the project. Start by copying the default environment file (`.env.default`) to a new file named `.env`. Generate a new secret key value and update the `SECRET_KEY` variable in the `.env` file. You can generate a secret key using python with the following python script:

```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Your `.env` file should have the following contents:
```
SECRETY_KEY='<SOME GENERATED KEY>'
```

#### Run Migration (Set up DB)
Once your environment is configured you need to set up your local database. Run the following from the project root directory:

```
python3 manage.py migrate
```

You should see a new database file `db.sqlite3`.


#### Run the App
Now, run the app using:

```
python3 manage.py runserver
```

## Tests
Run tests for this project by executing the command:

```
python manage.py test
```

Tests in each app should be stored in a directory named `tests/`, and each test should follow the naming convention `test_<module_name>.py` (i.e. `Events/tests/test_models.py`). Violating this naming convention may result in the tests not being recognized by Django.

## Test Coverage
Utilize the `coverage` library to evaluate code test coverage. Run the following command:

```
coverage run ./manage.py test && coverage report
```

You can evaluate code coverage for a specific app using the following command:

```
coverage run --source=<APP_NAME> ./manage.py test <APP_NAME> && coverage report
```

To generate a test coverage report as html use the following command:

```
coverage run ./manage.py test && coverage report && coverage html && open htmlcov/index.html
```


## Code Quality
To examine cod quality, utilize the `radon` library (Ensure `radon` is installed, see `requirements.txt`).  
