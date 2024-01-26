from abc import ABC, abstractmethod
from typing import List, Any, Optional

from schemas.chat import CreateChatMessageRequest, ChatMessageResponse, ChatResponse, GetUserChatMessagesResponse
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse


class ChatServiceMeta(ABC):
    @abstractmethod
    def get_user_chats(self, user_public_id: str) -> List[Optional[ChatResponse]]:
        pass

    @abstractmethod
    def get_user_chat_detail(self, chat_public_id: str) -> GetUserChatMessagesResponse:
        pass

    @abstractmethod
    def create_chat_message(self, message_data: CreateChatMessageRequest):
        pass
