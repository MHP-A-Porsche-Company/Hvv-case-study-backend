# REST API for Geographical Measurements

## Introduction

This project is a REST API developed using Python's FastAPI framework. The API exposes two endpoints, `/measurements`, which allows users to query measurements data by filtering based on years and geographical entities (such as countries or regions) as well as `/docs`, which provides a Swagger UI for interactive documentation.

The data is managed using `pandas` to handle the underlying data as a DataFrame or basically to mock a database , and caching is implemented using `fastapi-cache2` to improve performance.
The project uses `poetry` for dependency management, and `uvicorn` is used to run the FastAPI server. Unit tests are written using Python's built-in `unittest` module.

Also, there is a example script in the data directory how one could import the data in a time series database like `InfluxDB` for further development.

## Usage

### Locally (Without Docker):
1. Install dependencies:
```bash
poetry install
```

2. Run the API server:
```bash
cd src
uvicorn main:app --reload 
```

### Using Docker:
1. Build the Docker image:
```bash
docker build -t fastapi-measurements-api .
```
2. Run the Docker container:
```bash
docker run -d -p 8000:8000 fastapi-measurements-api
```

### Endpoint: `/docs`
Provides an interactive Swagger documentation.
```
- **Method**: `GET`
```
### Endpoint: `/measurements`
Queries geographical measurement data based on provided parameters (years and entities). The more filters you set, the fewer data you receive / operate on. 
```
- **Method**: `GET`
- **Parameters**:
    - `years` (optional): A comma-separated list of years (e.g. `2019,2020,2021`). If not provided, no filtering by year is applied.
    - `entities` (optional): A comma-separated list of geographical entities (countries or regions, e.g., `Germany,China`). If not provided, no filtering by entities is applied.

### Example Request:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/measurements?years=2019,2020&entities=Germany,China' \
  -H 'accept: application/json'
```

## Technical Decisions (Dependencies)

### Poetry
poetry is used for managing dependencies and packaging. It's a modern dependency management tool that simplifies package installation, virtual environment creation, and version control.

### FastAPI
We chose FastAPI for its simplicity and speed. It provides a simple and intuitive way to define REST endpoints while also handling input validation and output serialization. FastAPI's asynchronous nature also makes it suitable for high-performance APIs.

### fastapi-cache2
To improve the performance of the API, fastapi-cache2 is used to cache API responses. This reduces the load on the server by serving previously cached responses to repeated queries, especially when the data doesn't change frequently.

### pandas
pandas is used to simulate a database of measurements in a DataFrame. This allows for easy data manipulation and filtering based on the provided query parameters (years, entities). While in real-world applications, a database such as PostgreSQL or MongoDB would be used, pandas is ideal for rapid prototyping.

### uvicorn
uvicorn is used as the ASGI server to run FastAPI. It's lightweight and highly efficient for serving asynchronous web applications.

### Unittest
unittest is chosen for writing unit tests. It's a built-in Python module that provides a framework for testing code and ensures that API functionality behaves as expected.

## Security
The current API is intended for local use and rapid development, but it can be expanded with security features for production:

### Kubernetes
In a Kubernetes environment, we recommend leveraging Kubernetes tools for authentication (authN), authorization (authZ), and encryption. 
This approach ensures security is managed at a unified, platform-wide level, reducing complexity at the application layer.

We also advocate for using Istio as a service mesh layer in conjunction with Open Policy Agent (OPA). 
Together, these tools provide comprehensive control over intra-cluster communication, as well as ingress and egress traffic for all deployed services. 
By adopting this approach, you eliminate the need to implement security mechanisms within each individual service. 
Moreover, these tools offer a robust set of APIs for monitoring and observability, simplifying management and ensuring better operational insights.

If necessary you could also forward auth tokens to the database to enable more granular authorization like cell level if needed.  

### Implementation in service

#### Authentication
Possible technical solutions for implementing authentication checks would be simple authorization header / tokens or full-blown OAuth2 implementation, depending on the given situation.

#### Authorization
Implementing authentication could be also done less or more complex depending on the outer requirements and systems. A simple solution could be implementing RBAC with JWT. 
A more advanced solution would be using Open Policy Agent in the Python application. This would provide more flexibility as well as a centralized system for managing.

#### Encryption
We would recommend enabling TLS / Https if the application is facing the public / private internet. Also use external services to manage and validate certificates.
