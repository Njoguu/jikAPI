# jikAPI
[![Github Issues](https://img.shields.io/github/issues-raw/Njoguu/jik-api-v2.0-Alpha)](https://github.com/Njoguu/jik-api-v2.0-Alpha/issues) 
[![Github pull requests](https://img.shields.io/github/issues-pr-raw/Njoguu/jik-api-v2.0-Alpha?color=yellow)](https://github.com/Njoguu/jik-api-v2.0-Alpha/pulls) <br>
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40jikAPI)](https://twitter.com/@the_jikAPI)
[![jikAPI](https://github.com/Njoguu/jik-api-v2.0-Alpha/actions/workflows/jikAPI.yml/badge.svg)](https://github.com/Njoguu/jik-api-v2.0-Alpha/actions/workflows/jikAPI.yml)
[![Tests](https://github.com/Njoguu/jik-api-v2.0-Alpha/actions/workflows/tests.yml/badge.svg)](https://github.com/Njoguu/jik-api-v2.0-Alpha/actions/workflows/tests.yml)

## Description:
jikAPI (Jobs In Kenya Live API) is a Job Search REST API that provides job postings data to users. It allows users to search for job opportunities that have been recently posted by employers in Kenya. <br>
The API is built using the Flask framework and utilizes PostgreSQL as the database management system.

## Endpoints
The API provides the following endpoints for accessing job postings data:
- `GET /api/v2/jobs` : Retrieves a list of available job postings.
- `POST /api/v2/jobs` : Adds a new job posting to the database.
- `POST /api/v2/jobs/date` : Retrieves job postings posted on a specific date.
- `POST /api/v2/jobs/keyword` : Retrieves jobs with specific keywords. 
- `GET /api/v2/jobs/{id}` : Retrieves a specific job posting with the given id.
- `DELETE /api/v2/jobs/{id}` : Deletes a specific job posting with the given id.
- `PATCH /api/v2/jobs/{id}` : Updates a specific job posting with the given id.

## Usage
To use the API, make HTTP requests to the appropriate endpoint with the desired parameters. The API will return a JSON response with the requested data.

## Development:
### Setup & Installtion

Clone the repository using the following command.

```bash
git clone https://github.com/Njoguu/jik-api-v2.0-Alpha.git
```

### Viewing The App: with Docker
1. Make sure you have docker installed.

2. Navigate to the folder structure then build the container with the command 
```bash 
docker build -t <your-image-name> .
```

3. Run the container with the command 
```bash 
docker run -d -p 5000:5000 <your-image-name>
```

### To view the app

Go to `http://127.0.0.1:5000`

## Tests
To run the API tests, use the following command: `pytest`

## Documentation
The API uses Swagger for API documentation. To access the documentation, navigate to /api/v2/docs in your web browser when the API is running.


