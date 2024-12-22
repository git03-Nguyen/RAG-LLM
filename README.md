# RAG-LLM
## Introduction
This repository contains the python code to store knowledge base and retrieve related movies by query.

## Container Setup
1. Clone the repository
2. Build the docker image using docker-compose
```bash
docker-compose up
```

## Usage
1. Run the docker container
2. Open the browser and go to `http://localhost:8000/docs`
3. To developer, they should use retriever API to retrieve the related movies by query.
4. To admin, they should use knowledge base API to manage the knowledge base.

## How to get google api key
1. Go to https://ai.google.dev/gemini-api/docs/
2. Click on `Get a Gemini API Key` button
3. Create API key and copy it