from __future__ import print_function

import argparse
import logging
import threading
import time
import os
from collections import OrderedDict

from astropy.io import fits
import numpy as np

from pixelink import PixeLINK

LOGGER = logging.getLogger(__name__)


class PixelinkApplication(object):
    """ A high level application layer driver for the Pixelink camera. """

    def __init__(self, opts, run_options=True):
        self._opts = opts
        self._dev = PixeLINK()
        self._acquiring = False
        if run_options:
            self.__run_options()

    def close(self):
        self._dev.close()

    def get_header(self, timestamp=None, run_num=1):
        opts = self._opts
        header = OrderedDict()
        if timestamp is None:
            timestamp = time.strftime('%Y%m%d%H%M%S')

        # header.update(dev.get_bias_state(use_labels=True))
        header.update({
            'TIME': timestamp,
            'SENSOR': self._opts.sensor,
            # 'ACQTYPE': acq_type,
            'TITLE': opts.title,
            'FRAME': run_num,
        })
        return header

    def save_fits(self, data, header):
        opts = self._opts
        fits_header = fits.Header()
        for key in header:
            fits_header.update({'hierarch %s' % key: header[key]})

        file_name = os.path.abspath(opts.output.format(**header))
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError:
            pass

        fits.writeto(file_name, data, fits_header)
        LOGGER.info('Saved fits file to: "%s"', file_name)
        return file_name

    def acquire_async(self):
        th = threading.Thread(target=self.acquire)
        th.start()

    def acquire(self, repeat=1):
        """ Grab a frame and save it. """
        try:
            self._acquiring = True
            self._acquire(repeat)
        finally:
            self._acquiring = False
            # event.post('gui', signals.CtrlToGuiEvent.UPDATE_BUTTONS, '*')

    def _acquire(self, repeat=1):
        # opts = self._opts
        dev = self._dev
        timestamp = time.strftime('%Y%m%d%H%M%S')
        for run_idx in range(repeat):
            # exp_time = opts.expose_time
            time_0 = time.time()
            header = self.get_header(timestamp=timestamp, run_num=run_idx+1)

            data = dev.grab()

            LOGGER.info('Acquired %d frames in %0.3f seconds',
                        run_idx+1, time.time()-time_0)

            LOGGER.info('Data mean: %f, std: %f, shape: %s',
                        np.mean(data), np.std(data), np.shape(data))

            fits_file = self.save_fits(data, header)
            logging.info('Saved fits file to:\n%s', fits_file)

            # try:
            #     self._remote_viewer.append_file(fits_file)
            # except IOError:
            #     pass

            # if self._viewer:
            #     self._viewer.view_fits(fits_file, True)

    def __run_options(self):
        opts = self._opts
        dev = self._dev
        if opts.expose_time:
            LOGGER.debug('Setting shutter time to %0.3f seconds', opts.expose_time)
            dev.shutter = opts.expose_time

        if opts.roi:
            LOGGER.debug('Setting region of interest to %s', repr(opts.roi))
            dev.roi = opts.roi

        if opts.acquire:
            self.acquire()


def execute(opts):
    """ Translate the option switches and arguments into method calls on the
    ARC readout controller device.
    """
    dev = PixelinkApplication(opts, run_options=True)
    dev.close()


def main():
    """ main entry point of script """

    settings = {}
    #
    # # check if a configuration file was passed in and use it's default values
    # for key in ['-i', '--ini-file']:
    #     if key in sys.argv:
    #         ini_file = sys.argv[sys.argv.index(key) + 1]
    #
    # # gather all the default settings from the configuration file
    # settings = {}
    # if ini_file:
    #     if ExtendedInterpolation:
    #         cfg = ConfigParser(interpolation=ExtendedInterpolation())
    #     else:
    #         cfg = ConfigParser()
    #     cfg.read(ini_file)
    #     for section in cfg.sections():
    #         for key in cfg[section]:
    #             if section == 'bias':
    #                 settings[section] = settings.get(section, [])
    #                 settings[section].append('%s=%s' % (key.upper(), cfg[section][key]))
    #             else:
    #                 settings[key] = str(cfg[section][key])

    # define the argument parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', default=0, type=int, help='Run the application as a web server')

    parser.add_argument('-i', '--ini-file',
                        help='The .ini configuration file')

    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')

    group = parser.add_argument_group('viewer')
    group.add_argument('--viewer',
                       help='the ds9.exe or esaimage.py file location. '
                            'Leave empty to disable this viewer.')

    group = parser.add_argument_group('acquire')
    group.add_argument('--title', default='testing',
                       help='the measurement label (no spaces)')
    group.add_argument('-s', '--sensor', choices=['N/A', 'PL-B781G'], default='N/A',
                       help='the sensor id')
    group.add_argument('-o', '--output', default='./data/{TIME}.fits',
                       help='the output fits file.')
    group.add_argument('-f', '--frames', default=0, type=int,
                       help='number of frames to readout in a ramp')
    group.add_argument('-r', '--roi', default=None, type=int, nargs='+',
                       help='region of interest')
    group.add_argument('-e', '--expose-time', default=0.0, type=float,
                       help='exposure time in seconds')
    group.add_argument('-x', '--repeat', default=1, type=int,
                       help='number of times to repeat the acquisition')

    group = parser.add_argument_group('actions')
    group.add_argument('-A', '--acquire', action='store_true',
                       help='acquire the frames x ramps images')
    group.add_argument('-D', '--dump', action='store_true',
                       help='dump the state of the camera to the console')
    group.add_argument('-S', '--simulate', action='store_true',
                       help='enable the arc driver simulator')

    # process the arguments
    parser.set_defaults(**settings)
    parser.parse_args()
    opts = parser.parse_args()

    log_level = [logging.ERROR, logging.INFO, logging.DEBUG][min(opts.verbosity, 2)]

    frmt = '%(asctime)s %(levelname)-7s %(name)-20s %(funcName)-20s %(message)s'
    logging.basicConfig(level=log_level, format=frmt)
    if opts.port:
        print('server feature not implemented')
        # try:
        #     run_server(opts)
        # except KeyboardInterrupt:
        #     print('Caught ctr+c')
    else:
        execute(opts)

if __name__ == '__main__':  # pragma: no cover
    main()
