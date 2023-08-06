# -*- coding: utf-8 -*-
from chat_api.chat.optimizations import get_thread_optimization_option, UserThreadsPool
from chat_api.chat.signals import chat_api_thread_schema_completed
from chat_api.chat.tasks import finish_processing_message_task
from chat_api.common import AttachmentTypes
from chat_api.schemas.models import Question
from chat_api.settings import chat_settings
from chat_api.utils.fields import JSONField
from chat_api.utils.safe_delete_policy import SafeDeleteMixin
from collections import defaultdict
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from simpleeval import simple_eval
from threading import current_thread
from universal_notifications.signals import ws_received

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class UserThread(models.Model):
    PERMISSION_MESSAGES_READ = 1
    PERMISSION_MESSAGES_CREATE = 2
    PERMISSION_MESSAGES_EDIT = 4
    PERMISSION_MESSAGES_DELETE = 8
    PERMISSION_THREAD_READ = 16
    PERMISSION_THREAD_EDIT = 32
    PERMISSION_THREAD_DELETE = 64
    PERMISSION_THREAD_ADD_USER = 128
    PERMISSION_THREAD_REMOVE_USER = 256
    PERMISSION_THREAD_CONTROL_OTHERS = 512
    PERMISSION_THREAD_BREAK_STATE = 1024
    PERMISSION_THREAD_ROLLBACK = 2048
    PERMISSION_THREAD_REOPEN = 4096

    PERMISSIONS_DEFAULT = chat_settings.THREAD_PERMISSIONS_DEFAULT
    PERMISSIONS_CREATOR_DEFAULT = chat_settings.THREAD_CREATOR_PERMISSIONS_DEFAULT

    NOTIFIACTIONS_UNREAD = 1
    NOTIFICATIONS_WS = 2
    NOTIFICATIONS_PUSH = 4

    NOTIFICATIONS_DEFAULT = NOTIFIACTIONS_UNREAD | NOTIFICATIONS_WS  # FIXME: move to settings

    FREQUENCY_UNIT_HOURS = "hours"
    FREQUENCY_UNIT_DAYS = "days"
    FREQUENCY_UNIT_WEEKS = "weeks"
    FREQUENCY_UNIT_MONTHS = "months"
    FREQUENCY_UNIT_CHOICES = (
        (FREQUENCY_UNIT_HOURS, "Hours"),
        (FREQUENCY_UNIT_DAYS, "Days"),
        (FREQUENCY_UNIT_WEEKS, "Weeks"),
        (FREQUENCY_UNIT_MONTHS, "Months")
    )

    ON_FINISH_OPEN = "open"
    ON_FINISH_CLOSE = "close"
    ON_FINISH_REPEAT = "repeat"
    ON_FINISH_CHOICES = (
        (ON_FINISH_OPEN, "Open"),
        (ON_FINISH_CLOSE, "Close"),
        (ON_FINISH_REPEAT, "Repeat")
    )

    STATE_SCRIPTED = "scripted"
    STATE_SCRIPTED_FE_CONTROLLED = "scripted_fe_controlled"
    STATE_ASSISTED = "assisted"
    STATE_CLOSED = "closed"
    STATE_OPEN = "open"
    STATE_CHOICES = (
        (STATE_SCRIPTED, "Scripted"),
        (STATE_SCRIPTED_FE_CONTROLLED, "Scripted (Front End Controlled)"),
        (STATE_ASSISTED, "Assisted"),
        (STATE_CLOSED, "Closed"),
        (STATE_OPEN, "Open")
    )

    automated_sender = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, db_index=False,
                                         related_name="automated_threads_sent_by", on_delete=models.CASCADE)
    created = models.DateTimeField(db_index=True)
    frequency_unit = models.CharField(max_length=50, choices=FREQUENCY_UNIT_CHOICES, null=True, blank=True)
    frequency_value = models.IntegerField(null=True, blank=True)
    initial_question = models.ForeignKey("chat_api.Question", null=True, blank=True, related_name="states_inited_with",
                                         on_delete=models.CASCADE, db_index=False)
    next_restart = models.DateTimeField(null=True, blank=True, db_index=True)
    notifications = models.IntegerField(default=NOTIFICATIONS_DEFAULT, null=True, blank=True)
    on_finish = models.CharField(max_length=50, choices=ON_FINISH_CHOICES, default="open", blank=True)
    permissions = models.IntegerField(default=PERMISSIONS_DEFAULT, null=True, blank=True)
    question = models.ForeignKey("chat_api.Question", null=True, blank=True, related_name="states_with",
                                 on_delete=models.SET_NULL, db_index=False)
    related_message = models.ForeignKey("chat_api.Message", null=True, blank=True, related_name="states_related_with",
                                        on_delete=models.SET_NULL, db_index=False, editable=False)
    repeat_until = models.DateTimeField(null=True, blank=True)
    schema = models.ForeignKey("chat_api.Schema", null=True, blank=True, on_delete=models.CASCADE, db_index=False)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default=STATE_OPEN)
    thread = models.ForeignKey("chat_api.Thread", on_delete=models.CASCADE, related_name="users")
    type = models.CharField(max_length=50, choices=chat_settings.TYPES_CHAT, db_index=True, editable=False)
    updated = models.DateTimeField(db_index=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_message = models.ForeignKey("chat_api.Message", null=True, blank=True, db_index=False,
                                     on_delete=models.SET_NULL, related_name="last_in_user_threads")
    variables_pool = JSONField(blank=True, default=dict)

    class Meta:
        unique_together = (("user", "thread"), )
        app_label = "chat_api"

    def __init__(self, *args, **kwargs):
        super(UserThread, self).__init__(*args, **kwargs)
        self._old_question_id = self.question_id

    @property
    def title(self):
        return self.thread.title

    def recalculate_variables_pool(self):
        self.variables_pool = {}
        modifications = list(self.variable_modifications.exclude(related_message__deleted=True).order_by("id"))
        message_answer_pks = {mod.related_message_answer_id for mod in modifications if mod.related_message_answer_id}
        existing_answers_through = set()
        if message_answer_pks:
            existing_answers_through = set(
                Message.answers.through.objects.filter(
                    pk__in=message_answer_pks, message__deleted=False, message__thread_id=self.thread_id,
                ).values_list("id", flat=True)
            )

        for mod in modifications:
            if mod.related_message_answer_id and mod.related_message_answer_id not in existing_answers_through:
                mod.delete()
                continue

            for symbol, expression in mod.variable_modifications:
                if self.variables_pool:
                    current_values = defaultdict(float, self.variables_pool)
                else:
                    # Workaround for strange behaviour of simpleeval - it accepts defaultdict w/o problems,
                    # as long as there is at least one element inside. Otherwise it throws an error.
                    current_values = defaultdict(float, {"_______________": 0})
                self.variables_pool[symbol] = simple_eval(expression, names=current_values)
        self.__class__.objects.filter(pk=self.pk).update(variables_pool=self.variables_pool)

    def move_to_qid(self, next_qid):
        assert self.state in (self.STATE_SCRIPTED, self.STATE_SCRIPTED_FE_CONTROLLED)  # sanity check
        completed = False

        if next_qid < 0:  # end
            if self.on_finish == self.ON_FINISH_REPEAT:
                self.question = self.initial_question
            else:
                self.question = None
                self.related_message = None
                if self.on_finish == self.ON_FINISH_CLOSE:
                    self.state = self.STATE_CLOSED
                elif self.on_finish == self.ON_FINISH_OPEN:
                    self.state = self.STATE_OPEN
                else:
                    raise NotImplementedError
                completed = True
        else:
            question = Question.objects.get(schema_id=self.schema_id, qid=next_qid)
            if question.type == Question.TYPE_FORK:
                self.move_to_qid(question.get_fork_for_variables(self.variables_pool))
                return
            self.question = question
        self.save()

        if self.question_id and self.question.type == Question.TYPE_MESSAGE:
            self.move_to_qid(self.question.next_qid)

        if completed:
            chat_api_thread_schema_completed.send(sender=self.__class__, user_thread=self)


class Thread(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_message = models.ForeignKey("chat_api.Message", null=True, blank=True, db_index=False,
                                     on_delete=models.SET_NULL, related_name="last_in_threads")
    title = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=chat_settings.TYPES_CHAT, default=chat_settings.TYPES_CHAT_DEFAULT)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Thread: %d" % self.id

    class Meta:
        app_label = "chat_api"


class Attachment(models.Model):
    description = models.TextField(blank=True)
    message = models.ForeignKey("chat_api.Message", on_delete=models.CASCADE, related_name="attachments")
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey("contenttypes.ContentType", null=True, db_index=False, on_delete=models.CASCADE)
    options = JSONField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    thumbnail_image = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    thumbnail = JSONField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=AttachmentTypes.TYPE_CHOICES)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        app_label = "chat_api"


class Message(SafeDeleteMixin):
    answers = models.ManyToManyField("chat_api.Answer", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    has_attachments = models.BooleanField(default=False)  # OPTIMIZATION FIXME: deprecated
    meta = JSONField(null=True, blank=True)
    related_question = models.ForeignKey("chat_api.Question", null=True, blank=True, on_delete=models.CASCADE)
    predecessor = models.ForeignKey("chat_api.Question", null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="preceeding_messages")
    sender = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, db_index=False)
    text = models.TextField(blank=True)
    thread = models.ForeignKey("chat_api.Thread", on_delete=models.CASCADE, related_name="messages")
    type = models.CharField(max_length=50, default="message", db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    @classmethod
    def create_with_attachments(cls, **kwargs):
        attachments = kwargs.pop("attachments", None)
        message = cls(**kwargs)
        message._suppress_ws = True  # to avoid sending signal twice
        message.save()  # we need id for attachments
        message.has_attachments = bool(attachments)
        for attachment in attachments:
            attachment.message_id = message.pk
        Attachment.objects.bulk_create(attachments)
        message._suppress_ws = False  # now the signal will be send
        message.save()

        return message

    @classmethod
    def create_from_question(cls, user_thread, question, predecessor_id):
        message = Message.objects.create(
            meta=question.meta, related_question_id=question.pk, text=question.text, predecessor_id=predecessor_id,
            thread=user_thread.thread, type=question.show_as_type, sender_id=user_thread.automated_sender_id
        )
        if question.variable_modifications:
            VariableModification.objects.create(
                related_message=message, user_thread=user_thread, variable_modifications=question.variable_modifications
            )
        return message

    class Meta:
        app_label = "chat_api"


class UnreadMessage(models.Model):
    message = models.ForeignKey("chat_api.Message", related_name="unread_states", on_delete=models.CASCADE)
    thread = models.ForeignKey("chat_api.Thread", related_name="unread_messages", on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=chat_settings.TYPES_CHAT, default=chat_settings.TYPES_CHAT_DEFAULT,
                            blank=True, db_index=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name="unread_messages", on_delete=models.CASCADE)

    class Meta:
        app_label = "chat_api"


class ThreadWSSubscription(models.Model):
    thread = models.ForeignKey("chat_api.Thread", related_name="ws_subscription", on_delete=models.CASCADE)
    user = models.OneToOneField(AUTH_USER_MODEL, related_name="ws_subscription", on_delete=models.CASCADE)


class VariableModification(models.Model):
    variable_modifications = JSONField(blank=True, default=list)
    user_thread = models.ForeignKey(UserThread, related_name="variable_modifications", on_delete=models.CASCADE)
    related_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    related_message_answer_id = models.IntegerField(null=True, blank=True)


# signals
def user_thread_pre_save(sender, instance, **kwargs):
    if not instance.created:
        instance.created = instance.thread.created
    if not instance.updated:
        instance.updated = instance.thread.updated
    if not instance.type:
        instance.type = instance.thread.type
    if not instance.id and not instance.last_message_id:
        if chat_settings.CHAT_MESSAGE_FILTER_QUERYSET:
            instance.last_message = chat_settings.CHAT_MESSAGE_FILTER_QUERYSET(
                Message.objects.filter(thread_id=instance.thread_id), instance.user
            ).order_by("-id").first()
        else:
            instance.last_message_id = instance.thread.last_message_id
    if not instance.id and instance.schema_id and not instance.question_id:
        instance.question = Question.objects.filter(schema__id=instance.schema_id).order_by("position").first()


def user_thread_post_save(sender, instance, created, **kwargs):
    if instance.state == UserThread.STATE_SCRIPTED:
        if instance.question_id != instance._old_question_id and instance.question_id is not None:
            # Related question_id - points to the previous question. Answer will point to the current question.
            message = Message.create_from_question(instance, instance.question, instance._old_question_id)
            UserThread.objects.filter(pk=instance.pk).update(related_message=message)


def send_message_ws(instance, member_ids, user_threads, user_threads_to_send_ws_to, thread):
    from chat_api.chat.notifications import MessageUpdatedWS

    # OPTIMIZATION FIXME: temporary workaround for incorrect number of unread messages due to bulk create
    limit_fields_to = get_thread_optimization_option(thread.type, "LIMIT_FIELDS_TO")
    if user_threads_to_send_ws_to:
        for user_thread in user_threads_to_send_ws_to:
            instance.user_thread = user_thread
            instance.user_thread.last_message = instance  # otherwise this WS would not be sent
            if (not chat_settings.CHAT_MESSAGE_USER_FILTER or
                    chat_settings.CHAT_MESSAGE_USER_FILTER(instance, user_thread.user)):
                if limit_fields_to:
                    MessageUpdatedWS(instance, [user_thread.user], {"fields": limit_fields_to}).send()
                else:
                    MessageUpdatedWS(instance, [user_thread.user], {}).send()

    if not getattr(instance, "_suppress_ws", False):
        if not get_thread_optimization_option(thread.type, "NO_WS_TO_SUBSCRIBED"):
            ws_subscriptions = ThreadWSSubscription.objects.select_related("user").filter(thread_id=instance.thread_id)
            ws_subscriptions = list(ws_subscriptions.exclude(user_id__in=member_ids))
            if ws_subscriptions:
                for ws_subscription in ws_subscriptions:
                    if (not chat_settings.CHAT_MESSAGE_USER_FILTER or
                            chat_settings.CHAT_MESSAGE_USER_FILTER(instance, ws_subscription.user)):
                        instance.user_thread = UserThread(
                            user=ws_subscription.user, thread_id=instance.thread_id, created=thread.created,
                            updated=instance.updated, notifications=0, state=UserThread.STATE_CLOSED,
                            permissions=UserThread.PERMISSION_MESSAGES_READ | UserThread.PERMISSION_THREAD_READ,
                            last_message=instance
                        )
                        if limit_fields_to:
                            MessageUpdatedWS(instance, [ws_subscription.user], {"fields": limit_fields_to}).send()
                        else:
                            MessageUpdatedWS(instance, [ws_subscription.user], {}).send()


def get_threads(message):
    user_threads = None
    if hasattr(current_thread, "request"):
        user_threads_pool = UserThreadsPool.get_user_threads_pool(current_thread.request, message.thread_id)
        if user_threads_pool:
            user_threads = list(user_threads_pool.values())
    if not user_threads:
        user_threads = list(UserThread.objects.filter(thread_id=message.thread_id).select_related("user", "thread"))

    if user_threads:
        thread = user_threads[0].thread
    else:
        thread = message.thread

    return thread, user_threads


def message_post_save(sender, instance, created, **kwargs):
    thread, user_threads = get_threads(instance)
    skip_thread_update = get_thread_optimization_option(thread.type, "NO_UPDATES_FOR_LAST_MESSAGE_AND_UPDATED")

    # adding unread message + sending WS + updating user specific last message
    member_ids = []
    user_threads_ids_to_update_last_message = []
    user_threads_ids_to_not_update_last_message = []
    unread_objects_to_create = []
    user_tracking_unread_ids = []
    user_threads_to_send_ws_to = []

    for user_thread in user_threads:
        if (not chat_settings.CHAT_MESSAGE_USER_FILTER or
                chat_settings.CHAT_MESSAGE_USER_FILTER(instance, user_thread.user)):

            user_threads_ids_to_update_last_message.append(user_thread.pk)
            user_thread.last_message = instance

            if (created and user_thread.notifications & UserThread.NOTIFIACTIONS_UNREAD and
                    instance.sender_id != user_thread.user_id):
                unread_objects_to_create.append(UnreadMessage(
                    message=instance, thread_id=instance.thread_id, type=user_thread.thread.type, user=user_thread.user
                ))
                user_tracking_unread_ids.append(user_thread.user_id)

            if user_thread.notifications & UserThread.NOTIFICATIONS_WS and not getattr(instance, "_suppress_ws", False):
                user_threads_to_send_ws_to.append(user_thread)
        else:
            user_threads_ids_to_not_update_last_message.append(user_thread.pk)

        member_ids.append(user_thread.user_id)

    if not skip_thread_update:
        # FIXME: content of this if is prone to Deadlocks.
        # Just try to send a bunch of messages via swagger to one thread as one user.
        # solution: larger optimisation, as UserThread is always returned with Message to the user
        # and move it to celery task afterwards.
        # check https://github.com/mozilla/django-post-request-task as possible taks hadler.
        UserThread.objects.filter(thread_id=instance.thread_id).update()

        if user_threads_ids_to_update_last_message:
            UserThread.objects.filter(id__in=user_threads_ids_to_update_last_message).update(
                last_message=instance, updated=instance.updated
            )
        if user_threads_ids_to_not_update_last_message:
            UserThread.objects.filter(id__in=user_threads_ids_to_not_update_last_message).update(
                updated=instance.updated
            )

    if hasattr(current_thread, "request"):
        UserThreadsPool.initialize_unread_states(
            current_thread.request, instance.thread_id, unread_objects_to_create, user_tracking_unread_ids
        )

    if unread_objects_to_create:
        UnreadMessage.objects.bulk_create(unread_objects_to_create)

    # sending WS to subscribed
    # move to task after requests, using: https://github.com/mozilla/django-post-request-task as possible taks handler.
    send_message_ws(instance, member_ids, user_threads, user_threads_to_send_ws_to, thread)

    # there also is a way to listen to post_request/commit hook.
    # https://github.com/mozilla/django-post-request-task
    finish_processing_message_task.apply_async([instance.id], countdown=10)  # 10s is long but it's to finish all ops


def variables_modification_post_save(sender, instance, created, **kwargs):
    if created:
        instance.user_thread.recalculate_variables_pool()


def attachment_post_save(sender, instance, created, **kwargs):
    if created:
        Message.objects.filter(pk=instance.message_id).update(has_attachments=True)
    message_post_save(None, instance.message, False)  # send WS after attachment was created/edited


def attachment_post_delete(sender, instance, **kwargs):
    Message.objects.filter(pk=instance.message_id).update(
        has_attachments=bool(Attachment.objects.filter(message_id=instance.message_id).exists())
    )
    message_post_save(None, instance.message, False)  # send WS after attachment was deleted


def ws_handler_mark_message_as_read(sender, message_data, channel_emails, **kwargs):
    command = message_data.get("message", "")
    message_id = message_data.get("data", {}).get("message")
    if command == "mark_message_as_read" and len(channel_emails) == 1 and message_id:
        UnreadMessage.objects.filter(message_id=message_id, user__email=channel_emails[0]).delete()


def ws_handler_dots(sender, message_data, channel_emails, **kwargs):
    command = message_data.get("message", "")
    data = message_data.get("data", {})
    thread_id = data.get("thread")
    length = data.get("length")
    if command == "thread_someone_is_writing" and len(channel_emails) == 1 and thread_id and length:
        from chat_api.chat.notifications import DotsWS

        user_threads = UserThread.objects.filter(thread_id=thread_id).select_related("user")
        receivers = []
        sender = None
        for user_thread in user_threads:
            if user_thread.user.email == channel_emails[0]:
                sender = user_thread.user
                continue

            if user_thread.notifications & UserThread.NOTIFICATIONS_WS:
                receivers.append(user_thread.user)

        ws_subscriptions = ThreadWSSubscription.objects.select_related("user").filter(thread_id=thread_id)
        ws_subscriptions = ws_subscriptions.exclude(user__in=receivers)
        for ws_subscription in ws_subscriptions:
            receivers.append(ws_subscription.user)

        if sender:  # must be a thread member to send dots
            DotsWS({"thread": thread_id, "length": length, "sender_data": sender}, receivers, {}).send()


pre_save.connect(user_thread_pre_save, sender=UserThread)
post_save.connect(user_thread_post_save, sender=UserThread)
post_save.connect(message_post_save, sender=Message)
post_save.connect(attachment_post_save, sender=Attachment)
post_delete.connect(attachment_post_delete, sender=Attachment)
post_save.connect(variables_modification_post_save, sender=VariableModification)
ws_received.connect(ws_handler_mark_message_as_read)
ws_received.connect(ws_handler_dots)
