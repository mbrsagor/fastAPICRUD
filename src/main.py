from fastapi import FastAPI, APIRouter, status

app = FastAPI()
router = APIRouter()


@router.get('/')
def get_notes():
    return "return a list of note items"


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_note():
    return "create note item"


@router.patch('/{noteId}')
def update_note(noteId: str):
    return f"update note item with id {noteId}"


@router.get('/{noteId}')
def get_note(noteId: str):
    return f"get note item with id {noteId}"


@router.delete('/{noteId}')
def delete_note(noteId: str):
    return f"delete note item with id {noteId}"


app.include_router(router, tags=['Notes'], prefix='/api/notes')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
