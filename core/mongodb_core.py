import asyncio
import json

from pymongo import MongoClient
from objects.covid_case import CovidCase
from data_mapper import map_covid_data

from stopwatch import Stopwatch
import log_service

client = MongoClient("localhost", 27017)
db = client['covid']


async def add_initial_covid_data():
    covid_cases = await map_covid_data()
    copy = []
    for case in covid_cases:
        copy.append(case.__dict__)
    await log_service.log_event("Running MongoDB bulk data insertion of COVID-19 Data")
    timer = Stopwatch()
    timer.start()
    
    cases_collection = db.get_collection("cases")
    cases_collection.insert_many({"data":data} for data in covid_cases).inserted_ids
    
    timer.stop()
    await log_service.log_event("Finished inserting data. Time was: " + str(timer))

asyncio.run(add_initial_covid_data())