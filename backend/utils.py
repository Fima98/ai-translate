import openai
import logging
import asyncio
import time
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from .config import settings
from . import models, schemas

logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = f'{settings.openai_api_key}'
openai.api_key = OPENAI_API_KEY


async def perform_translation(task_id: int, content: str, languages: List[str], db: Session):
    logging.info(f"Starting translation for task {task_id}")
    translations = {}

    def translate_with_retry(language: str, retries: int = 3):
        for attempt in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a translator."},
                        {"role": "user", "content": f"Translate the following text into {language}:\n\n{content}"}
                    ],
                )
                return response.choices[0].message["content"].strip()
            except openai.error.RateLimitError:
                logging.warning(
                    f"Rate limit exceeded while translating to {language}, retrying...")
                time.sleep(5)
            except openai.error.OpenAIError as e:
                logging.error(
                    f"OpenAI API error while translating to {language}: {e}")
                break
            except Exception as e:
                logging.error(
                    f"Unexpected error while translating to {language}: {e}")
                break
        return "Translation failed"

    for language in languages:
        logging.info(f"Translating to {language}...")
        translations[language] = await asyncio.to_thread(translate_with_retry, language)

    await update_translation_task(db, task_id, {"status": "completed", "translations": translations})
    logging.info(f"Translation for task {task_id} completed")


async def update_translation_task(db: Session, task_id: int, updates: dict) -> models.TranslationTask:
    task = db.query(models.TranslationTask).filter(
        models.TranslationTask.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation task with id {task_id} not found"
        )

    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
