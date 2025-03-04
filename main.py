from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="FastAPI PostgreSQL Demo")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a simple model
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).all()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI PostgreSQL Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            form {{ background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            label {{ display: block; margin-bottom: 5px; }}
            input, textarea {{ width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px; }}
            button {{ background: #4CAF50; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }}
            button:hover {{ background: #45a049; }}
            .item {{ background: white; padding: 15px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .success {{ background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FastAPI PostgreSQL Demo</h1>
            
            <form action="/items/" method="post">
                <h2>Add New Item</h2>
                <div>
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div>
                    <label for="description">Description:</label>
                    <textarea id="description" name="description" rows="3" required></textarea>
                </div>
                <button type="submit">Add Item</button>
            </form>
            
            <h2>Current Items</h2>
            {''.join(f'<div class="item"><h3>{item.name}</h3><p>{item.description}</p></div>' for item in items)}
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

@app.post("/items/", response_class=HTMLResponse)
async def create_item_form(request: Request, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    
    # Redirect back to the homepage with all items
    items = db.query(Item).all()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI PostgreSQL Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            form {{ background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            label {{ display: block; margin-bottom: 5px; }}
            input, textarea {{ width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px; }}
            button {{ background: #4CAF50; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }}
            button:hover {{ background: #45a049; }}
            .item {{ background: white; padding: 15px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .success {{ background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FastAPI PostgreSQL Demo</h1>
            
            <div class="success">Item "{item.name}" added successfully!</div>
            
            <form action="/items/" method="post">
                <h2>Add New Item</h2>
                <div>
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div>
                    <label for="description">Description:</label>
                    <textarea id="description" name="description" rows="3" required></textarea>
                </div>
                <button type="submit">Add Item</button>
            </form>
            
            <h2>Current Items</h2>
            {''.join(f'<div class="item"><h3>{item.name}</h3><p>{item.description}</p></div>' for item in items)}
        </div>
    </body>
    </html>
    """
    return html_content

# Keep the original API endpoint for programmatic access
@app.post("/api/items/")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query to check DB connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}") 