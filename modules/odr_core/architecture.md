# ODR Core Module Architecture

## 1. Directory Structure

```bash
opendatarepository_fw/
├── modules/
│   └── odr_core/
│       ├── init.py
│       ├── models/
│       │   ├── init.py
│       │   ├── user.py
│       │   ├── team.py
│       │   └── content.py
│       ├── schemas/
│       │   ├── init.py
│       │   ├── user.py
│       │   ├── team.py
│       │   └── content.py
│       ├── crud/
│       │   ├── init.py
│       │   ├── user.py
│       │   └── team.py
│       ├── database.py
│       ├── config.py
│       └── alembic/
│           ├── versions/
│           ├── env.py
│           └── alembic.ini
│       └── tests/
│           ├── __init__.py
│           ├── test_db_manager.py
│           ├── test_database.py
│           ├── test_config.py
│           ├── test_user_model.py
│           ├── test_user_crud.py
│           ├── test_user_api.py
│           ├── test_team_model.py
│           ├── test_team_crud.py
│           ├── test_team_api.py
│           └── test_content_model.py
├── server/
│   ├── pyproject.toml
│   ├── tests
│   ├── Taskfile.yml
│   ├── pyproject.toml
│   ├── server/
│   │   ├── api/
│       └── main.py
│           ├── __init__.py
│           └── endpoints/
│               ├── user.py
│               ├── team.py
│               ├── content.py
│               ├── annotation.py
│               └── embedding.py
│           └── dependencies.py

```

## 2. Key Components

### 2.1 odr_core/models/

- Contains SQLAlchemy ORM models for each entity (User, Team, Content)
- Defines table structures and relationships

### 2.2 odr_core/schemas/

- Contains Pydantic models for data validation and serialization
- Defines the structure of request/response data

### 2.3 odr_core/crud/

- Contains CRUD operations for each entity
- Implements business logic for data manipulation

### 2.4 odr_core/database.py

- Sets up database connection
- Provides session management

### 2.5 odr_core/config.py

- Manages configuration settings for the core module
- Includes settings for both production and test databases

### 2.6 odr_core/alembic/

- Contains Alembic migration scripts and configuration

## 3. Integration with FastAPI Server

### 3.1 server/main.py

- Sets up the FastAPI application
- Includes routers from api/endpoints

### 3.2 server/api/endpoints/

- Defines API routes for each entity
- Uses odr_core components (models, schemas, crud) to handle requests

## 4. Testing

### 4.1 tests/test_db_manager.py

- Manages test database setup, teardown, and migrations
- Provides utilities for test database sessions

### 4.2 Individual test files

- Test database connection, configuration, models, CRUD operations, and API endpoints
- Use TestDBManager for consistent test database management

## 5. Key Interactions

1. **Database Interactions**:
   - FastAPI endpoints use CRUD functions from `odr_core.crud`
   - CRUD functions use SQLAlchemy models from `odr_core.models`
   - Database sessions are managed through `odr_core.database`

2. **Data Validation**:
   - API requests and responses are validated using Pydantic models from `odr_core.schemas`

3. **Business Logic**:
   - Core business logic is implemented in `odr_core.crud` functions
   - Additional logic can be added in API endpoints as needed

4. **Database Migrations**:
   - Managed through Alembic in `odr_core.alembic`
   - New migrations can be generated and applied as the schema evolves

5. **Testing**:
   - TestDBManager ensures consistent test database setup and teardown
   - Each test file focuses on specific components (models, CRUD, API)

## 6. Usage in FastAPI Server

Example of a FastAPI endpoint using odr_core components:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from odr_core import crud, schemas
from odr_core.database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.user.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

7. Basic thoughts on this architecture

Separation of Concerns: Core data model and business logic are separated from the API layer.
Reusability: odr_core can be used in different parts of the project or even in other projects.
Maintainability: Centralized management of data models and migrations.
Scalability: Easy to add new entities or extend existing ones.
Testability: Core components can be easily unit tested independently of the API.
Consistency: TestDBManager ensures consistent database state across all tests.
