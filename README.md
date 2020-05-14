## NoSQL Benchmark comparison
This project focuses on the comparison of mongoDB and Neo4j. The comparisons includes: 
* Data insertion and deletion
* Data Processing  
* Scalability
* Data/Schema modelling
* Security
### Neo4j 

###### Data/Schema modelling 
The Graph data model is a very simple and straightforward model(Also called "Whiteboard friendly"). Its design components consist of **Nodes**, **Labels** and **Relationships**
**Nodes:** Entities/objects
**Labels:** Name of the Node
**Relationship:** The relation between a pair(or more) of nodes

###### Scalability
Just like most of NoSQL databases, Neo4j is also known for scaling horizontically(sharding). This has the advantage of distributing the load across multiple servers or clusters.


###### Security


###### Logs from Data processing, insertion and deletion

*adding COVID-19 data to Neo4j* 
*Finished inserting data. Time was: **206.96s*** 

*Retrieving 5000 nodes with relationships from Neo4j* 
*Finished retrieving 5000 nodes. Time was: **4.74s*** 

*Deleting COVID nodes and relationships from Neo4j* 
*Finished deleting nodes and relationships . Time was: **2.39s*** 



### MongoDB

###### Scalability

mongoDB is also known for horizontal scaling of documents.

###### Security
MongoDB offers network encryption and can pass through disk encryption to help you protect your database and communications. TLS and SSL are both standard technologies that are used for encrypting network traffic.

###### Data/Schema modelling
The modelling process consists of designing schemas using JSON structure. 
Things to consider when designing the schema, is to get familiar with the different ways of designing "relational" data and its given "one-to-N" relations. mongoDB gives the freemdom of choice in regards og document-design and "relational" mapping.

###### Logs from Data processing, insertion and deletion


*Running MongoDB bulk data insertion of COVID-19 Data*
*Finished inserting data. Time was: **356.13ms***

*Retrieving 5000 documents from Mongodb*
*Finished retrieving 5000 documents. Time was: **1.56s*** 

*Deleting all COVID documents from Mongodb* 
*Finished deleting documents. Time was: **254.47ms*** 


### Conclusion
Looking at these test results, we saw a huge difference in insertion of data. MongoDB offered a more extensive API for its database operations(such as bulk_insert), where this was not possible in Neo4J. While also looking at all the benchmarks, mongodb has the better score in regards of reading, writing and processing data. In addition to that, mongoDB also offers a "relational" solution for noSQL databases(like Neo4J) with a more complex design process.



