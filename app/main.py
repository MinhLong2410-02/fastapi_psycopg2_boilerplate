from fastapi import FastAPI, Depends
from app.core.db import get_db_connection, close_connection_pool

app = FastAPI()

# Dependency to get a database connection
def get_db():
    with get_db_connection() as conn:
        yield conn

# Example endpoint using the dependency
@app.get("/items/{item_id}")
def read_item(item_id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
    return {"item": item}

# Close the connection pool on shutdown
@app.on_event("shutdown")
def shutdown():
    close_connection_pool()
