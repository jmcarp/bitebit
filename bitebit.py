import bitalino

import time
import numpy as np
import pylab as plt


MAC_ADDRESS = '98:d3:31:b2:13:12'
CHANNELS = {
    'light': 9,
}

plt.ion()


class Collector(object):
    
    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate
        self.device = None

    def clear_bitalino(self):
        if self.device:
            self.device.close()
            self.device = None
            time.sleep(1)

    def setup_bitalino(self):
        self.clear_bitalino()
        self.device = bitalino.BITalino()
        self.device.open(MAC_ADDRESS, self.sampling_rate)
        time.sleep(1)
        self.device.start(range(6))
    
    def write(self, channel, width, increment, fname):
        self.setup_bitalino()
        with open(fname, 'w') as fp:
            while True:
                t0 = time.time()
                data = self.device.read(increment)[channel, :]
                fp.write('\n'.join([str(x) for x in data]))
                fp.write('\n')
                print(time.time() - t0)

    def collect(self, channel, width, increment, ylim, fname=None):
        fp = open(fname, 'w') if fname else None
        plt.close()
        self.setup_bitalino()
        data = self.device.read(width)[channel, :]
        graph = plt.plot(data)[0]
        plt.ylim(ylim)
        while True:
            t0 = time.time()
            new_data = self.device.read(increment)[channel, :]
            data = np.hstack((data[increment:], new_data))
            graph.set_ydata(data)
            #if fp:
            #    fp.write('\n'.join([str(value) for value in new_data]))
            #    fp.write('\n')
            plt.draw()
            plt.pause(0.0001)
            print(time.time() - t0)


