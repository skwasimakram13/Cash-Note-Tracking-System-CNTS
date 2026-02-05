print("Starting sqlalchemy debug...")
try:
    from sqlalchemy.orm import Session
    print("SQLAlchemy Session imported successfully.")
except Exception as e:
    print(f"SQLAlchemy import failed: {e}")
except OSError as e:
    print(f"SQLAlchemy DLL error: {e}")

try:
    import greenlet
    print("Greenlet imported successfully.")
except Exception as e:
    print(f"Greenlet import failed: {e}")
