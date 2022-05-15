from flask_script import Manager,Server
from app import create_app,db

from flask_migrate import Migrate, MigrateCommand
from app.models import *

from app import create_app

app = create_app('development')




if __name__ == '__main__':
    app.run(debug=True)