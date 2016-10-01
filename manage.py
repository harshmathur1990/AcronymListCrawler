from __init__ import create_app
from flask_script import Manager
from flask_script import Server
from flask_migrate import Migrate, MigrateCommand
from models import CrawlerDB
#
#
# if config.env and config.env in ['production', 'staging']:
#     newrelic_cfg_file = os.path.join(os.getcwd(), "conf", u'newrelic-{}-{}.ini'.format(config.env, config.client))
#     newrelic.agent.initialize(newrelic_cfg_file)

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/crawler?charset=utf8mb4'

db = CrawlerDB()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver", Server(host="localhost", port=9982))
manager.add_command("db", MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
