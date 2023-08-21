# Exchange Rates API

A service that provides the current exchange rate and the history of the exchange rate via HTTP REST API,
with access only for authorized users.

The base currency is USD. The exchange rates are provided by the [Exchangerate.host](https://github.com/Formicka/exchangerate.host)
The history is available for each day.

Framework: FastAPI.
Database: PostgreSQL.
Cache: Redis.

# Quick Start

Prerequisites:
- Docker
- Docker Compose

Steps:
1. Clone the repository: `git clone https://github.com/air17/currencies_exchange_fastapi.git`
2. Copy `.env.example` to `.env` and fill in the variables.
3. Start the service: `docker-compose up -d`
4. Access the API docs through your web browser at http://127.0.0.1:8000/api/v1/docs.

Adjust number of workers in `.env` to increase the number of requests per second.
