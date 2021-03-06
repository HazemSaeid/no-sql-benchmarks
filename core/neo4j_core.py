import py2neo as neo
import asyncio
from covid_case import CovidCase
import log_service
import data_mapper
from stopwatch import Stopwatch

graph = neo.Graph("bolt://localhost:7687", auth=("neo4j", "1234"))


async def add_covid_data():
    cases = await data_mapper.map_covid_data()
    tx = graph.begin()
    await log_service.log_event("adding COVID-19 data to Neo4j")
    timer = Stopwatch()
    timer.start()
    for case in cases:
        state = neo.Node("State", name=case.state)
        county = neo.Node("County", name=case.county)
        cases = neo.Node("Cases", date=case.date, amount=case.cases, deaths=case.deaths)

        state_rel_county = neo.Relationship(state, "HAS", county)
        county_rel_cases = neo.Relationship(county, "REGISTERED", cases)

        tx.merge(state, primary_label="State", primary_key=("name"))
        tx.merge(county, primary_label="County", primary_key=("name"))
        tx.merge(state_rel_county, primary_label="HAS", primary_key=("state", "county"))
        tx.create(cases)
        tx.create(county_rel_cases)
    timer.stop()
    tx.commit()
    await log_service.log_event("Finished inserting data. Time was: " + str(timer))


async def retrieve_covid_data():
    await log_service.log_event("Retrieving 5000 nodes with relationships from Neo4j")
    timer = Stopwatch()
    timer.start()

    graph.run('MATCH (s:State)-[h:HAS]-(c:County)-[r:REGISTERED]-(ca:Cases) RETURN s, h, c, r, ca limit 5000')

    timer.stop()
    await log_service.log_event("Finished retrieving 5000 nodes. Time was: " + str(timer))


async def delete_covid_data():
    await log_service.log_event("Deleting COVID nodes and relationships from Neo4j")
    timer = Stopwatch()
    timer.start()

    graph.run('MATCH (n) DETACH DELETE n')

    timer.stop()
    await log_service.log_event("Finished deleting nodes and relationships . Time was: " + str(timer))


# asyncio.run(add_covid_data())
# asyncio.run(retrieve_covid_data())
# asyncio.run(delete_covid_data())
