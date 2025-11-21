# Dealz

A application for tracking products and prices.

## Prerequisites

- Python 3.14+
- PostgreSQL database
- pip or conda

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd dealz
   ```

2. **Create a Conda environment**

   ```bash
   conda create -n dealz-env python=3.14
   conda activate dealz-env
   ```

3. **Install dependencies**

   ```bash
   cd server
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the `server/` directory with the following variables:

   ```env
   DB_DRIVER=postgresql
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=dev-dealz
   ```

5. **Run database migrations or start the application**
   ```bash
   cd server
   alembic upgrade head
   # or
   uvicorn main:app --reload
   ```

## Database Migrations

### Create a new migration

```bash
cd server
alembic revision --autogenerate -m "Added new model..."
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migrations

```bash
alembic downgrade -1
```

### Check current migration

```bash
alembic current
```

## License

MIT
