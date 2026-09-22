# Weather API Ingestion

***A small Python project I built to practice working with APIs and improve my data engineering skills.***

## What I Practiced

- Building a reusable API client in Python
- Working with REST APIs using `requests`
- Using Python classes and type hints
- Managing API credentials with environment variables
- Making multiple API requests concurrently
- Handling HTTP, connection, timeout, and JSON errors
- Working with nested JSON responses
- Saving raw API responses
- Transforming semi-structured API data into tabular data
- Using Pandas for basic data transformation

## What the Project Does

The project gets weather data for multiple cities from the OpenWeatherMap API.

The basic flow is:

```text
OpenWeatherMap API
        ↓
Python API Client
        ↓
Parallel API Endpoint Requests
        ↓
JSON File
        ↓
Transform Data
        ↓
Pandas DataFrame
```


## Why I Built This

This was a **Sunday practice project**, mainly to get more comfortable with Python API ingestion, ***concurrent*** requests, JSON handling, and basic data transformation.

It's not intended to be a production-ready pipeline. The goal was simply to practice and understand the concepts by building something myself.

---
