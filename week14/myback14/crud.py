import hashlib
from fastapi import HTTPException
import secrets

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).order_by(models.User.id.asc()).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    m = hashlib.sha256()
    salt = secrets.token_bytes(16).hex()
    m.update(user.password.encode('utf-8'))
    m.update(bytes.fromhex(salt))
    password = m.hexdigest()

    db_user = models.User(username=user.username, salt=salt, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def verify_user(db: Session, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')


    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    m.update(bytes.fromhex(db_user.salt))
    password = m.hexdigest()
    if db_user.password != password:
        raise HTTPException(status_code=404, detail='User authentication failed')

    return db_user

def create_paste(db: Session, username: str, password: str, paste: schemas.PasteCreate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    m.update(bytes.fromhex(db_user.salt))
    password = m.hexdigest()
    if db_user.password != password:
        raise HTTPException(status_code=404, detail='User authentication failed')
    
    db_paste = models.Paste(title=paste.title, content=paste.content, owner=db_user)
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)

    return db_paste

def get_pastes_by_username(db: Session, username: str, skip: int = 0, limit: int = 100):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    
    return db.query(models.Paste).filter(models.Paste.owner_id == db_user.id).\
        order_by(models.Paste.created_at.desc()).offset(skip).limit(limit).all()

def get_pastes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paste).order_by(models.Paste.created_at.desc()).offset(skip).limit(limit).all()
