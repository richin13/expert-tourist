import os
from flask_script import Manager

from expert_tourist import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'config.DevConfig'))
manager = Manager(app)

@manager.command
def load_data():
    from expert_tourist.models import PlaceLoader
    loader = PlaceLoader()
    loader.to_db()


if __name__ == '__main__':
    manager.run()
