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
To examine code quality, utilize the `radon` library. You can evaluate the quality of a module using the following commands:

#### Cyclomatic Complexity:
```
radon cc <FILE_NAME | APP_NAME>
```

#### Maintainability:
```
radon mi -i A <FILE_NAME | APP_NAME>
```

#### Halstead Metrics:
```
radon hal <FILE_NAME | APP_NAME>
```

#### Raw - Lines of Code (LOC), Cohesion/Coupling:
```
radon raw <FILE_NAME | APP_NAME>
```

[More Radon Usage](https://radon.readthedocs.io/en/latest/commandline.html)

### Interpret Radon Results

#### Cyclomatic Complexity [More Information](https://radon.readthedocs.io/en/latest/commandline.html#the-cc-command):
Each file is given a grade:
* `A`: Low Complexity (1 - 5)
* `B`: (6 - 10)
* `C`: (11 - 20)
* `D`: (21 - 30)
* `E`: (31 - 40)
* `F`: (41 - 50)
* `G`: High complexity (51+)

Generally, it is best to maintain lower complexity in the interest of readability and maintainability.


#### Maintainability [More Information](https://radon.readthedocs.io/en/latest/commandline.html#the-mi-command):
Once again, each file is given a letter grade:
* `A`: Very High (20 - 100)
* `B`: Medium (10-19)
* `C`: Extremely Low (0 - 9)

For maintainable code, it is best to maintain `A` grades here.

#### Halstead Metrics [More Information](https://en.wikipedia.org/wiki/Halstead_complexity_measures):

The halstead metrics are provided as follows:
* `h1`: Number of distinct operators
* `h2`: Number of distinct operands
* `N1`: Total number of operators
* `N2`: Total number of operands
* `vocabulary`: Result of `h1 + h2`
* `length`: Result of `N1 + N2`
* `calculated_length`: Result of `h1 log(h1) + h2 log(h2)`
* `volume`: Result of `length x log(vocabulary)`
* `difficulty`: Result of `h1/2 + N2/h2`
* `effort`: Result of `difficulty x volume`


#### Raw - Lines of Code (LOC), Cohesion/Coupling [More Information](https://radon.readthedocs.io/en/latest/commandline.html#the-raw-command):

This is an evaluation of number of lines of code and their purpose (i.e. blank, comments, code, etc).

## Code Qualification - PyLint [More Information](https://pylint.pycqa.org/en/latest/index.html)

To evaluate the overall consistency and readability of the code, as well as its adherence to coding best practices, use the `Pylint` library. To evaluate a module use the following command:
```
pylint --generated-members=objects --ignore=migrations < APP_NAME >
```
This will examine the module's code for formatting errors and non-adherence to coding practices, and it will provide a score X/10 based on what it finds. The `--generated-members=objects` qualifier lets PyLint know that the created objects in the test cases are being set dynamically and should be ignored to avoid throwing E1101 (no-member) errors. The `--ignore=migrations` qualifier tells PyLine to ignore the migrations directory when checking the code.


## Code Security - Bandit

To evaluate the presence of security pitfalls in the code, use the `Bandit` library. To evaluate a module use the following command:
```
bandit -r < APP_NAME >
```
This will examine the module for potential security issues and generate a report detailing the number of issues found, the severity of those issues, and the confidence rating of those issues.


## Google Maps API Key Configuration
This app uses the [Google Maps API](https://developers.google.com/maps) to store set location information for events. You must first create a Google Maps API key.


### Generate a Google Maps API Key [More Information](https://developers.google.com/maps/get-started):


#### Set Up Google Cloud Project
Navigate to the Google Cloud Console's [Project Selector](https://console.cloud.google.com/projectselector2/home) page. Select `Create Project` to begin creating a new cloud project. Make sure that [billing](https://console.cloud.google.com/projectselector2/billing) is enabled for your Cloud project. 


#### Enable APIs
Navigate to the [Maps API Library](https://console.cloud.google.com/projectselector2/google/maps-apis/api-list) page. Ensure that `Maps JavaScript API` and `Places API` are enabled.


#### Get API Key
Navigate to the Google Cloud Console's [Credentials](https://console.cloud.google.com/projectselector2/google/maps-apis/credentials) page. Select `Create credentials` and then select `API key`. The API key created dialog displays the newly created API key.


#### Insert API Key Into .env
After acquiring an API key, set the API key in the `.env` file:
```
GOOGLE_MAPS_API_KEY='<YOUR API KEY>'
```


### Restrict your Google Maps API [More Information](https://developers.google.com/maps/api-security-best-practices#restricting-api-keys):

You need to restrict your Google Maps API key so that it is limited to use on certain websites or certain IP addresses.

To achieve this, navigate to the Google Cloud Console's [Google Maps Platform Credentials](https://console.cloud.google.com/projectselector2/google/maps-apis) page. Select the Google Cloud project for which you created to generate your API key. Select the API key that you want to restrict. On the Edit API key page, under Key restrictions, select `Set an application restriction`. Here, you can select the type of application restriction that you wish to add to your api key. The restriction types are as follows:
* `Websites`: Specify one or more referrer websites. Always provide the full referrer URI, including the protocol scheme, hostname and optional port (e.g., https://google.com)
* `IP addresses`: Specify one or more IPv4 or IPv6 addresses, or subnets using CIDR notation.


