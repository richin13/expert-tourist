[![Build Status](https://travis-ci.org/richin13/expert-tourist.svg?branch=master)](https://travis-ci.org/richin13/expert-tourist) [![license](https://img.shields.io/github/license/richin13/expert-tourist.svg)](https://opensource.org/licenses/MIT)

# expert-tourist

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
source venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

## Running the app

Simply run 

```bash
python run.py
```

## Running tests

Simply run 

```bash
python setup.py test
```

## License

See LICENSE

