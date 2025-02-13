from sqlmodel import SQLModel, Field, create_engine
from enum import Enum

class Banks(Enum):
    ACTIVOBANK = "ActivoBank"
    SANTANDER = "Santander"
    MILLENIUM = "Millenium"

class Status(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    BLOCKED = "Blocked"
    PENDING = "Pending"

class Account(SQLModel, table=True):
    id: int = Field(primary_key=True)
    value: float
    bank: Banks = Field(default=Banks.ACTIVOBANK)
    status : Status = Field(default=Status.ACTIVE)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)