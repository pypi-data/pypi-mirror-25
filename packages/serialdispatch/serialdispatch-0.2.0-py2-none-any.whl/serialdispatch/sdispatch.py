import threading
import time
import copy
import serial
import logging

from serialdispatch.frame import Frame

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SerialDispatch(object):
    """ Sends and receives blocks of data through a byte-aligned interface """
    format_specifiers = {0: 'NONE', 1: 'STRING', 2: 'U8', 3: 'S8', 4: 'U16', 5: 'S16', 6: 'U32', 7: 'S32', 8: 'FLOAT'}

    topical_data = {}
    subscribers = {}

    def __init__(self, port, timeout=0.003, threaded=True):
        """ Initializes frame and threading """
        self.timeout = timeout
        self.port = port

        self.frame = Frame(port, threaded=False)

        self.threaded = threaded
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def close(self):
        self.threaded = False

    def subscribe(self, topic, callback):
        """ Adds a callback method to a topic

        Args:
            topic: a string representing the topic which is being subscribed to
            callback: a function which is to be called when the topic is received
        """
        if topic not in self.subscribers.keys():
            self.subscribers[topic] = [callback]
        else:
            self.subscribers[topic].append(callback)

        logger.debug('subscribers to "{}" updated: {}'.format(topic, self.subscribers[topic]))

    def unsubscribe(self, topic, callback):
        """ Removes the callback from the specified topic

        Args:
            topic: a string representing the topic which is being unsubscribed from
            callback: a function which is being removed from the subscribed topic
        """
        if self.subscribers[topic]:
            self.subscribers[topic].remove(callback)

        if len(self.subscribers[topic]) == 0:
            self.subscribers.pop(topic)

        logger.debug('subscribers to "{}" updated: {}'.format(topic, self.subscribers[topic]))

    def _simplify_data(self, data):
        if isinstance(data, list):
            if len(data[0]) == 1:
                return data[0][0]

            if len(data) == 1:
                return data[0]

        return data

    def _construct_header(self, topic, data, format_specifier):
        header = [e for e in bytearray(topic, 'utf-8')]
        header.append(0)

        if isinstance(data[0][0], str):
            length = len(data[0][0])
            dim = 1

        else:
            length = len(data[0])
            dim = len(data)

        header.append(dim)
        header.append(length & 0x00ff)
        header.append((length & 0xff00) >> 8)

        format_specifiers = {v: k for k, v in self.format_specifiers.items()}
        for i, e in enumerate(format_specifier):
            fs = format_specifiers[e]
            if (i & 1) == 0:
                header.append(fs & 0xf)
            else:
                header[-1] += ((fs & 0xf) << 4)

        return header

    def publish(self, topic, data, format_specifier=None):
        """ Publishes data to a particular topic

        Args:
            topic: the topic to which to publish
            format_specifier: a list of format specifiers
            data: a list of lists, each internal list
                containing a complete set of data
        """
        logger.debug('publishing data to {}'.format(topic))

        # check the 'data' for the simplest formats, convert to the list of lists as appropriate
        if isinstance(data, list):
            if not isinstance(data[0], list):
                data = [data]
        else:
            data = [[data]]

        logger.debug('sending data: {}'.format(data))

        if format_specifier in [None, 'string', 'String', 'STRING']:
            format_specifier = ['STRING']

        if not isinstance(format_specifier, list):
            format_specifier = [format_specifier]

        msg = self._construct_header(topic, data, format_specifier)

        for i, e in enumerate(format_specifier):
            if e == 'NONE' or e == 'STRING':
                msg.extend(bytearray(data[0][0], 'utf-8'))

            elif e == 'U8' or e == 'S8':
                unsigned_data8 = [x if x > 0 else x + 256 for x in data[i]]
                msg.extend(unsigned_data8)

            elif e == 'U16' or e == 'S16':
                unsigned_data16 = [x if x > 0 else x + 65536 for x in data[i]]

                for x in unsigned_data16:
                    msg.append(x & 255)
                    msg.append((x & 65280) >> 8)

            elif e == 'U32' or e == 'S32':
                unsigned_data32 = [x if x > 0 else x + 4294967296 for x in data[i]]

                for x in unsigned_data32:
                    msg.append(x & 255)
                    msg.append((x & 65280) >> 8)
                    msg.append((x & 16711680) >> 16)
                    msg.append((x & 4278190080) >> 24)

            else:
                logger.error('width not supported: {}'.format(e))

        msg_to_send = copy.deepcopy(msg)
        self.frame.push_tx_message(msg_to_send)

        processing_time = self.timeout + (len(msg_to_send) * 8.0/self.port.baudrate)
        time.sleep(processing_time)    # provide a small gap between publishes to allow the uC to process the messages

        return msg

    def run(self):
        """ Monitors received data and properly formats it """
        run_once = True
        while self.threaded or run_once:
            self.frame.run()

            while self.frame.rx_is_available:

                msg = self.frame.pull_rx_message()
                logger.debug('data received: {}'.format(msg))

                # find the first '0' in the msg
                zero_index = 0
                for i, element in enumerate(msg):
                    if element == 0:
                        zero_index = i
                        break

                topic = ''.join(chr(c) for c in msg[0:zero_index])
                msg = msg[zero_index + 1:]
                dim = msg.pop(0)
                length = msg.pop(0)
                length += msg.pop(0) * 256

                # pull off the format specifiers
                format_specifiers = []
                i = 0
                while True:
                    fs0 = msg.pop(0)
                    format_specifiers.append(self.format_specifiers[fs0 & 15])

                    i += 1
                    if i == dim:
                        break

                    format_specifiers.append(self.format_specifiers[(fs0 & 240) >> 4])

                    i += 1
                    if i == dim:
                        break

                for element in format_specifiers:
                    if element == 'STRING':
                        string_message = ''.join(chr(c) for c in msg)
                        self.topical_data[topic] = string_message

                    elif element == 'U8':
                        if not self.topical_data:
                            self.topical_data[topic] = []

                        # pull the next row of U8 from the msg
                        self.topical_data[topic].append(msg[0: length])
                        msg = msg[length:]

                    elif element == 'S8':
                        if not self.topical_data:
                            self.topical_data[topic] = []

                        # pull the next row of U8 from the msg
                        row = msg[0: length]

                        # apply the sign to each row
                        row = [(e - 256) if e > 127 else e for e in row]

                        self.topical_data[topic].append(row)
                        msg = msg[length:]

                    elif element == 'U16':
                        if not self.topical_data:
                            self.topical_data[topic] = []

                        # pull the next row of U16 from the msg
                        row8 = msg[0: length * 2]
                        row16 = []
                        while row8:
                            num16 = row8.pop(0)
                            num16 += row8.pop(0) * 256
                            row16.append(num16)

                        self.topical_data[topic].append(row16)
                        msg = msg[length * 2:]

                    elif element == 'S16':
                        if not self.topical_data:
                            self.topical_data[topic] = []

                        # pull the next row of U16 from the msg
                        row8 = msg[0: length * 2]
                        row16 = []
                        while row8:
                            num16 = row8.pop(0)
                            num16 += row8.pop(0) * 256
                            row16.append(num16)

                        # apply the sign to each row
                        row16 = [(e - 65536) if e > 32767 else e for e in row16]

                        self.topical_data[topic].append(row16)
                        msg = msg[length * 2:]

                    elif element == 'U32':
                        if not self.topical_data:
                            self.topical_data[topic] = []

                        # pull the next row of U16 from the msg
                        row8 = msg[0: length * 4]
                        row32 = []
                        while row8:
                            num32 = row8.pop(0)
                            num32 += row8.pop(0) * 256
                            num32 += row8.pop(0) * 65536
                            num32 += row8.pop(0) * 16777216
                            row32.append(num32)

                        self.topical_data[topic].append(row32)
                        msg = msg[length * 4:]

                    elif element == 'S32':
                        if not self.topical_data:
                            self.topical_data[topic] = []

                        # pull the next row of U16 from the msg
                        row8 = msg[0: length * 4]
                        row32 = []
                        while row8:
                            num32 = row8.pop(0)
                            num32 += row8.pop(0) * 256
                            num32 += row8.pop(0) * 65536
                            num32 += row8.pop(0) * 16777216
                            row32.append(num32)

                        # apply the sign to each row
                        row32 = [(e - 4294967296) if e > 2147483648 else e for e in row32]

                        self.topical_data[topic].append(row32)
                        msg = msg[length * 4:]

                    elif element == 'FLOAT':
                        logger.error('FLOAT not currently supported!')

                    else:
                        logger.error('unrecognized message type: {}'.format(element))

                # remove any data that doesn't have subscribers
                temp_dict = copy.deepcopy(self.topical_data)
                keys = temp_dict.keys()
                for key in keys:
                    if key not in self.subscribers:
                        self.topical_data.pop(key)

                    else:
                        # execute callbacks
                        for callback in self.subscribers[key]:
                            data = self._simplify_data(self.topical_data.get(key))
                            callback(data)

                        ''' at this point, the data should have
                        been consumed by the function and can
                        now be discarded, which helps keep memory
                        use low'''
                        self.topical_data.pop(key)

            if self.timeout:
                time.sleep(self.timeout)

            if not self.threaded:
                run_once = False

''' --------------------------------------------------------------------------
Everything below this line is intended to used in conjunction with the example
Dispatch c file.  It also provides a simple 'getting started' script.
--------------------------------------------------------------------------'''

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # define your serial port or supply it otherwise
    port = serial.Serial("COM12", baudrate=57600, timeout=0.1)

    # create a new instance of PyDispatch
    ps = SerialDispatch(port)

    # create your subscribers
    def array_subscriber():
        # retrieve received data for topic 'bar' and print to screen
        print('data: ', ps.get('bar'))

    def i_subscriber():
        # retrieve received data for topic 'i' and print to screen
        print('i: ', ps.get('i'))

    # use the instance of PyDispatch to associate the subscriber function with the topic
    ps.subscribe('bar', array_subscriber)
    ps.subscribe('i', i_subscriber)

    # publish to topics as desired
    while True:
        ''' publish 'a test message', to subscribers of 'foo', note
            that the message must be in a list of lists '''
        ps.publish('foo', [['a test message']])
        time.sleep(0.2)