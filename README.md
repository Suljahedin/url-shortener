# URL Shortener

A full-stack URL shortener built with Python, FastAPI, SQLite, SQLAlchemy, and Next.js.

## Project Status

🚧 In development.

The backend is being built first. The frontend will be added after the API is implemented and tested.

## Planned Features

- [ ] Create short URLs from long URLs
- [ ] Redirect users to original URLs
- [ ] Store URLs in a SQLite database
- [ ] Track click counts
- [ ] View URL statistics
- [ ] Delete shortened URLs
- [ ] Automated API tests
- [ ] Build a Next.js frontend

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest

### Frontend

- Next.js
- React
- TypeScript

## Development

The backend uses `uv` for Python dependency and environment management.

```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```

Once the API is running, visit http://127.0.0.1:8000/docs to explore the interactive API documentation.

## License

Not yet specified.
