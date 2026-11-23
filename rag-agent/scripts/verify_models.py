
from app.infrastructure.database.base import Base

# Importing models registers them with Base.metadata.
from app.infrastructure.database import models

def verify_models():

    print("Registered database tables:")

    for table_name, table in Base.metadata.tables.items():

        print(f"\nTable: {table_name}")

        for column in table.columns:
            print(
                f"  {column.name}: {column.type}"
                f" | Nullable: {column.nullable}"
                f" | Primary Key: {column.primary_key}"
            )

if __name__ == "__main__":
    verify_models()