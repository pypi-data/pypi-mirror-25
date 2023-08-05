from balebot.models.base_models.request_body import RequestBody


class RequestToResponseMapper:
    request_response_map = {

        "CreateGroup": ("balebot.models.server_responses.group.response_create_group", "ResponseCreateGroup"),
        "GetGroupApiStruct": ("balebot.models.server_responses.group.get_group_api_response", "GetGroupApiResponse"),
        "InviteUser": ("balebot.models.server_responses.bot_success_response", "BotSuccess"),

        "DeleteValue": ("balebot.models.server_responses.bot_success_response", "BotSuccess"),
        "GetKeys": ("balebot.models.server_responses.key_value.get_keys", "GetKeys"),
        "GetValue": ("balebot.models.server_responses.key_value.get_value", "GetValue"),
        "SetValue": ("balebot.models.server_responses.bot_success_response", "BotSuccess"),

        "SendMessage": ("balebot.models.server_responses.messaging.message_sent", "MessageSent"),

        "GetDifference": ("balebot.models.server_responses.sequence.difference_update", "DifferenceUpdate"),

        "GetWebhooks": ("balebot.models.server_responses.webhooks.get_webhooks", "GetWebhooks"),
        "RegisterWebhook": ("balebot.models.server_responses.webhooks.register_webhook", "RegisterWebhook"),

    }

    @classmethod
    def get_response(cls, request):
        if isinstance(request, RequestBody):
            request_class_name = request.__class__.__name__
            return cls.request_response_map[str(request_class_name)]
        else:
            return cls.request_response_map[str(request)]
