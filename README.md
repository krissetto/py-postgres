# FastAPI PostgreSQL Demo

A simple FastAPI application that connects to a PostgreSQL database.

## Setup

### Option 1: Using uv (Recommended)

1. Install uv if you don't have it already:
   ```
   pip install uv
   ```

2. Create a virtual environment and install dependencies:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. Configure the database connection:
   - Edit the `.env` file to set your PostgreSQL connection details
   - Default is: `postgresql://postgres:postgres@localhost:5432/postgres`

4. Run the application:
   ```
   uvicorn main:app --reload
   ```

### Option 2: Using pip (Legacy)

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure the database connection:
   - Edit the `.env` file to set your PostgreSQL connection details
   - Default is: `postgresql://postgres:postgres@localhost:5432/postgres`

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

## Access the Application

- Homepage with form: http://localhost:8000/
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- List items: http://localhost:8000/items/
- Create item: POST to http://localhost:8000/items/ with query parameters `name` and `description`

## Requirements

- Python 3.10+
- PostgreSQL database
