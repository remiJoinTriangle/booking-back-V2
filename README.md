# booking-back-V2

## Setup

### Database Setup

1. Install PostgreSQL (if not already installed):

```bash
brew install postgresql
```

2. Start PostgreSQL service:

```bash
brew services start postgresql
```

3. Create the database:

```bash
createdb astra
```

### Python Setup

4. Create virtual environment (if not already created):

```bash
python -m venv venv
```

5. Activate virtual environment:

```bash
source venv/bin/activate
```

6. Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

7. Set up environment variables:

```bash
cp .env.example .env
```

Then edit `.env` and update the `DATABASE_URL` with your PostgreSQL username and `OPENAI_API_KEY` with an OpenAI API key:

```
DATABASE_URL=postgresql+asyncpg://your_username@localhost:5432/astra
OPENAI_API_KEY=your_openai_api_key
```

8. Run intial migrations:

```bash
alembic upgrade head
```

## Running the Server

From the project root, run:

```bash
uvicorn backend.main:app --reload
```

Note: Make sure PostgreSQL is running and the database `astra` exists at `localhost:5432`. Update the `DATABASE_URL` in your `.env` file with your PostgreSQL username.

## (Optional) Importing a Database Dump

If you have a SQL dump in a file `astra_dump.sql`, run:

```bash
psql -d astra -f astra_dump.sql
```

### Migrations

To create a new migration, run:

```bash
alembic revision --autogenerate -m "Add new table"
```

To apply the migration, run:

```bash
alembic upgrade head
```
