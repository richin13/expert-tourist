[![Build Status](https://travis-ci.org/richin13/expert-tourist.svg?branch=dev)](https://travis-ci.org/richin13/expert-tourist) [![license](https://img.shields.io/github/license/richin13/expert-tourist.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/richin13/expert-tourist/branch/dev/graph/badge.svg)](https://codecov.io/gh/richin13/expert-tourist)

# expert-tourist

A RESTful API to compute and recommend touristic routes based on user-defined preferences using the Bayes theorem.
For the front-end pair application see [richin13/expert-tourist-react](https://github.com/richin13/expert-tourist-react)

## Setup

Clone the repo

```bash
git clone git@github.com:richin13/expert-tourist.git
cd expert-tourist
```

Create the virtual environment and setup the required ENV vars

```bash
virtualenv venv
echo 'export SECRET_KEY="<secure-value-here>"' >> venv/bin/activate
echo 'export PYTHONPATH="./"' >> venv/bin/activate
echo 'alias flask="python manage.py"' >> venv/bin/activate
echo 'alias runtests="pytest ----disable-pytest-warnings"' >> venv/bin/activate
source venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

## Load the initial data

```bash
flask load_data
```

## Running the app

Simply run 

```bash
flask runserver
```

## Running tests

Simply run 

```bash
runtests
```

Happy hacking!

## License

See LICENSE

