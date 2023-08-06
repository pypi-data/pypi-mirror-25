# -*- coding: utf-8 -*-
from chat_api.chat.serializers import DotsSerializer, MessageWithThreadSerializer
from universal_notifications.notifications import WSNotification


class MessageUpdatedWS(WSNotification):
    message = "message_created_or_updated"
    serializer_class = MessageWithThreadSerializer
    category = "chat"


class DotsWS(WSNotification):
    message = "thread_someone_is_writing"
    serializer_class = DotsSerializer
    category = "chat"
