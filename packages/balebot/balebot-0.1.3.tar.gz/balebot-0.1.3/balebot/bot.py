import functools

from balebot.models.base_models import response
from balebot.connection.network import Network
from balebot.bale_future import BaleFuture
from balebot.models.client_requests import *

from balebot.models.base_models import BotQuotedMessage, FatSeqUpdate, GroupPeer, Request, UserPeer
from balebot.models.constants.request_to_response_mapper import RequestToResponseMapper
from balebot.models.constants.service_type import ServiceType
from balebot.models.messages import BaseMessage, TextMessage


class Bot:
    def __init__(self, loop, network, bale_futures, timeout):
        self._loop = loop
        if isinstance(network, Network):
            self._network = network

        self._network = network
        self._bale_futures = bale_futures
        self.timeout = timeout

    def set_future(self, request_id, request_body, success_callback=None, failure_callback=None, **kwargs):
        response_body_module, response_body_class = RequestToResponseMapper.get_response(request_body)
        bale_future = BaleFuture(request_id, response_body_module, response_body_class,
                                 success_callback, failure_callback, **kwargs)
        self._bale_futures.append(bale_future)

        self._loop.call_later(self.timeout, functools.partial(self.timeout_future, bale_future))

    def timeout_future(self, bale_future):
        if bale_future in self._bale_futures:
            bot_timeout_json = {"body": {"tag": "CLIENT_REQUEST_TIMEOUT"}}
            error_response = response.Response(bot_timeout_json)
            bale_future.reject(error_response)
            self._bale_futures.remove(bale_future)

    def send_request(self, json_request):
        self._network.send(json_request)

    def reply(self, update, message, success_callback=None, failure_callback=None, **kwargs):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            message_id = update.body.random_id
            user_peer = update.get_effective_user()
            if isinstance(message, BaseMessage):
                self.send_message(message, user_peer,
                                  BotQuotedMessage(message_id, user_peer),
                                  success_callback=success_callback,
                                  failure_callback=failure_callback,
                                  **kwargs)
            else:
                self.send_message(TextMessage(message), user_peer,
                                  BotQuotedMessage(message_id, user_peer),
                                  success_callback=success_callback,
                                  failure_callback=failure_callback,
                                  **kwargs)

    def respond(self, update, message, success_callback=None, failure_callback=None, **kwargs):
        user_peer = update.get_effective_user()
        if isinstance(message, BaseMessage):
            self.send_message(message, user_peer,
                              success_callback=success_callback,
                              failure_callback=failure_callback,
                              **kwargs)
        else:
            self.send_message(TextMessage(message), user_peer,
                              success_callback=success_callback,
                              failure_callback=failure_callback,
                              **kwargs)

    # messaging
    def send_message(self, message, peer, quoted_message=None, random_id=None, success_callback=None,
                     failure_callback=None, **kwargs):
        receiver = peer
        request_body = SendMessage(message=message, receiver_peer=receiver,
                                   quoted_message=quoted_message, random_id=random_id)
        request = Request(service=ServiceType.Messaging, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # group
    def create_group(self, title, success_callback=None, failure_callback=None, **kwargs):
        request_body = CreateGroup(title)
        request = Request(service=ServiceType.Groups, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def get_group_api_struct(self, group_id, client_user_id, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetGroupApiStruct(group_id=group_id, client_user_id=client_user_id)
        request = Request(service=ServiceType.Groups, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def invite_user(self, group_peer_id, group_peer_access_hash, user_peer_id,
                    user_peer_access_hash, success_callback=None, failure_callback=None, **kwargs):
        group_peer = GroupPeer(peer_id=group_peer_id, access_hash=group_peer_access_hash)
        user_peer = UserPeer(peer_id=user_peer_id, access_hash=user_peer_access_hash)
        request_body = InviteUser(group_peer=group_peer, user_peer=user_peer)
        request = Request(service=ServiceType.Groups, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # webhooks
    def get_webhooks(self, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetWebhooks()
        request = Request(service=ServiceType.WebHooks, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def register_webhook(self, name, success_callback=None, failure_callback=None, **kwargs):
        request_body = RegisterWebhook(name=name)
        request = Request(service=ServiceType.WebHooks, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # sequence-update
    def get_difference(self, seq, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetDifference(seq=seq)
        request = Request(service=ServiceType.SequenceUpdate, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request
