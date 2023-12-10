from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.depends import get_db
from app.main import app
from app.test.util import get_access_token

TEST_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/test"
engine = create_engine(TEST_DATABASE_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db: SessionTesting) -> Generator:
    app.dependency_overrides[get_db] = lambda: db  # 테스트 시 app의 get_db를 db로 오버라이드
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def access_token(client: TestClient) -> Dict[str, str]:
    return get_access_token(client)
