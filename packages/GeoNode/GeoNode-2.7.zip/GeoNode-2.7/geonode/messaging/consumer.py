import logging
import sys

from geonode.geoserver.signals import geoserver_post_save2
from geonode.security.views import send_email_consumer, send_email_owner_on_view
from geonode.social.signals import notification_post_save_resource2
from geonode.layers.views import layer_view_counter
from kombu.mixins import ConsumerMixin
from django.conf import settings

from queues import queue_email_events, queue_geoserver_events,\
                   queue_notifications_events, queue_all_events,\
                   queue_geoserver_catalog, queue_geoserver_data,\
                   queue_geoserver, queue_layer_viewers

logger = logging.getLogger(__package__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class Consumer(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        return

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(queue_all_events,
                     callbacks=[self.on_message]),
            Consumer(queue_email_events,
                     callbacks=[self.on_email_messages]),
            Consumer(queue_geoserver_events,
                     callbacks=[self.on_geoserver_messages]),
            Consumer(queue_notifications_events,
                     callbacks=[self.on_notifications_messages]),
            Consumer(queue_geoserver_catalog,
                     callbacks=[self.on_geoserver_catalog]),
            Consumer(queue_geoserver_data,
                     callbacks=[self.on_geoserver_data]),
            Consumer(queue_geoserver,
                     callbacks=[self.on_geoserver_all]),
            Consumer(queue_layer_viewers,
                     callbacks=[self.on_layer_viewer]),
        ]

    def on_consume_end(self, connection, channel):
        super(Consumer, self).on_consume_end(connection, channel)
        logger.info("finished.")

    def on_message(self, body, message):
        logger.info("broadcast: RECEIVED MSG - body: %r" % (body,))
        message.ack()
        return

    def on_email_messages(self, body, message):
        logger.info("on_email_messages: RECEIVED MSG - body: %r" % (body,))
        layer_uuid = body.get("layer_uuid")
        user_id = body.get("user_id")
        send_email_consumer(layer_uuid, user_id)
        # Not sure if we need to send ack on this fanout version.
        message.ack()
        logger.info("on_email_messages: finished")
        return

    def on_geoserver_messages(self, body, message):
        logger.info("on_geoserver_messages: RECEIVED MSG - body: %r" % (body,))
        layer_id = body.get("id")
        geoserver_post_save2(layer_id)
        # Not sure if we need to send ack on this fanout version.
        message.ack()
        logger.info("on_geoserver_messages: finished")
        return

    def on_notifications_messages(self, body, message):
        logger.info("on_notifications_message: RECEIVED MSG - body: %r" % (body,))
        instance_id = body.get("id")
        app_label = body.get("app_label")
        model = body.get("model")
        created = body.get("created")
        notification_post_save_resource2(instance_id, app_label, model, created)
        message.ack()
        logger.info("on_notifications_message: finished")
        return

    def on_geoserver_all(self, body, message):
        logger.info("on_geoserver_all: RECEIVED MSG - body: %r" % (body,))
        message.ack()
        logger.info("on_geoserver_all: finished")
        # TODO:Adding consurmer's producers.
        return

    def on_geoserver_catalog(self, body, message):
        logger.info("on_geoserver_catalog: RECEIVED MSG - body: %r" % (body,))
        message.ack()
        logger.info("on_geoserver_catalog: finished")
        return

    def on_geoserver_data(self, body, message):
        logger.info("on_geoserver_data: RECEIVED MSG - body: %r" % (body,))
        message.ack()
        logger.info("on_geoserver_data: finished")
        return

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        logger.info(">>> Ready:")
        logger.info(connection)
        logger.info("{} consumers:".format(len(consumers)))
        for i, consumer in enumerate(consumers, start=1):
            logger.info("{0} {1}".format(i, consumer))

        super(Consumer, self).on_consume_ready(connection, channel, consumers,
                                               **kwargs)

    def on_layer_viewer(self, body, message):
        logger.info("on_layer_viewer: RECEIVED MSG - body: %r" % (body,))
        viewer = body.get("viewer")
        owner_layer = body.get("owner_layer")
        layer_id = body.get("layer_id")
        layer_view_counter(layer_id)
        if settings.EMAIL_ENABLE:
            send_email_owner_on_view(owner_layer, viewer, layer_id)
        message.ack()
        logger.info("on_layer_viewer: finished")

        return
