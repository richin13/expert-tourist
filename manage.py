import os
from flask_script import Manager, prompt_bool

from expert_tourist import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'config.DevConfig'))
manager = Manager(app)

data_manager = Manager(usage='Performs data operations')


@data_manager.command
def load():
    from expert_tourist.models import PlaceDatasetManager
    loader = PlaceDatasetManager()
    loader.load_dataset()


@data_manager.command
def group(field):
    from expert_tourist.models import PlaceDatasetManager
    loader = PlaceDatasetManager()
    grouped_data = loader.group_by(field)
    print(str(grouped_data))


@data_manager.command
def drop():
    if prompt_bool('Are you sure you want to delete all the data from the database? [y/N]'):
        from expert_tourist.models import Place, User
        Place.drop_collection()
        User.drop_collection()


manager.add_command('data', data_manager)

if __name__ == '__main__':
    manager.run()
