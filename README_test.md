## How to test:
### Launch Locust
```bash
 locust -f locustfile.py --host http://localhost:8000
```
___
#### 1. If it is necessary to clear Redis of hashes
```bash
docker exec -it redis redis-cli flushdb
```
#### or for all databases
```bash
docker exec -it redis redis-cli flushall
```
#### 2. If it is necessary to clear PostgreSQL of product events
```SQL
TRUNCATE TABLE product_events_productevent RESTART IDENTITY CASCADE;
```