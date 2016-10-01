from sqlalchemydb import AlchemyDB
from sqlalchemy import Table, Column, Integer, String, VARCHAR, ForeignKey


class CrawlerDB(AlchemyDB):

    @classmethod
    def init(cls):
            AlchemyDB.init()

            CrawlerDB.urls = Table('url', CrawlerDB.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('url', String(100), unique=True),
                         Column('code', String(100)),
                         )

            CrawlerDB._table["urls"] = CrawlerDB.urls

            CrawlerDB.category = Table('category', CrawlerDB.metadata,
                             Column('id', Integer, primary_key=True, autoincrement=True),
                             Column('name', VARCHAR(250), nullable=False),
                             Column('preference', Integer))

            CrawlerDB._table["category"] = CrawlerDB.category

            CrawlerDB.acronym = Table('acronym', CrawlerDB.metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('category_id', Integer, ForeignKey("category.id")),
                            Column('name', VARCHAR(250), nullable=False),
                            Column('value', VARCHAR(250), nullable=False),
                            )

            CrawlerDB._table["acronym"] = CrawlerDB.acronym
