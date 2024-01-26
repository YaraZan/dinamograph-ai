import datetime
from typing import Optional, List

from pydantic import BaseModel


class ChatMessageResponse(BaseModel):
    id: int
    created_at: datetime.datetime
    text: Optional[str]
    url: Optional[str]
    is_ai_generated: bool


class ChatResponse(BaseModel):
    public_id: str


class GetUserChatsResponse(BaseModel):
    chats: List[Optional[ChatResponse]]


class GetUserChatMessagesResponse(BaseModel):
    messages: List[Optional[ChatMessageResponse]]


class CreateChatMessageRequest(BaseModel):
    user_public_id: str
    chat_public_id: str
    text: Optional[str]
    is_ai_generated: bool
