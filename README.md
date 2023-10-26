# Harvestly
__An Online Farmers Market__

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

__Note__ that this link is __not__ a private access link. If you do not currently have permission to access, please request access from one of the contributors above.

```
TODO
```

In replit, run the application by clicking the green `Run` button at the center of the screen. Note that a small `Webview` window will open when the application boots up. __Please do not use the `Webview` window!__ Instead, open the application web link in a web browser:

```
TODO
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

