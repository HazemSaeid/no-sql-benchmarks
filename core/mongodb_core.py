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

asyncio.run(add_initial_covid_data())