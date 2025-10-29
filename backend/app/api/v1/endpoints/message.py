from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter(
    prefix="/api/v1/messages",
    tags=["messages"]
)

@router.get("/", response_model=list[MessageRead])
def get_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取留言列表"""
    messages = db.query(Message).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    return messages

@router.post("/", response_model=MessageRead)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """创建新留言"""
    db_message = Message(
        sender_id=message.sender_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/{message_id}", response_model=MessageRead)
def get_message(message_id: int, db: Session = Depends(get_db)):
    """获取单个留言详情"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="留言不存在")
    return message

@router.put("/{message_id}/read", response_model=MessageRead)
def mark_as_read(message_id: int, db: Session = Depends(get_db)):
    """标记留言为已读（通过直接更新数据库）"""
    update_result = db.query(Message).filter(Message.id == message_id).update({"is_read": True})
    if update_result == 0:
        raise HTTPException(status_code=404, detail="留言不存在")
    db.commit()
    message = db.query(Message).filter(Message.id == message_id).first()
    return message