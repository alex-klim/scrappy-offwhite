from celery import Celery
from celery.task import Task
from pymongo import MongoClient


app = Celery(broker='redis://localhost:6379')
conn = MongoClient('localhost', port=27017)
db = conn['offwhitedb']

@app.task(name="add_product")
def add_product(item):
    db.products.insert_one(item)

@app.task(name="add_price")
def add_price(item):
    db.price.insert_one(item)

if __name__ == '__main__':
    app.worker_main()
