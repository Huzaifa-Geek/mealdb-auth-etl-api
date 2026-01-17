# mealdb-auth-etl-api

A secure FastAPI backend that performs ETL (Extract, Transform, Load) on data from TheMealDB API, stores it in MySQL, and exposes JWT-protected, role-based APIs.


## Features

- ETL pipeline to ingest meal data from TheMealDB API
- Data transformation with pricing and affordability classification
- JWT-based authentication with Argon2 password hashing
- Role-Based Access Control (RBAC)
-- Admin: View all meals and trigger data synchronization
-- User: View only affordable meals (price < 1500)

  ## Installation

  ```
  pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[argon2] python-dotenv requests
  ```
  ## Run Server
```
uvicorn main:app --reload

```
before running update .env with your MySQL credentials and SECRET_KEY

## Database Schema

**Open MySQL Workbench**
```sql
   CREATE DATABASE your_database_name;
```
Ensure your DB_NAME in the .env file matches the name you just created



