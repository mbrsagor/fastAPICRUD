from src import models
from src.db import schemas
from src.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response

from utils import messages

router = APIRouter()


# Get all note with pagination with filter
@router.get('/')
def get_notes(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    notes = db.query(models.Note).filter(models.Note.title.contains(search)).limit(limit).offset(skip).all()
    resp = {
        'status': True,
        'message': messages.DATA_RENDERED,
        'data': notes
    }
    return resp


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    new_note = models.Note(**payload.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    resp = {
        'status': True,
        'message': messages.DATA_RENDERED
    }
    return resp


# Update note
@router.put('/{noteId}')
def update_note(noteId: str, payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    update_data = payload.dict(exclude_unset=True)
    note_query.filter(models.Note.id == noteId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_note)
    resp = {
        'status': True,
        'message': messages.DATA_UPDATED
    }
    return resp


# Get single note
@router.get('/{noteId}')
def get_post(noteId: str, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == noteId).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    resp = {
        'status': True,
        'message': messages.DATA_RENDERED,
        'data': note
    }
    return resp


@router.delete('/{noteId}')
def delete_post(noteId: str, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
