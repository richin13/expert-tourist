from flask_script import Manager
from flask_migrate import MigrateCommand

from expert_tourist import app

manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def load_data():
    from expert_tourist.models import PlaceLoader
    loader = PlaceLoader()
    loader.to_db()

if __name__ == '__main__':
    manager.run()
