from objects.covid_case import CovidCase
import asyncio
import csv
import json

async def map_covid_data():
    covid_cases = []
    with open(r"data\us-counties.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            obj = CovidCase(line[0], line[1], line[2], line[3], int(line[4]), int(line[5]))
            covid_cases.append(obj)
    return covid_cases
