[![Build Status](https://travis-ci.org/richin13/expert-tourist.svg?branch=master)](https://travis-ci.org/richin13/expert-tourist) [![license](https://img.shields.io/github/license/richin13/expert-tourist.svg)](https://opensource.org/licenses/MIT)

# expert-tourist

# Setup [Backend]

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
echo 'alias runtests="pytest --ignore=react-app"' >> venv/bin/activate
source venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

## Apply the migrations

```bash
flask upgrade
flask migrate
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

# Setup [Fontend]


## First steps

First, `cd` into **react-app** directory

You must install `yarn`. To do that, run the following command

```
npm install yarn -g # bye bye, npm :p
```

## Install the dependencies

```
yarn install
```

## Build the project

```
yarn build
```

## Start the project

```
yarn start
```

Happy hacking!


## TODO

 - Add hot loaders
 - Remove extra and unused dependencies
 - Clean package.json


## License

See LICENSE

