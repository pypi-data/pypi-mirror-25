import logging

from cloudbrain.connectors.openbci import OpenBCIConnector
from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class OpenBCISource(ModuleInterface):
    def __init__(self, subscribers, publishers, port, baud, filter_data):

        super(OpenBCISource, self).__init__(subscribers, publishers)
        self.connector = OpenBCIConnector(port=port, baud=baud,
                                          filter_data=filter_data)

        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)


    def start(self):

        # Callback functions to handle the sample for that metric.
        # Each metric has a specific number of channels.
        callback_functions = {}

        for publisher in self.publishers:
            metrics_to_num_channels = publisher.metrics_to_num_channels()
            _LOGGER.debug("Metrics to channels mapping: %s"
                          % metrics_to_num_channels)
            for (metric_name, num_channels) in metrics_to_num_channels.items():
                if metric_name not in callback_functions:
                    callback_functions[metric_name] = self.callback_factory(
                        metric_name, num_channels)

        self.connector.start(callback_functions)


    def callback_factory(self, metric_name, num_channels):
        """
        Callback function generator for OpenBCI metrics
        :return: callback function
        """


        def callback(sample):
            """
            Handle OpenBCI samples for that metric
            :param sample: the sample to handle
            """
            message = {}
            for i in range(num_channels):
                channel_value = "%.4f" % (
                    sample.channel_data[i] * 10 ** 9)  # Nano volts
                message["channel_%s" % i] = float(channel_value)
                message['timestamp'] = sample.timestamp

            for publisher in self.publishers:
                _LOGGER.debug("Publishing on metric %s: %s" % (metric_name,
                                                               message))
                publisher.publish(metric_name, message)


        return callback
