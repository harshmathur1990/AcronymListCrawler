from flask import Flask
from api import crawl
from models import CrawlerDB
import log


def create_app():
    app = Flask(__name__)
    app.register_blueprint(crawl, url_prefix='/crawl')
    CrawlerDB.init()
    log.setup_logging()
    return app
