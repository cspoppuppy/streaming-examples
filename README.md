# Streaming Examples
*Derived from @danielfordfc [python-playground](https://github.com/danielfordfc/python-playground)*

Data source: Confluent Kafka \
Destination: Hudi Table (local) \
Streaming Options:
- Hudi Deltastreamer (not able to handle Kafka transactional topic)
- Spark Structured Streaming + [ABRiS](https://github.com/AbsaOSS/ABRiS/tree/master) (to handle schema evolution)

## Setup
---
- Install and run Confluent Kafka with Docker using this quick start: https://docs.confluent.io/platform/current/platform-quickstart.html

- Use this repo to setup Python virtual environment and install dependencies: 
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## How to use
---

### Produce Kafka topic
```bash
# produce avro topic using pageviews dataset
python kafka/produce.py -c avro -d pageviews -t pageviews-avro
# produce json topic using pageviews dataset
python kafka/produce.py -c json -d pageviews -t pageviews-json
# produce transactional topic using pageviews dataset
python kafka/produce.py -c transactional -d pageviews -t pageviews-trans
```

-c = classification (avro (default), json, transactional) [Optioanl] \
-d = dataset (e.g. pageviews (default)) [Optional] \
-t = topic name (e.g. pageviews (default)) [Optional] \
-b = bootstrap server (e.g. localhost:9092 (default)) [Optional] \
-s = schema registry (e.g. http://localhost: 8081 (default)) [Optional] \
-n = number of messages to produce (e.g. 10 (default)) - [Optional]


### Spark Structured Streaming
```bash
bash ./bin/spark_structured_streaming.sh -o hudi_ss -t pageviews-avro
```

-o = output dir (required) \
-t = topic name (required) \
-b = base path (optional) - defaults to /tmp/warehouse/spark/{output dir} \
-l = log4j path (optional) - defaults to local log4j2.properties file \
-d = debug bool (optional) - defaults to false - set to true to enable debug logging

Test Schema Evolution
1. Ingest data with initial schema
```bash
# Produce data with initial schema
python kafka/produce.py -c avro -d pageviews -t pageviews-avro
# Ingest data
bash ./bin/spark_structured_streaming.sh -o hudi_ss -t pageviews-avro
# Check data
bash ./bin/spark_query.sh -o hudi_ss -t pageviews-avro
```

2. Ingest data with evolved schema (extra column `test1`)
```bash
# Produce data with evolved schema
python kafka/produce.py -c avro -d pageviews1 -t pageviews-avro
# Ingest data
bash ./bin/spark_structured_streaming.sh -o hudi_ss -t pageviews-avro
# Check data, should see extra column `test1`
bash ./bin/spark_query.sh -o hudi_ss -t pageviews-avro
```

3. Ingest data with intial schema (remove column `test1`)
```bash
# Produce data with evolved schema
python kafka/produce.py -c avro -d pageviews -t pageviews-avro
# Ingest data
bash ./bin/spark_structured_streaming.sh -o hudi_ss -t pageviews-avro
# Check data, should still see extra column `test1` with null values
bash ./bin/spark_query.sh -o hudi_ss -t pageviews-avro
```

4. Delete hudi table and ingest again from beginning
```bash
# Remove hudi table
rm -rf /tmp/warehouse/spark/hudi_ss/pageviews-avro
# Ingest data
bash ./bin/spark_structured_streaming.sh -o hudi_ss -t pageviews-avro
# Check data, should see the same as step 3
bash ./bin/spark_query.sh -o hudi_ss -t pageviews-avro
```


### Spark + Hudi DeltaStreaming
```bash
bash ./bin/spark_hudi_deltastreamer.sh -o hudi_dt -t pageviews-avro
```

-o = output dir (required) \
-t = topic name (required) \
-b = base path (optional) - defaults to /tmp/warehouse/spark/{output dir} \
-l = log4j path (optional) - defaults to local log4j2.properties file \
-d = debug bool (optional) - defaults to false - set to true to enable debug logging

*If not using pageviews topic, will require to amend the key fields in `hoodie-conf.properties` file*

### Query Ingested Data (Hudi table)
```bash
bash ./bin/spark_query.sh -o hudi_ss -t pageviews-avro
bash ./bin/spark_query.sh -o hudi_dt -t pageviews-avro
```

-o = output dir (required) \
-t = topic name (required) \
-b = base path (optional) - defaults to /tmp/warehouse/spark/{output dir} \
-l = log4j path (optional) - defaults to local log4j2.properties file \
-d = debug bool (optional) - defaults to false - set to true to enable debug logging
