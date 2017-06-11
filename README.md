[![Build Status](https://travis-ci.org/richin13/expert-tourist.svg?branch=dev)](https://travis-ci.org/richin13/expert-tourist) [![codecov](https://codecov.io/gh/richin13/expert-tourist/branch/dev/graph/badge.svg)](https://codecov.io/gh/richin13/expert-tourist) [![Code Climate](https://codeclimate.com/github/richin13/expert-tourist/badges/gpa.svg)](https://codeclimate.com/github/richin13/expert-tourist) [![Requirements Status](https://requires.io/github/richin13/expert-tourist/requirements.svg?branch=master)](https://requires.io/github/richin13/expert-tourist/requirements/?branch=master) [![license](https://img.shields.io/github/license/richin13/expert-tourist.svg)](https://opensource.org/licenses/MIT)

# Expert Tourist

Expert tourist is a RESTful API to compute and recommend touristic routes based on user-defined preferences using the Bayes theorem.
For the front-end pair application see [richin13/expert-tourist-react](https://github.com/richin13/expert-tourist-react)

## Our stack

We use the power of Python combined with the flexibility of MongoDB. Some of the open source libraries used for this
project are:

 - [Flask](http://flask.pocoo.org/) (0.12)
 - [MongoDB](https://www.mongodb.com/)
 - [MongoEngine](http://mongoengine.org/)
 - [Google Maps Services](https://github.com/googlemaps/google-maps-services-python)
 - [Flask-Restful](http://flask-restful.readthedocs.io/en/0.3.5/) (0.3.5)
 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
 - [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/index.html)
 - [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
 - And a looong [etc](https://github.com/richin13/expert-tourist/blob/dev/requirements.txt).

## Setting up a development environment

This instructions can also be found on the [repo](https://github.com/richin13/expert-tourist)

### Installation

```bash
git clone git@github.com:richin13/expert-tourist.git  # Cloning the repo
cd expert-tourist  # CD'ing into the cloned repo
virtualenv venv  # Creating a Virtual Environment.
# Creating nice shorcuts
echo 'export SECRET_KEY="<secure-value-here>"' >> venv/bin/activate
echo 'export PYTHONPATH="./"' >> venv/bin/activate
echo 'alias flask="python manage.py"' >> venv/bin/activate
echo 'alias tests="py.test --cov=./ --disable-pytest-warnings"' >> venv/bin/activate
source venv/bin/activate  # Activate the Virtual Environment
pip install -r requirements.txt  # Install all the dependencies
```

### Loading the initial data

Make sure you have a running instance of MongoDB bound to `127.0.0.1:27017`

```bash
flask load_data  # Unless you defined flask alias, the command would be `python manage.py`
```

### Running the application

```bash
flask runserver  # Runs with development configuration
```

### Running the tests

```
tests
```

## License

See LICENSE

