from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas
from utils.export import export_to_csv, export_to_json
from utils.email_service import send_email
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/")
def read_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

# Corrected Update Endpoint
@app.put("/notes/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        return {"error": "Note not found"}
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return {"message": "Note deleted"}

@app.get("/notes/export/{format}")
def export_notes(format: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    if format == "csv":
        export_to_csv(notes)
    elif format == "json":
        export_to_json(notes)
    else:
        return {"error": "Invalid format. Use 'csv' or 'json'."}
    background_tasks.add_task(send_email, "Export Ready", "Your notes are ready.", "user@example.com")
    return {"message": "Export initiated, email will be sent shortly."}

@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note: return {"error": "Note not found"}
    db_note.title = note.title if note.title else db_note.title
    db_note.content = note.content if note.content else db_note.content
    db.commit()
    db.refresh(db_note)
    return db_note