import asyncio
import uuid

import aioamqp
from aioamqp.channel import Channel

from .transportabc import TransportABC, ClientTransportABC
from ..webtypes import Request, Response, Methods


class RabbitMQClientTransport(ClientTransportABC):
    def __init__(self, channel):
        self.channel = channel
        self._response_futures = {}
        self.response_queue_name = str(uuid.uuid1()).encode()
        self._consumer_tag = None
        self._starting_future = asyncio.ensure_future(self.start())


    async def make_request(self, service: str, method: str, path: str,
                           body: bytes = None, query: str = None,
                           headers: dict = None, correlation_id: str = None,
                           content_type: str = None,
                           exchange: str = 'amq.topic',
                           **kwargs):

        if not self._starting_future.done:
            await self._starting_future
        path = path.replace('/', '.').lstrip('.')
        if headers is None:
            headers = {}
        if query:
            headers['x-wasp-query-string'] = query

        if not body:
            body = b'None'
        message_id = str(uuid.uuid4())
        properties = {
            'headers': headers,
            'correlation_id': correlation_id,
            'message_id': message_id,
            'type': method,
            'app_id': 'test',
        }
        if method != 'PUBLISH':
            properties['reply_to'] = self.response_queue_name
            properties['expiration']: '30000'

        if content_type:
            properties['content_type'] = content_type

        await self.channel.basic_publish(exchange_name=exchange,
                                         routing_key=path,
                                         properties=properties,
                                         payload=body)

        if method != 'PUBLISH':
            future = asyncio.Future()
            self._response_futures[message_id] = future
            return await future

    async def start(self):
        await self.channel.queue_declare(queue_name=self.response_queue_name,
                                         durable=False,
                                         exclusive=True,
                                         auto_delete=True)
        self._consumer_tag = (await self.channel.basic_consume(
            self.handle_responses,
            queue_name=self.response_queue_name,
            no_ack=True)).get('consumer_tag')

    async def handle_responses(self, channel, body, envelope, properties):
        future = self._response_futures[properties.message_id]

        headers = properties.headers
        status = headers.pop('Status')

        response = Response(headers=headers,
                            correlation_id=properties.correlation_id,
                            body=body,
                            status=status,
                            content_type=properties.content_type)

        future.set_result(response)


class RabbitMQTransport(TransportABC):
    def __init__(self, *, url, port=5672, queue='', virtualhost='/',
                 username='guest', password='guest',
                 ssl=False, verify_ssl=True, create_queue=True,
                 use_acks=False):
        self.host = url
        self.port = port
        self.virtualhost = virtualhost
        self.queue = queue
        self.username = username
        self.password = password
        self.ssl = ssl
        self.verify_ssl = verify_ssl
        self.create_queue = create_queue
        self._use_acks=use_acks
        self._transport = None
        self._protocol = None
        self.channel = None
        self._app = None
        self._loop = None
        self._consumer_tag = None
        self._counter = 0
        self._handler = None
        self._done_future = asyncio.Future()
        self._closing = False

    def get_client(self):
        return RabbitMQClientTransport(self.channel)

    async def declare_exchange(self):
        pass

    async def declare_queue(self):
        pass

    async def bind_to_exchange(self, *, exchange, routing_key):
        await self.channel.queue_bind(exchange_name=exchange,
                                      queue_name=self.queue,
                                      routing_key=routing_key)

    async def start(self, handler):
        self._handler = handler
        # ToDo: Need to reconnect because of potential forking affects
        # await self.close()
        # await self.connect()
        await self.channel.basic_qos(prefetch_count=1)
        self._consumer_tag = (await self.channel.basic_consume(
            self.handle_request,
            queue_name=self.queue,
            no_ack=not self._use_acks)).get('consumer_tag')

        try:
            await self._done_future
        except asyncio.CancelledError:
            pass

        print('shutting down rabbit')
        # shutting down
        await self.channel.basic_cancel(self._consumer_tag)

        while self._counter > 0:
            await asyncio.sleep(1)

    def listen(self, *, loop):
        async def setup():

            await self.connect(loop=loop)
            if self.create_queue:
                await self.channel.queue_declare(queue_name=self.queue)
            await self.channel.basic_qos(prefetch_count=1)

        loop.run_until_complete(setup())
        print('-- Listening for rabbitmq messages on queue {} --'
              .format(self.queue))

    async def _handle_rabbit_error(self, exception):
        print(exception)
        if isinstance(exception, aioamqp.ChannelClosed) and not self._closing:
            await self.connect()

    async def connect(self, loop=None):
        self._transport, self._protocol = await aioamqp.connect(
            host=self.host,
            port=self.port,
            virtualhost=self.virtualhost,
            login=self.username,
            password=self.password,
            ssl=self.ssl,
            verify_ssl=self.verify_ssl,
            heartbeat=20,
            on_error=self._handle_rabbit_error,
            loop=loop
        )
        self.channel = await self._protocol.channel()

    async def close(self):
        self._closing = True
        await self._protocol.close()
        self._transport.close()

    async def handle_request(self, channel: Channel, body, envelope,
                             properties, futurize=True):
        """
        the 'f' param is simply because aioamqp doesnt send another job until
         this method returns (completes), so we ensure the future of
         ourselves and return immediately so we can handle many requests
         at a time.
        """
        if futurize:
            asyncio.ensure_future(
                self.handle_request(channel, body, envelope, properties,
                                    futurize=False))
            return

        self._counter += 1
        route = envelope.routing_key
        headers = properties.headers or {}
        query = headers.pop('x-wasp-query-string', '').lstrip('?')
        headers['content-type'] = properties.content_type
        headers['content-encoding'] = properties.content_encoding
        correlation_id = properties.correlation_id
        message_id = properties.message_id
        reply_to = properties.reply_to
        method = properties.type or 'POST'

        request = Request(
            headers=headers,
            path=route,
            correlation_id=correlation_id,
            method=method,
            query_string=query,
            body=body,
        )

        response = await self._handler(request)
        if reply_to:
            response.headers['Status'] = str(response.status.value)

            payload = response.data or b'None'

            properties = {
                'correlation_id': response.correlation_id,
                'headers': response.headers,
                'content_type': response.content_type,
                'message_id': message_id,
                'expiration': '30000',
            }
            await channel.basic_publish(exchange_name='',
                                        payload=payload,
                                        routing_key=reply_to,
                                        properties=properties)

        if self._use_acks:
            await self.channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
        self._counter -= 1

    def shutdown(self):
        print('Rabbit got shutdown signal')
        self._done_future.cancel()



