## NoSQL Benchmark comparison
This project focuses on the comparison of mongoDB and Neo4j. The comparisons includes: 
* Data insertion and deletion
* Data Processing  
* Scalability
* Data/Schema modelling
* Security

### Problem statement
NoSQL data processing in a relational context. 

In this project, we are trying to process covid-19 data in noSQL databases with and mapping them in their specific domain.

This thesis mostly focuses on insertion and reading of data in MongoDB and Neo4J
### Neo4j 

###### Data/Schema modelling 
The Graph data model is a very simple and straightforward model(Also called "Whiteboard friendly"). Its design components consist of **Nodes**, **Labels** and **Relationships**  
**Nodes:** Entities/objects  
**Labels:** Name of the Node  
**Relationship:** The relation between a pair(or more) of nodes

###### Scalability
Just like most of NoSQL databases, Neo4j is also known for scaling horizontically(sharding). This has the advantage of distributing the load across multiple servers or clusters.


###### Security


###### Data processing, insertion and deletion

*adding COVID-19 data to Neo4j*  
```python
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
```
*Finished inserting data. Time was: **206.96s*** 

*Retrieving 5000 nodes with relationships from Neo4j*  
```python
async def retrieve_covid_data():
    await log_service.log_event("Retrieving 5000 nodes with relationships from Neo4j")
    timer = Stopwatch()
    timer.start()

    graph.run('MATCH (s:State)-[h:HAS]-(c:County)-[r:REGISTERED]-(ca:Cases) RETURN s, h, c, r, ca limit 5000')

    timer.stop()
    await log_service.log_event("Finished retrieving 5000 nodes. Time was: " + str(timer))
```
*Finished retrieving 5000 nodes. Time was: **4.74s*** 

*Deleting COVID nodes and relationships from Neo4j*  
```python
async def delete_covid_data():
    await log_service.log_event("Deleting COVID nodes and relationships from Neo4j")
    timer = Stopwatch()
    timer.start()

    graph.run('MATCH (n) DETACH DELETE n')

    timer.stop()
    await log_service.log_event("Finished deleting nodes and relationships . Time was: " + str(timer))
```
*Finished deleting nodes and relationships . Time was: **2.39s*** 



### MongoDB

###### Scalability

mongoDB is also known for horizontal scaling of documents.

###### Security
MongoDB offers network encryption and can pass through disk encryption to help you protect your database and communications. TLS and SSL are both standard technologies that are used for encrypting network traffic.

## What is sharding in MongoDB?
Sharding in MongoDB is a method for distributing data across multiple machines. Sharding os the 'scalability' of the database, that could boost the performance because of the separated workload. Database sharding can consist in two forms: Vertical and Horizontal. 

_**Vertical:**_ Increasing capacity on a single server, so that the storage, CPU and RAM increases. 
_**Horizontal:**_ Diving dataset and the load over to multiple servers. 

## What are the different components required to implement sharding?

*   Shard: A subset of the sharded data distributed to the specific machine
*   mongos: query-router. Interface for an application to communicate with a sharded cluster(applications does not communicated directly with the shards). 
*   config-servers: Servers specially configured for sharding purposes

## Explaing the architecture of sharding in MongoDB


![](/ShardingArchitecture.PNG)


###### Data/Schema modelling
The modelling process consists of designing schemas using JSON structure. 
Things to consider when designing the schema, is to get familiar with the different ways of designing "relational" data and its given "one-to-N" relations. mongoDB gives the freemdom of choice in regards og document-design and "relational" mapping.

###### Logs from Data processing, insertion and deletion


*Running MongoDB bulk data insertion of COVID-19 Data*  
```python
async def add_initial_covid_data():
    covid_cases = await map_covid_data()
    await log_service.log_event("Running MongoDB bulk data insertion of COVID-19 Data")

    timer = Stopwatch()
    timer.start()
    
    db.cases.insert_many([case.__dict__ for case in covid_cases])
    
    timer.stop()
    await log_service.log_event("Finished inserting data. Time was: " + str(timer))
```
*Finished inserting data. Time was: **356.13ms***

*Retrieving 5000 documents from Mongodb*  
```python
async def retrieve_covid_data():
    await log_service.log_event("Retrieving 5000 documents from Mongodb")

    timer = Stopwatch()
    timer.start()
    
    db.cases.find({}).limit(5000)
    
    timer.stop()
    await log_service.log_event("Finished retrieving 5000 documents. Time was: " + str(timer))
```
*Finished retrieving 5000 documents. Time was: **1.56s*** 

*Deleting all COVID documents from Mongodb*  
```python
async def delete_covid_data():
    await log_service.log_event("Deleting all COVID documents from Mongodb")

    timer = Stopwatch()
    timer.start()
    
    db.cases.delete_many({})
    
    timer.stop()
    await log_service.log_event("Finished deleting documents. Time was: " + str(timer))
```
*Finished deleting documents. Time was: **254.47ms*** 


### Conclusion
Looking at these test results, we saw a huge difference in insertion of data. MongoDB offered a more extensive API for its database operations(such as bulk_insert), where this was not possible in Neo4J. While also looking at all the benchmarks, mongodb has the better score in regards of reading, writing and processing data. In addition to that, mongoDB also offers a "relational" solution for noSQL databases(like Neo4J) with a more complex design process.



