from sqlalchemy.orm import declarative_base, mapped_column
from typing_extensions import Annotated

Base = declarative_base()

mapped_int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
