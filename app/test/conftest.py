from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.depends import get_db
from app.main import app
from app.test.util import get_access_token

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db: SessionTesting):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def access_token(client: TestClient) -> Dict[str, str]:
    return get_access_token(client)
