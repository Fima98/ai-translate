from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, utils
from ..database import get_db


router = APIRouter(
    prefix='/translate',
    tags=["Translation"]
)


@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def translate_text(
    request: schemas.TranslationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user)
):
    try:
        task = models.TranslationTask(
            content=request.content,
            languages=request.languages,
            status="pending",
            translations={},
            owner_id=get_current_user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        background_tasks.add_task(
            utils.perform_translation, task.id, request.content, request.languages, db)

        return schemas.TaskResponse(task_id=task.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating translation task: {str(e)}"
        )


@router.get("/{task_id}", response_model=schemas.TranslationResponse, status_code=status.HTTP_200_OK)
async def get_translation_task(task_id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(models.TranslationTask).filter(
        models.TranslationTask.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation task with id {task_id} not found"
        )
    if task.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this translation task"
        )
    return schemas.TranslationResponse(
        task_id=task.id, status=task.status, translations=task.translations or {}
    )
