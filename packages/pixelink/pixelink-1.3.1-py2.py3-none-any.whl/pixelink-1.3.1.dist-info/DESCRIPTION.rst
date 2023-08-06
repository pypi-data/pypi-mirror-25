PixeLINK
========

A Python driver for the PixeLINK camera.


Compatibility
-------------

Tested and developed with the following environment,

* PixeLINK camera model: PixeLINK GigE PL-B781G
* PixeLINK Software Development Kit 4.2 - Release 8.7.1 (~2014 including the 2017 version)
* Window 7 Pro (32 and 64 bit)
* Python 2.7 (32 and 64 bit) and Python 3.6 (64bit)


Installation
------------

Use Python's pip tool to install this package::

    pip install pixelink

There are several dependencies,

    * decorator (required)
    * numpy (optional)
    * pillow (optional - used to save the images)

For Window's users use the following binary repository to install numpy,

    * http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

Once the Numpy+MKL wheel file is downloaded, then execute the following
command (assuming numpy‑1.13.2+mkl‑cp36‑cp36m‑win_amd64.whl)::

    pip install numpy‑1.13.2+mkl‑cp36‑cp36m‑win_amd64.whl


Examples
--------

Frame grabbing with numpy installed,

.. code-block:: python

    >>> from pixelink import PixeLINK
    >>> cam = PixeLINK()
    >>> cam.shutter = 0.002
    >>> cam.grab()
    array([[17, 18, 17, ..., 18, 16, 17],
           [16, 17, 17, ..., 18, 17, 17],
           [17, 17, 16, ..., 17, 17, 17],
           ...,
           [20, 20, 21, ..., 20, 20, 20],
           [21, 18, 20, ..., 21, 20, 21],
           [22, 21, 20, ..., 20, 21, 20]], dtype=uint8)
    >>> raw_data = cam.grab()
    >>> raw_data.mean()
    21.016006038647344
    >>> cam.shutter = 0.003
    >>> raw_data = cam.grab()
    >>> raw_data.mean()
    29.30297418478261
    >>> cam.close()
    >>>
    >>> from PIL import Image
    >>> im = Image.fromarray(raw_data)
    >>> im.save('test1.png')


Frame grabbing without numpy installed,

.. code-block:: python

    >>> from pixelink import PixeLINK
    >>> from PIL import Image
    >>> cam = PixeLINK()
    >>> cam.shutter = 0.004
    >>> data = cam.grab()
    >>> data
    <ctypes.c_char_Array_6624000 object at 0x00000000039EF448>
    >>> cam.size
    (2208, 3000)
    >>> cam.pixel_size
    1
    >>> im = Image.frombuffer('L', cam.size, data)
    __main__:1: RuntimeWarning: the frombuffer defaults may change in a future release; for portability, change the call to read:
      frombuffer(mode, size, data, 'raw', mode, 0, 1)
    >>> im.save('test2.png')
    >>> cam.close()


Continuous frame grabbing in a thread,

.. code-block:: python

    import threading
    import time

    from pixelink import PixeLINK, PxLerror


    def grab_frames(cam):
        frame_num = 0
        time_start = time.time()
        print('Continuous frame grabbing started...')
        while cam.is_open():
            frame_num += 1
            try:
                data = cam.grab()
                # TODO: do something with the data...
            except PxLerror as exc:
                print('ERROR: grab_frames:', str(exc))
                continue
            t_total = time.time() - time_start
            if frame_num % 10 == 0:
                frame_rate = float(frame_num) / t_total
                print('#%04d FPS: %0.3f frames/sec' % (frame_num, frame_rate))


    def main():
        cam = PixeLINK()
        cam.shutter = 0.002  # exposure time in seconds
        th = threading.Thread(target=grab_frames, args=[cam])
        th.start()
        try:
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            print('Caught CTRL+C')
        finally:
            print('Closing camera...')
            cam.close()
            print('Waiting for thread...')
            th.join()
            print('Done.')

    if __name__ == '__main__':
        main()


Links
-----

* Documentation: https://hsmit.gitlab.io/pixelink/
* Repository: https://gitlab.com/hsmit/pixelink
* PyPi Location: https://pypi.python.org/pypi/pixelink
* PyPi Test Location: https://test.pypi.org/project/pixelink/


