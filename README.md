# RAG-LLM
## Introduction
This repository contains the python code to store knowledge base and retrieve related movies by query.

## Container Setup
1. Clone the repository
2. Create .env file from .env.example (at the same level of .env.example)
3. Build the docker image using docker-compose
    ```bash
    docker-compose up
    ```
4. Let create the token to access knowledge base by running create token API
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/create-token/' \
      -H 'accept: application/json' \
      -d ''
    ```
    The token will be printed out in console and log file (at your local machine).
    The token is used to manage the knowledge base.
5. Run sync knowledge base API to embed all data of mongodb into knowledge base. 
If you have your own mongodb, please update the MONGODB_URI and MONGODB_DB in .env file.
It will consume a lot of time to embed all data into knowledge base.

**Note:** If you want to watch the logs easily in app container, you can modify configuration of structlog.
```
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)
```
## Usage
1. Run the docker container
2. Open the browser and go to `http://localhost:8000/docs` (swagger UI) and `http://localhost:8000/redoc` (redoc UI)
3. To developer, they should use retriever API to retrieve the related movies by query.
4. To admin, they should use knowledge base API to manage the knowledge base.

## How to get google api key
1. Go to https://ai.google.dev/gemini-api/docs/
2. Click on `Get a Gemini API Key` button
3. Create API key and copy it

## Project structure
```
|-- app
|   |-- api
|   |   |-- __init__.py
|   |   |-- create_token.py
|   |   |-- knowledge_base.py
|   |   |-- rag.py
|   |   |-- retriever.py
|   |-- models
|   |   |-- request_model.py
|   |   |-- response_model.py
|   |-- services
|   |   |-- knowledge_base_service.py
|   |   |-- model_service.py
|   |   |-- rag_service.py
|   |   |-- retriever_service.py
|   |   |-- tmdb_service.py
|   |-- utils
|   |   |-- decode_jwt.py
|   |   |-- exceptions.py
|   |   |-- transform_document.py
|   |   |-- vector_store.py
|   |-- main.py
|-- run.py
|-- ...
```

- **api:** Contains the API endpoints
- **models:** Contains the request and response models (interface)
- **services:** Contains the business logic
- **utils:** Contains the utility functions
- **main.py:** Contains the FastAPI application
- **run.py:** Contains the code to run the FastAPI application

## API Endpoints
### APIs used for building web applications (developer)
- **GET /healthy:** Check the health of the service
- **GET /knowledge_base/collections:** Get all collections in knowledge base
- **GET /retriever/:** Retrieve related movies by query in given collection

### APIs manage knowledge base (Should be used by admin)
- **POST /create-token/:** Create token to access knowledge base (Print out in console and log file)
- **POST /knowledge-base/sync:** Sync knowledge base with the given collection 
- **POST /knowledge-base/sync-with-auto-retry:** Sync knowledge base with the given collection with auto retry
- **POST /knowledge-base/drop:** Drop the all collections in knowledge base
