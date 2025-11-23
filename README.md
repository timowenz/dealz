# Dealz

An application for tracking products and prices.

## Prerequisites

- Python 3.14+
- PostgreSQL database
- pip or conda
- Node.js (for Vite client)

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:timowenz/dealz.git
cd dealz
```

### 2. Server Setup

#### a. Create a Conda environment

```bash
conda create -n dealz-env python=3.14
conda activate dealz-env
```

#### b. Install server dependencies

```bash
cd server
pip install -r requirements.txt
```

#### c. Configure environment variables

Create a `.env` file in the `server/` directory with the following variables:

```env
DB_DRIVER=postgresql
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dev-dealz
```

#### d. Run database migrations or start the application

```bash
cd server
alembic upgrade head
# or
uvicorn main:app --reload
```

---

### 3. Vite Client Setup

The client application is located in the `client` directory and uses Vite.

#### a. Install Node.js dependencies

```bash
cd ./client
npm install
```

#### b. Start the Vite development server

```bash
npm run dev
```

The client will be running on [http://localhost:5173](http://localhost:5173).

---

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
