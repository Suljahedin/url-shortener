# URL Shortener API

A RESTful URL shortener API built with Python, FastAPI, and SQLAlchemy. It allows users to create short URLs, redirect to original destinations, track link clicks, and manage stored URLs through HTTP endpoints.

## Features

- **Create short URLs** — Generate unique, six-character alphanumeric codes.
- **URL redirection** — Redirect short URLs to their original destinations using HTTP 307.
- **Click tracking** — Track how many times each short URL has been accessed.
- **List URLs** — Retrieve stored URLs with pagination.
- **Search URLs** — Filter URLs by their original destination.
- **Retrieve URL details** — Get information about a specific URL.
- **Delete URLs** — Remove stored URLs.
- **Input validation** — Validate URLs and query parameters.
- **Automated tests** — Test API endpoints and important application behavior.
- **Interactive API documentation** — Explore and test endpoints through Swagger UI.

## Tech Stack

- **Python 3.12+**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Pytest**
- **uv**

## Project Structure

```text
url-shortener/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── redirects.py
│   │   │   └── urls.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── tests/
│   │   └── test_urls.py
│   ├── pyproject.toml
│   └── uv.lock
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

### Installation

Clone the repository:

```bash
git clone https://github.com/Suljahedin/url-shortener.git
cd url-shortener/backend
```

Install dependencies:

```bash
uv sync
```

### Run the API

Start the development server:

```bash
uv run fastapi dev app/main.py
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive Swagger documentation:

`http://127.0.0.1:8000/docs`

Alternative API documentation:

`http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/urls` | Create a short URL |
| GET | `/urls` | List URLs with pagination and search |
| GET | `/urls/{url_id}` | Retrieve URL details |
| DELETE | `/urls/{url_id}` | Delete a URL |
| GET | `/{short_code}` | Redirect to the original URL |

### Create a Short URL

**Request**

`POST /urls`

```json
{
  "original_url": "https://www.python.org/"
}
```

**Example response — `201 Created`**

```json
{
  "id": 1,
  "original_url": "https://www.python.org/",
  "short_code": "aB3xQ7",
  "click_count": 0,
  "created_at": "2026-10-29T20:00:00"
}
```

The generated short code will vary.

### List URLs

`GET /urls`

Optional query parameters:

| Parameter | Default | Description |
|---|---:|---|
| `skip` | `0` | Number of records to skip |
| `limit` | `10` | Number of records to return, from 1 to 100 |
| `search` | None | Search within original URLs |

Examples:

```text
GET /urls?skip=0&limit=10
GET /urls?skip=10&limit=10
GET /urls?search=python
```

### Retrieve URL Details

`GET /urls/1`

Returns the URL record with the specified ID, including its click count.

### Redirect to the Original URL

`GET /aB3xQ7`

Redirects the client to the original destination and increments the click count.

### Delete a URL

`DELETE /urls/1`

Deletes the URL record and returns `204 No Content` when successful.

## Running Tests

Run the automated test suite from the `backend` directory:

```bash
uv run pytest -v
```

The tests cover URL creation, listing, pagination, search, retrieval of missing URLs, deletion, redirects, click tracking, and invalid pagination parameters.

## Database

The application uses SQLite with SQLAlchemy ORM. The database file is created locally when the application starts.

The local database is excluded from version control.

## Future Improvements

Potential improvements include:

- Database migrations with Alembic
- More comprehensive error handling
- Rate limiting and abuse prevention
- Expiration dates for short URLs
- Custom short codes
- Deployment and production configuration

## License

See the [LICENSE](LICENSE) file for license information.
