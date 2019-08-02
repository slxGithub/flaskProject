from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from werkzeug.contrib.fixers import ProxyFix

from ihome import create_app, db

app = create_app("develop")
app.wsgi_app = ProxyFix(app.wsgi_app)
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manage.run()
    # app.run()
