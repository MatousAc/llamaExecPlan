## Ideas:

Graph DB for relations between mathematical equations.

Implement Entropy-learned Hashing in a No-SQL DB.

Software that identifies common data objects in Excel sheets/confused tables and tries to separate them into a proper RDBMS. Basically normalization?

Software that identifies common data objects in Excel sheets/confused tables and tries to separate them into a proper RDBMS. Basically normalization?

A follow-up using Weka-3 for clustering University data.

In-parallel processing of tuples for loosely joined tables (what does loosely joined tables mean?)

Parallelizing a single query if it has multiple joins

Comparison of cost and performance between Azure and AWS for storing and serving Weather data.



Real ideas:

A tool to create TypeScript classes from SQL db tables.

Hybridize indexing and hashing


Machine learning for block transfer or buffer management

Reverse engineering Relational Algebra

Training a model to understand relational algebra (Find SQL query DB, translate to relational algebra)

Reverse engineering Relational Algebra

Try prefetching blocks from related tables to optimize time


Apply web routing algorithms for index searches.​

Compare GPU to CPU SQL Query execution time
Combine in-memory DB on GPU
How to get memory information/block size from C++ in Linux.

## In-
Comparing time execution of different queries between hard drive and memory.

Questions to answer:
* Is in-memory faster?
* Which types of queries gain the most performance between databases?
* How to cloud databases compare to local ones? (Stretch goal. Focus on Cloud DB for now)
### Databases to use potentially
||Local|Cloud|
|-|-|-|
|**Storage**|SQL Server, PostgresQL, MySQL|AWS Aurora DB (PostgreSQL, MySQL)|
|**In-memory**|Apache Derby, H2|Amazon MemoryDB|

Data we can analyze:
* Query execution speed
  * SQL server gives this automatically
  * AWS Aurora DB - MySQL should provide this in [logs](https://dev.mysql.com/doc/refman/8.0/en/query-log.html)
  * Manually configuring a simple timer might work too?
* Rows/sec
* Block hits/sec
* Block reads/sec
* Block writes/sec
* CPU Utilization
  * Should be possible for local dbs
  * Possible for cloud [link](https://dev.mysql.com/doc/refman/8.0/en/query-log.html)
* Network congestion/traffic [link](https://dev.mysql.com/doc/refman/8.0/en/query-log.html)
* Memory use percentage [link](https://docs.aws.amazon.com/memorydb/latest/devguide/metrics.memorydb.html)
* 


# LLM Optimization
(Testing) Query Optimization with GAI

Use Llama 2 to generate better queries.

Database design with LLMs
  

- The problem: Automatic current approaches for query optimization may not be so efficient (deficient heuristics).
- The solution: Propose a prototype that uses GAI to propose an optimized query plan (we're going to cover the topic of query optimization on Monday). The user inputs the information about the set of tables, relationships, attributes, indexes, and number of records per table to the model. The model returns an optimized plan. 
- Evaluation: Evaluate the execution time of the original query vs. the optimized query on a set of popular DBMSs. 
If someone is interested in doing this, you should have prior knowledge on GAI (LLMs) and hopefully experience with LLAMA. If so, send an email to everyone to "lock" this project.