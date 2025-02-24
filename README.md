# Test Generation API

Using FastAPI to create API that can generate and manage tests based on the provided dataset. The generated tests are specific to a user and allow optional parameters such as category filtering and autofill.

### Build

There is docker-compose configuration, which you can build and run using:

```
docker-compose up --build
```

### Running AWS DynamoDB locally

After running the system, you should attach to your localstack container and create AWS table there.

```
docker exec -it localstack sh

aws dynamodb create-table \
    --endpoint-url=http://localhost:4566 \
    --table-name AppData \
    --attribute-definitions \
        AttributeName=PK,AttributeType=S \
        AttributeName=SK,AttributeType=S \
    --key-schema \
        AttributeName=PK,KeyType=HASH \
        AttributeName=SK,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

To check if everything is working properly, please use:

```
aws dynamodb list-tables --endpoint-url=http://localhost:4566 --region us-east-1
aws dynamodb describe-table --table-name AppData --endpoint-url=http://localhost:4566 --region us-east-1
```

To view all items in the AppData table:

```
aws dynamodb scan --table-name AppData --endpoint-url=http://localhost:4566 --region us-east-1
```

### Populating database

After initialization of the database, you should attach to your localstack container and create AWS table there.

```
docker exec -it fastapi_app sh

cd app/
python populate_db.py
```
