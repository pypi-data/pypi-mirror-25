from pixelink import PixeLINK

try:
    from esapy_image.image_loader import ImageStreamer
except ImportError:
    ImageStreamer = object


class PxLstreamer(ImageStreamer):

    def __init__(self):
        super(PxLstreamer, self).__init__()
        self._cam = PixeLINK()
        self._cam.roi = [0, 0, 1000, 1000]

    def grab(self):
        with self._mutex:
            if not self._cam:
                self._is_running = False
                return

            raw = self._cam.grab()
            if raw is None:
                return
            self.set_data(raw)

    def stop(self):
        if self._cam:
            with self._mutex:
                self._cam.close()
                del self._cam
                self._cam = None
