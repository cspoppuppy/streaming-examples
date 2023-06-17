# Streaming Examples

## Setup
---
- Install and run Confluent Kafka with Docker using this quick start: https://docs.confluent.io/platform/current/platform-quickstart.html

- Use this repo to setup Python virtual environment and install dependencies: 
    ```bash
    python -m venv venv
    source venv/bin/activate
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

-c = classification (avro (default), json, transactional) [Optioanl]
-d = dataset (e.g. pageviews (default)) [Optional]
-t = topic name (e.g. pageviews (default)) [Optional]
-b = bootstrap server (e.g. localhost:9092 (default)) [Optional]
-s = schema registry (e.g. http://localhost: 8081 (default)) [Optional]
-n = number of messages to produce (e.g. 10 (default)) - [Optional]


### Spark Structured Streaming


### Spark + Hudi DeltaStreaming


### Query Ingested Data
