# AcronymListCrawler
This Repository crawls http://www.acronymslist.comand stored acronyms as key value pair in mysql db.

pip install -r requirements.txt

python manage.py shell

from main import *
url = 'http://acronymslist.com/'
do(url=url)
