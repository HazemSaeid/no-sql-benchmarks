import asyncio
import json
from pymongo import MongoClient
from covid_case import CovidCase
from data_mapper import map_covid_data
from stopwatch import Stopwatch
import log_service

client = MongoClient("localhost", 27017)
db = client['local']


async def add_initial_covid_data():
    covid_cases = await map_covid_data()
    await log_service.log_event("Running MongoDB bulk data insertion of COVID-19 Data")

    timer = Stopwatch()
    timer.start()
    
    db.cases.insert_many([case.__dict__ for case in covid_cases])
    
    timer.stop()
    await log_service.log_event("Finished inserting data. Time was: " + str(timer))


async def retrieve_covid_data():
    await log_service.log_event("Retrieving 5000 documents from Mongodb")

    timer = Stopwatch()
    timer.start()
    
    db.cases.find({}).limit(5000)
    
    timer.stop()
    await log_service.log_event("Finished retrieving 5000 documents. Time was: " + str(timer))


async def delete_covid_data():
    await log_service.log_event("Deleting all COVID documents from Mongodb")

    timer = Stopwatch()
    timer.start()
    
    db.cases.delete_many({})
    
    timer.stop()
    await log_service.log_event("Finished deleting documents. Time was: " + str(timer))


# asyncio.run(add_initial_covid_data())
# asyncio.run(retrieve_covid_data())
# asyncio.run(delete_covid_data())