import couchdb
from objects.covid_case import CovidCase,CovidCaseEncoder
import csv
import json
import asyncio
import data_mapper

couch = couchdb.Server('http://admin:password@localhost:5984/')

db = couch['covid']

async def add_covid_data_from_csv():
    covid_cases = await data_mapper.map_covid_data()
    db.save(json.dumps(covid_cases))


asyncio.run(add_covid_data_from_csv())