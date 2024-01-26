from typing import Optional, List

from fastapi import HTTPException, status, UploadFile, File

from database.database import MainSession
from database.models.chat import Chat
from database.models.message import Message
from schemas.chat import CreateChatMessageRequest, ChatMessageResponse, ChatResponse, GetUserChatMessagesResponse
from service.meta.chat_service_meta import ChatServiceMeta

# Create main database instances
main_database = MainSession()


class ChatService(ChatServiceMeta):
    def get_user_chats(self, user_public_id: str) -> List[Optional[ChatResponse]]:
        matching_chats = main_database.query(Chat).filter(Chat.author.public_id == user_public_id).all()

        user_chats = []

        for chat in matching_chats:
            user_chats.append(ChatResponse(
                public_id=chat.public_id,
            ))

        return matching_chats

    def get_user_chat_detail(self, chat_public_id: str) -> GetUserChatMessagesResponse:
        matching_chat = main_database.query(Chat).filter(Chat.public_id == chat_public_id).first()

        if matching_chat is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")

        messages = []

        for message in matching_chat.messages:
            messages.append(ChatMessageResponse(
                id=message.id,
                text=message.text,
                url=message.url,
                is_ai_generated=message.is_ai_generated
            ))

        messages_response = GetUserChatMessagesResponse(
            messages=messages
        )

        return messages_response

    def create_chat_message(
            self,
            message_data: CreateChatMessageRequest,
            image: Optional[UploadFile] = File(None),
    ):
        matching_chat = main_database.query(Chat).filter(Chat.author.public_id == message_data.chat_public_id).first()

        if matching_chat is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")

        new_message = Message(
            user_id=message_data.user_public_id,
            chat_id=matching_chat.id
        )