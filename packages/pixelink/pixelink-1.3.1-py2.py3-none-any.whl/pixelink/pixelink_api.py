#!/usr/bin/env python
#   --------------------------------------------------------------------------
#   Copyright 2014 SRE-F, ESA (European Space Agency)
#       Hans Smit <hsmit@rssd.esa.int>
#
#   Additional enhancements by Danny Smith, The University of Queensland [10-Sep-2017]
#       Danny Smith <danny.smith@uq.edu.au>
#
#   This code is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; version 2 or 3.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#   --------------------------------------------------------------------------
"""
A wrapper around the PixeLINK API exposed in PxlAPi40.dll.
The complete driver implementation is not yet complete, but the core
functionality for adjusting ROI, shutter time, and frame grabbing are in place.
Some additional features have now been exposed [25-Jul-2017].

There are 2 implementations:
    1) PxLapi class: the "core" c-style function calls with either returned error
       codes or thrown exceptions.
    2) PixeLINK class: high level objected-oriented implementation.

There are 2 optional dependencies:
    1) numpy: open source numerical library that has a N-dimensional array object
    2) esapy.iodevice.camera.cvcamera: ESA SRF-F image processing package

If both packages are not available, then the module will degrade "nicely" and
still function properly, but with limited functionality related to image
and data processing.

There are limitations as well:
    1) single channel (uint8) gray scale (no color frame grabbing).
    2) no image processing routines. This can be implemented using scipy.

Update:  Color grabbing works fine.  You can use OpenCV to convert
the image to something more usable [10-Sep-2017]:
    img = cv2.cvtColor(img, cv2.cv.CV_BayerGB2BGR)
or  img = cv2.cvtColor(img, cv2.cv.CV_BayerBG2BGR)

This module was tested using the camera model: PixeLINK GigE PL-B781G.
Reference: http://www.pixelink.com/products/PL-B781-details.aspx

This module was also tested on PixeLINK PL-B623CF and M12C [10-Sep-2017].

"""
from __future__ import print_function

import threading
import ctypes as C

try:
    from decorator import decorator
except ImportError as ex:
    from functools import wraps
    # NOTE: the following decorator function DOES NOT WORK
    # it's only here so that the pixelink setup.py script can
    # build the application.

    def decorator(func):
        if func.__name__ == 'safe_streaming':
            @wraps
            def wrapper(pl, *args, **kwargs):
                return func(pl, *args, **kwargs)
        elif func.__name__ == 'wrap_return_code':
            @wraps
            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)
        else:
            @wraps
            def wrapper(lock, *args, **kwargs):
                return func(lock, *args, **kwargs)
        return wrapper
    print("error: decorator is not installed. Use the following command to install it:")
    print("pip install decorator")

try:
    # try and import numpy, if it is not installed on the user's computer
    # then use raw ctypes string buffers instead.
    import numpy
    HAS_NUMPY = True
except ImportError as ex:
    HAS_NUMPY = False
    print("warning: pixelink.py numpy is not installed. Using raw ctypes buffers instead.")


DEVICE_LOCK = threading.RLock()


def synchronized(lock):
    """ Synchronisation decorator using 'decorator' library.

    :param threading.RLock lock: the
    :return: a caller function into a decorator
    """

    def _synchronized(func, *args, **kwargs):
        """ Caller function that applies the lock

        :param func: function to process
        :arg args: list of arguments used by 'func'
        :key kwargs: dictionary of arguments used by 'func'

        :return: the executed 'func'
        """
        with lock:
            return func(*args, **kwargs)

    return decorator(_synchronized)


@decorator
def safe_streaming(func, pl, *args, **kwargs):
    """
    Temporarily turn off streaming when updating certain
    camera features.
    """
    is_streaming = pl.streaming
    if is_streaming:
        pl.streaming = False
    result = func(pl, *args, **kwargs)
    if is_streaming:
        pl.streaming = True
    return result


@decorator
def wrap_return_code(func, self, *args, **kwargs):
    """
    Decorator that helps convert the PxLapi methods to either return error
    codes or raise exception on error codes.
    """
    result = func(self, *args, **kwargs)
    if self._useReturnCodes:
        return result

    to_return = None  # default to methods returns nothing
    if isinstance(result, (list, tuple)):
        if len(result) > 1:
            to_return = result[1]
        rc = result[0]
    else:
        rc = result

    if rc != 0:
        if len(args) > 0 and isinstance(args[0], C.c_void_p):
            h_camera = args[0]
        else:
            h_camera = None

        # must call unwrapped method, else
        #    'ERROR_REPORT' object is not iterable
        # is thrown. I don't yet understand this.
        (rc, report) = self._GetErrorReport(h_camera)
        exc = PxLerror(self, rc, h_camera, '', report)
        raise exc
    else:
        return to_return


class PxLapi(object):
    """ The PxLapi class is a thin wrapper around the dynamic library (.dll, .so)
    that exposes the PixeLINK API. This uses ctypes to adapt from C to Python.
    """
    # Feature IDs list for future Python driver functionality
    INVALID_FEATURE = None
    NOT_IMPLEMENTED = None

    FEATURE_BRIGHTNESS = 0
    # define FEATURE_PIXELINK_RESERVED_1     1
    FEATURE_SHARPNESS = 2
    FEATURE_COLOR_TEMP = 3
    FEATURE_HUE = 4
    FEATURE_SATURATION = 5
    FEATURE_GAMMA = 6
    FEATURE_SHUTTER = 7
    FEATURE_GAIN = 8
    # define FEATURE_IRIS                    9
    # define FEATURE_FOCUS                   10
    FEATURE_SENSOR_TEMPERATURE = 11
    # define FEATURE_TRIGGER                 12
    # define FEATURE_ZOOM                    13
    # define FEATURE_PAN                     14
    # define FEATURE_TILT                    15
    # define FEATURE_OPT_FILTER              16
    # define FEATURE_GPIO                    17
    FEATURE_FRAME_RATE = 18
    FEATURE_ROI = 19
    FEATURE_FLIP = 20
    FEATURE_PIXEL_ADDRESSING = 21
    FEATURE_PIXEL_FORMAT = 22
    # define FEATURE_EXTENDED_SHUTTER        23
    # define FEATURE_AUTO_ROI                24
    # define FEATURE_LOOKUP_TABLE            25
    FEATURE_MEMORY_CHANNEL = 26
    FEATURE_WHITE_SHADING = 27         # /* Seen in Capture OEM as White Balance */
    FEATURE_ROTATE = 28
    # define FEATURE_IMAGER_CLK_DIVISOR      29          /* DEPRECATED - New applications should not use. */
    # define FEATURE_TRIGGER_WITH_CONTROLLED_LIGHT   30  /* Allows trigger to be used more deterministically where  lighting cannot be controlled.                         */
    FEATURE_MAX_PIXEL_SIZE = 31           # /* The number of bits used to represent 16-bit data (10 or 12) */
    FEATURE_BODY_TEMPERATURE = 32
    # define FEATURE_MAX_PACKET_SIZE         33
    # define FEATURE_BANDWIDTH_LIMIT         34
    # define FEATURE_ACTUAL_FRAME_RATE       35
    FEATURE_SHARPNESS_SCORE = 36
    # define FEATURE_SPECIAL_CAMERA_MODE     37
    FEATURES_TOTAL = 38

    # Feature aliases for backward compatibility
    FEATURE_DECIMATION = FEATURE_PIXEL_ADDRESSING   # /* Really, decimation is just one type of pixel addressing          */
    FEATURE_EXPOSURE = FEATURE_SHUTTER            # /* IIDC'c EXPOSURE is equivalent to feature SHUTTER                 */
    FEATURE_WHITE_BAL = FEATURE_COLOR_TEMP         # /* IIDC's white balance is usually referred to as color temperature */
    FEATURE_TEMPERATURE = FEATURE_SENSOR_TEMPERATURE # /* Now more specific, as the temperature is from the sensor */

    # For PxLGetCameraFeatures
    FEATURE_ALL = -1

    # Feature Flags
    FEATURE_FLAG_PRESENCE = 0x00000001  # /* The feature is supported on this camera. */
    FEATURE_FLAG_MANUAL = 0x00000002
    FEATURE_FLAG_AUTO = 0x00000004
    FEATURE_FLAG_ONEPUSH = 0x00000008
    FEATURE_FLAG_OFF = 0x00000010
    FEATURE_FLAG_DESC_SUPPORTED = 0x00000020
    FEATURE_FLAG_READ_ONLY = 0x00000040
    FEATURE_FLAG_SETTABLE_WHILE_STREAMING = 0x00000080
    FEATURE_FLAG_PERSISTABLE = 0x00000100  # /* The feature will be saved with PxLSaveSettings */
    FEATURE_FLAG_EMULATION = 0x00000200  # /* The feature is implemented in the API, not the camera */
    FEATURE_FLAG_VOLATILE = 0x00000400  # /* The features (settable) value or limits, may change as the result of changing some other feature.  See help file for details on feature interaction */
    # Exactly one of these 'mode' bits should be set with each feature set operation
    FEATURE_FLAG_MODE_BITS = FEATURE_FLAG_MANUAL | FEATURE_FLAG_AUTO | FEATURE_FLAG_ONEPUSH | FEATURE_FLAG_OFF

    # Pixel Formats
    PIXEL_FORMAT_MONO8 = 0
    PIXEL_FORMAT_MONO16 = 1
    PIXEL_FORMAT_YUV422 = 2
    PIXEL_FORMAT_BAYER8_GRBG = 3
    PIXEL_FORMAT_BAYER16_GRBG = 4
    PIXEL_FORMAT_RGB24 = 5
    PIXEL_FORMAT_RGB48 = 6
    PIXEL_FORMAT_BAYER8_RGGB = 7
    PIXEL_FORMAT_BAYER8_GBRG = 8
    PIXEL_FORMAT_BAYER8_BGGR = 9
    PIXEL_FORMAT_BAYER16_RGGB = 10
    PIXEL_FORMAT_BAYER16_GBRG = 11
    PIXEL_FORMAT_BAYER16_BGGR = 12
    PIXEL_FORMAT_BAYER8 = PIXEL_FORMAT_BAYER8_GRBG
    PIXEL_FORMAT_BAYER16 = PIXEL_FORMAT_BAYER16_GRBG
    PIXEL_FORMAT_MONO12_PACKED = 13
    PIXEL_FORMAT_BAYER12_GRBG_PACKED = 14
    PIXEL_FORMAT_BAYER12_RGGB_PACKED = 15
    PIXEL_FORMAT_BAYER12_GBRG_PACKED = 16
    PIXEL_FORMAT_BAYER12_BGGR_PACKED = 17
    PIXEL_FORMAT_BAYER12_PACKED = PIXEL_FORMAT_BAYER12_GRBG_PACKED
    PIXEL_FORMAT_RGB24_DIB = PIXEL_FORMAT_RGB24
    PIXEL_FORMAT_RGB24_NON_DIB = 18
    PIXEL_FORMAT_RGB48_NON_DIB = PIXEL_FORMAT_RGB48
    PIXEL_FORMAT_RGB48_DIB = 19
    PIXEL_FORMAT_MONO12_PACKED_MSFIRST = 20
    PIXEL_FORMAT_BAYER12_GRBG_PACKED_MSFIRST = 21
    PIXEL_FORMAT_BAYER12_RGGB_PACKED_MSFIRST = 22
    PIXEL_FORMAT_BAYER12_GBRG_PACKED_MSFIRST = 23
    PIXEL_FORMAT_BAYER12_BGGR_PACKED_MSFIRST = 24
    PIXEL_FORMAT_BAYER12_PACKED_MSFIRST = PIXEL_FORMAT_BAYER12_GRBG_PACKED_MSFIRST

    # Stream State
    START_STREAM = 0
    PAUSE_STREAM = 1
    STOP_STREAM = 2

    # FEATURE_ROI parameters
    FEATURE_ROI_PARAM_LEFT = 0
    FEATURE_ROI_PARAM_TOP = 1
    FEATURE_ROI_PARAM_WIDTH = 2
    FEATURE_ROI_PARAM_HEIGHT = 3
    FEATURE_ROI_NUM_PARAMS = 4

    # FEATURE_FLIP parameters
    FEATURE_FLIP_PARAM_HORIZONTAL = 0
    FEATURE_FLIP_PARAM_VERTICAL = 1
    FEATURE_FLIP_NUM_PARAMS = 2

    # FEATURE_SHARPNESS_SCORE parameters
    FEATURE_SHARPNESS_SCORE_PARAM_LEFT = 0
    FEATURE_SHARPNESS_SCORE_PARAM_TOP = 1
    FEATURE_SHARPNESS_SCORE_PARAM_WIDTH = 2
    FEATURE_SHARPNESS_SCORE_PARAM_HEIGHT = 3
    FEATURE_SHARPNESS_SCORE_MAX_VALUE = 4
    FEATURE_SHARPNESS_SCORE_NUM_PARAMS = 5

    # Pixel Addressing
    FEATURE_PIXEL_ADDRESSING_PARAM_VALUE = 0
    FEATURE_PIXEL_ADDRESSING_PARAM_MODE = 1
    FEATURE_PIXEL_ADDRESSING_PARAM_X_VALUE = 2
    FEATURE_PIXEL_ADDRESSING_PARAM_Y_VALUE = 3
    FEATURE_PIXEL_ADDRESSING_NUM_PARAMS = 4

    PIXEL_ADDRESSING_MODE_DECIMATE = 0
    PIXEL_ADDRESSING_MODE_AVERAGE = 1
    PIXEL_ADDRESSING_MODE_BIN = 2
    PIXEL_ADDRESSING_MODE_RESAMPLE = 3

    PIXEL_ADDRESSING_VALUE_NONE = 1
    PIXEL_ADDRESSING_VALUE_BY_2 = 2

    # FEATURE_WHITE_SHADING (Displayed in Capture OEM as White Balance)
    FEATURE_WHITE_SHADING_PARAM_RED = 0
    FEATURE_WHITE_SHADING_PARAM_GREEN = 1
    FEATURE_WHITE_SHADING_PARAM_BLUE = 2

    FEATURE_WHITE_BALANCE_PARAM_RED = 0
    FEATURE_WHITE_BALANCE_PARAM_GREEN = 1
    FEATURE_WHITE_BALANCE_PARAM_BLUE = 2
    FEATURE_WHITE_BALANCE_NUM_PARAMS = 3

    # Standard Rotations
    FEATURE_ROTATE_0_DEG = 0
    FEATURE_ROTATE_90_DEG = 90
    FEATURE_ROTATE_180_DEG = 180
    FEATURE_ROTATE_270_DEG = 270

    # Flat-field Calibration Types
    FFC_TYPE_UNKNOWN = 0
    FFC_TYPE_UNCALIBRATED = 1
    FFC_TYPE_FACTORY = 2
    FFC_TYPE_FIELD = 3

    COMMAND_FFC_SETTINGS_READ = 0x00008001
    COMMAND_FFC_SETTINGS_WRITE = 0x00008002

    class FrameDesc(C.Structure):
        """ The 524 byte size structure passed to the GetNextFrame function
        that is populated with camera settings and frame information.
        """
        PXL_MAX_STROBES = 16
        PXL_MAX_KNEE_POINTS = 4
        _fields_ = [
            ("uSize", C.c_uint),
            ("fFrameTime", C.c_float),
            ("uFrameNumber", C.c_uint),
            ("fBrightnessValue", C.c_float),
            ("fAutoExposureValue", C.c_float),
            ("fSharpnessValue", C.c_float),
            ("fWhiteBalanceValue", C.c_float),
            ("fHueValue", C.c_float),
            ("fSaturationValue", C.c_float),
            ("fGammaValue", C.c_float),
            ("fShutterValue", C.c_float),
            ("fGainValue", C.c_float),
            ("fIrisValue", C.c_float),
            ("fFocusValue", C.c_float),
            ("fTemperatureValue", C.c_float),
            ("fTriggerMode", C.c_float),
            ("fTriggerType", C.c_float),
            ("fTriggerPolarity", C.c_float),
            ("fTriggerDelay", C.c_float),
            ("fTriggerParameter", C.c_float),
            ("fZoomValue", C.c_float),
            ("fPanValue", C.c_float),
            ("fTiltValue", C.c_float),
            ("fOpticalFilterValue", C.c_float),
            ("fGPIOMode", C.c_float * PXL_MAX_STROBES),
            ("fGPIOPolarity", C.c_float * PXL_MAX_STROBES),
            ("fGPIOParameter1", C.c_float * PXL_MAX_STROBES),
            ("fGPIOParameter2", C.c_float * PXL_MAX_STROBES),
            ("fGPIOParameter3", C.c_float * PXL_MAX_STROBES),
            ("fFrameRateValue", C.c_float),
            ("fRoiLeft", C.c_float),
            ("fRoiTop", C.c_float),
            ("fRoiWidth", C.c_float),
            ("fRoiHeight", C.c_float),
            ("fFlipHorizontal", C.c_float),
            ("fFlipVertical", C.c_float),
            ("fDecimationValue", C.c_float),
            ("fPixelFormatValue", C.c_float),
            ("ExtendedShutterKneePoint", C.c_float * PXL_MAX_KNEE_POINTS),
            ("fAutoROILeft", C.c_float),
            ("fAutoROITop", C.c_float),
            ("fAutoROIWidth", C.c_float),
            ("fAutoROIHeight", C.c_float),
            ("fDecimationModeValue", C.c_float),
            ("fWhiteShadingRedGain", C.c_float),
            ("fWhiteShadingGreenGain", C.c_float),
            ("fWhiteShadingBlueGain", C.c_float),
            ("fRotateValue", C.c_float),
            ("fImagerClkDivisorValue", C.c_float),
            ("fTriggerWithControlledLightValue", C.c_float),
            ("fMaxPixelSizeValue", C.c_float),
            ("fTriggerNumberValue", C.c_float),
            ("uImageProcessingMark", C.c_uint),
            ("fPixelAddressingHorizontal", C.c_float),
            ("fPixelAddressingVertical", C.c_float),
            ("dFrameTime", C.c_double),
            ("u64FrameNumber", C.c_longlong),
            ("fBandwidthLimitValue", C.c_float),
            ("fActualFrameRateValue", C.c_float),
            ("fSharpnessScoreParamsLeft", C.c_float),
            ("fSharpnessScoreParamsTop", C.c_float),
            ("fSharpnessScoreParamsWidth", C.c_float),
            ("fSharpnessScoreParamsHeight", C.c_float),
            ("fSharpnessScoreParamsMaxValue", C.c_float),
            ("fSharpnessScoreValue", C.c_float),
        ]

    class ErrorReport(C.Structure):
        """ This class is used as input to the GetErrorReport
        function. Wrapper class around the PxlAPi40.dll ERROR_REPORT
        structure. """
        _fields_ = [
            ("uReturnCode", C.c_int),
            ("strFunctionName", C.c_char * 32),
            ("strReturnCode", C.c_char * 32),
            ("strReport", C.c_char * 256),
        ]

        def __str__(self):
            msg = ''
            msg += ' errorCode: 0x%08x %s,' % (int(self.uReturnCode), self.strReturnCode)
            msg += ' errorDesc: %s,' % self.strReport
            msg += ' function: %s' % self.strFunctionName
            return msg

    def __init__(self, use_return_codes=False, dll_path='pxlapi40.dll'):
        self._lib = C.windll.LoadLibrary(dll_path)
        self._libPath = dll_path
        self._useReturnCodes = use_return_codes
        self._frameDesc = self.FrameDesc()
        # self._lib = self.__lib# for debugging

    @property
    def lib(self):
        return self._lib

    def __str__(self):
        return "lib = {0}, libPath = {1}".format(self._lib, self._libPath)

    def _GetErrorReport(self, h_camera):
        """ Retrieve the error report without using the wrapped API method. This
        is to ensure the exception::
            'ERROR_REPORT' object is not iterable
        is not thrown.
        Calling a wrapped function from within the wrap_return_code.wrapper
        function is not allowed.
        """
        report = self.ErrorReport()
        rc = self._lib.PxLGetErrorReport(h_camera, C.byref(report))
        return rc, report

    @wrap_return_code
    def GetErrorReport(self, h_camera):
        """ Get the last error description report from the camera. This should
        be called each time a PxLapi function is called and the return code (rc)
        is a error code.

        returns: class:`PxLapi.ErrorReport` type
        """
        return self._GetErrorReport(h_camera)

    @wrap_return_code
    def GetNumberCameras(self):
        """ Retrieves the list of cameras connected to the network (or computer)
        and returns the list of serial numbers. The number of cameras can be
        determine from the returned list length.
        """
        num_cameras = C.c_ulong(0)
        rc = self._lib.PxLGetNumberCameras(None, C.byref(num_cameras))
        if rc != 0:
            return rc, []

        serial_nums = (C.c_long * num_cameras.value)()
        rc = self._lib.PxLGetNumberCameras(C.byref(serial_nums), C.byref(num_cameras))
        return rc, [int(v) for v in serial_nums]

    @wrap_return_code
    def GetCameraFeatures(self, h_camera):
        """ Retrieves the camera features. The number of features can be
        determine from the returned list length.
        """

        class PARAMETERS(C.Structure):
            _fields_ = [
                ("min", C.c_float),
                ("max", C.c_float)
            ]

        class FEATURE(C.Structure):
            _fields_ = [
                ("featureID", C.c_int),
                ("flags", C.c_int),
                ("numberOfParameters", C.c_int),
                ("parameters", C.POINTER(PARAMETERS))
            ]

        class FEATURE_ARRAY(C.Structure):
            _fields_ = [
                ("size", C.c_int),
                ("numberOfFeatures", C.c_int),
                ("features", C.POINTER(FEATURE))
            ]

        num_features = C.c_ulong(0)
        rc = self._lib.PxLGetCameraFeatures(h_camera, PxLapi.FEATURE_ALL, None,
                                            C.byref(num_features))
        if rc != 0:
            return rc, []

        feature_data = (C.c_long * num_features.value)()
        rc = self._lib.PxLGetCameraFeatures(h_camera, PxLapi.FEATURE_ALL,
                                            C.byref(feature_data), C.byref(num_features))

        features = C.cast(feature_data, C.POINTER(FEATURE_ARRAY))
        feature_list = []
        for i in range(features.contents.numberOfFeatures):
            feature = [int(features.contents.features[i].featureID),
                       int(features.contents.features[i].flags),
                       int(features.contents.features[i].numberOfParameters)]
            feature_min_max = []
            for j in range(int(features.contents.features[i].numberOfParameters)):
                feature_min_max.append([float(features.contents.features[i].parameters[j].min),
                                        float(features.contents.features[i].parameters[j].max)])
            feature.append(feature_min_max)
            feature_list.append(feature)
        return rc, feature_list

    @wrap_return_code
    def GetFFCSettings(self, h_camera):
        """ Retrieves the camera FFC Settings. """

        class FFC_SETTINGS(C.Structure):
            _fields_ = [
                ("command", C.c_ulong),
                ("ffcInfo", C.c_ulong),
                ("ffcCalibratedGain", C.c_float)
            ]

        buf = FFC_SETTINGS()
        buf.command = C.c_ulong(PxLapi.COMMAND_FFC_SETTINGS_READ)
        buf.ffcInfo = C.c_ulong(0)
        buf.ffcCalibratedGain = C.c_float(0.0)
        input_size = (C.sizeof(buf) + 3) & ~0x3
        rc = self._lib.PxLCameraWrite(h_camera, input_size, C.byref(buf))
        if rc != 0:
            return rc, []
        rc = self._lib.PxLCameraRead(h_camera, C.sizeof(buf), C.byref(buf))
        if rc != 0:
            return rc, []
        else:
            return rc, [int(buf.ffcInfo), float(buf.ffcCalibratedGain)]

    @wrap_return_code
    def SetFFCSettings(self, h_camera, ffc_info, ffc_calibrated_gain=0.0):
        """ Set the camera FFC Settings. """

        class FFC_SETTINGS(C.Structure):
            _fields_ = [
                ("command", C.c_ulong),
                ("ffcInfo", C.c_ulong),
                ("ffcCalibratedGain", C.c_float)
            ]

        buf = FFC_SETTINGS()
        buf.command = C.c_ulong(PxLapi.COMMAND_FFC_SETTINGS_WRITE)
        buf.ffcInfo = C.c_ulong(ffc_info)
        buf.ffcCalibratedGain = C.c_float(ffc_calibrated_gain)
        input_size = (C.sizeof(buf) + 3) & ~0x3
        rc = self._lib.PxLCameraWrite(h_camera, input_size, C.byref(buf))
        if rc != 0:
            return rc, []
        rc = self._lib.PxLCameraRead(h_camera, C.sizeof(buf), C.byref(buf))
        if rc != 0:
            return rc, []
        else:
            return rc, [int(buf.ffcInfo), float(buf.ffcCalibratedGain)]

    @wrap_return_code
    def Initialize(self, serial_number=0):
        """ Initialize communication with the camera. This function must be
        called before any other driver functions.
        """
        h_camera = C.c_void_p(0)
        rc = self._lib.PxLInitialize(C.c_uint32(serial_number), C.POINTER(C.c_void_p)(h_camera))
        if rc == 0:
            return rc, h_camera
        return rc, 0

    @wrap_return_code
    def Uninitialize(self, h_camera):
        """ Close communication with the camera. This function must be the
        last call made to the underlying driver.
        """
        if h_camera:
            rc = self._lib.PxLUninitialize(h_camera)
        else:
            rc = 0
        return rc

    @wrap_return_code
    def SetStreamState(self, h_camera, state):
        """ Set the stream state: STOP_STREAM, PAUSE_STREAM, START_STREAM.
        Some API calls require the stream state to be stopped before setting
        a feature, such as ROI.
        """
        rc = self._lib.PxLSetStreamState(h_camera, state)
        return rc

    @wrap_return_code
    def GetNextFrame(self, h_camera):
        """ Retrieve the next frame when the camera is in "streaming" mode.
        Make sure SetStreamState(h_camera, PxLapi.START_STREAM) has been called
        before calling this function.

        TODO (DONE): in the future, the width and height arguments may not be needed
        since this information can be retrieved by making a call to:
        GetFeature(h_camera, PxLapi.FEATURE_ROI, 4)
        """
        sz, bits = self.GetPixelSize(h_camera)
        roi = self.GetFeature(h_camera, PxLapi.FEATURE_ROI, PxLapi.FEATURE_ROI_NUM_PARAMS)
        pixel_addressing = self.GetFeature(h_camera, PxLapi.FEATURE_PIXEL_ADDRESSING, PxLapi.FEATURE_PIXEL_ADDRESSING_NUM_PARAMS)

        if sz == 1:
            dtype = 'uint8'
        elif sz == 2:
            dtype = '>u2'  # Note: this requires development.
        elif sz == 3:
            dtype = '>u3'  # Note: this requires development.
        elif sz == 6:
            dtype = '>u6'  # Note: this requires development.
        else:
            dtype = 'uint8'

        # w = int(w)
        # h = int(h)
        w = int(roi[PxLapi.FEATURE_ROI_PARAM_WIDTH]) // int(pixel_addressing[PxLapi.FEATURE_PIXEL_ADDRESSING_PARAM_VALUE])
        h = int(roi[PxLapi.FEATURE_ROI_PARAM_HEIGHT]) // int(pixel_addressing[PxLapi.FEATURE_PIXEL_ADDRESSING_PARAM_VALUE])

        if HAS_NUMPY:
            c_void_p = C.POINTER(C.c_void_p)
            data = numpy.zeros((h, w), dtype)
            data_p = data.ctypes.data_as(c_void_p)
        else:
            # make the ctypes string buffer act like a numpy.array
            data = C.create_string_buffer(b'\0', w * h * sz)
            setattr(data, 'shape', (h, w))
            setattr(data, 'tostring', lambda: data.raw)
            data_p = C.byref(data)

        byte_count = w * h * sz
        rc = self._lib.PxLGetNextFrame(h_camera, byte_count, data_p,
                                       C.byref(self._frameDesc))
        if sz == 2:
            data >>= (16-bits)
        elif sz == 3:
            data >>= (24 - bits)
        elif sz == 6:
            data >>= (48 - bits)

        return rc, data

    @wrap_return_code
    def GetFeature(self, h_camera, feature, num_params=1):
        """ Retrieve a camera setting using the feature id definitions. """
        value = (C.c_float * num_params)()
        flags = C.c_ulong(0)
        param_len = C.c_ulong(num_params)
        rc = self._lib.PxLGetFeature(h_camera, feature,
                                     C.byref(flags), C.byref(param_len), C.byref(value))
        if rc != 0:
            return rc, 0
        elif num_params == 1:
            return rc, value[0]
        return rc, [float(v) for v in value]

    @wrap_return_code
    def GetFeatureFlags(self, h_camera, feature, num_params=1):
        """ Retrieve a camera setting using the feature id definitions. """
        value = (C.c_float * num_params)()
        flags = C.c_ulong(0)
        param_len = C.c_ulong(num_params)
        rc = self._lib.PxLGetFeature(h_camera, feature, C.byref(flags), C.byref(param_len), C.byref(value))
        if rc != 0:
            return rc, 0
        else:
            return rc, int(flags.value)

    @wrap_return_code
    def SetFeature(self, h_camera, feature, value):
        """ Set a camera setting using a feature id definition. """
        if isinstance(value, (list, tuple)):
            num_params = len(value)
            val = (C.c_float * num_params)(*value)
        else:
            num_params = 1
            val = C.c_float(value)
        flags = self.GetFeatureFlags(h_camera, feature, num_params)
        rc = self._lib.PxLSetFeature(h_camera, feature, flags, num_params,
                                     C.byref(val))
        return rc

    @wrap_return_code
    def SetFeatureFlags(self, h_camera, feature, new_flags, num_params=1):
        """ Set a camera setting using a feature id definition. """
        value = (C.c_float * num_params)()
        flags = C.c_ulong(0)
        param_len = C.c_ulong(num_params)
        rc = self._lib.PxLGetFeature(h_camera, feature, C.byref(flags), C.byref(param_len), C.byref(value))
        if rc != 0:
            return rc
        rc = self._lib.PxLSetFeature(h_camera, feature, new_flags, num_params, C.byref(value))
        return rc

    def GetPixelSize(self, h_camera):
        pix_type = -1
        pix_bits = 0
        feature = self.FEATURE_PIXEL_FORMAT
        value = (C.c_float * 1)()
        flags = C.c_ulong(0)
        param_len = C.c_ulong(1)
        rc = self._lib.PxLGetFeature(h_camera, feature,
                                     C.byref(flags), C.byref(param_len), C.byref(value))
        if rc == 0:
            pix_type = int(value[0])

        feature = self.FEATURE_MAX_PIXEL_SIZE
        rc = self._lib.PxLGetFeature(h_camera, feature,
                                     C.byref(flags), C.byref(param_len), C.byref(value))
        if rc == 0:
            pix_bits = int(value[0])

        byte_count_map = {
            self.PIXEL_FORMAT_MONO8: 1,
            self.PIXEL_FORMAT_BAYER8_GRBG: 1,
            self.PIXEL_FORMAT_BAYER8_RGGB: 1,
            self.PIXEL_FORMAT_BAYER8_GBRG: 1,
            self.PIXEL_FORMAT_BAYER8_BGGR: 1,
            self.PIXEL_FORMAT_YUV422: 2,
            self.PIXEL_FORMAT_MONO16: 2,
            self.PIXEL_FORMAT_BAYER16_GRBG: 2,
            self.PIXEL_FORMAT_BAYER16_RGGB: 2,
            self.PIXEL_FORMAT_BAYER16_GBRG: 2,
            self.PIXEL_FORMAT_BAYER16_BGGR: 2,
            self.PIXEL_FORMAT_RGB24: 3,
            self.PIXEL_FORMAT_RGB48: 6,
        }
        if pix_type in byte_count_map:
            byte_count = byte_count_map[pix_type]
        else:
            byte_count = -1  # TODO: requires development. Currently not supported

        return byte_count, pix_bits


class PxLerror(Exception):
    """ PixeLINK API exception """

    def __init__(self, api, error_code, h_camera=None, extra_info='', report=None):
        Exception.__init__(self, '')

        if report is None:
            # NOTE: _ is the return code, but is not used
            (_, report) = api.GetErrorReport(h_camera)

        self.errorCode = error_code
        self.h_camera = h_camera
        self.uReturnCode = report.uReturnCode
        self.strFunctionName = report.strFunctionName
        self.strReturnCode = report.strReturnCode
        self.strReport = report.strReport
        self.extraInfo = extra_info

    def __str__(self):
        if self.h_camera:
            cam_address = self.h_camera.value
        else:
            cam_address = 0
        msg = 'PixeLINK API error - '
        msg += self.extraInfo
        msg += ' h_camera: 0x%08x,' % cam_address
        msg += ' errorCode: 0x%08x %s,' % (int(self.errorCode), self.strReturnCode)
        msg += ' errorDesc: %s,' % self.strReport
        msg += ' function: %s' % self.strFunctionName
        return msg


class PixeLINK(object):
    """ High level interface to the PixeLINK camera. """

    feature_key_map = {
        'Brightness': PxLapi.FEATURE_BRIGHTNESS,
        'Sharpness': PxLapi.FEATURE_SHARPNESS,
        'ColorTemp': PxLapi.FEATURE_COLOR_TEMP,
        'WhiteBal': PxLapi.FEATURE_COLOR_TEMP,
        'Hue': PxLapi.FEATURE_HUE,
        'Saturation': PxLapi.FEATURE_SATURATION,
        'Gamma': PxLapi.FEATURE_GAMMA,
        'IntegrationTime': PxLapi.FEATURE_SHUTTER,
        'Exposure': PxLapi.FEATURE_SHUTTER,
        'Gain': PxLapi.FEATURE_GAIN,
        'Iris': PxLapi.NOT_IMPLEMENTED,
        'Focus': PxLapi.NOT_IMPLEMENTED,
        'SensorTemperature': PxLapi.FEATURE_SENSOR_TEMPERATURE,
        'Temperature': PxLapi.FEATURE_SENSOR_TEMPERATURE,
        'Trigger': PxLapi.NOT_IMPLEMENTED,
        'Zoom': PxLapi.NOT_IMPLEMENTED,
        'Pan': PxLapi.NOT_IMPLEMENTED,
        'Tilt': PxLapi.NOT_IMPLEMENTED,
        'OptFilter': PxLapi.NOT_IMPLEMENTED,
        'GPIO': PxLapi.NOT_IMPLEMENTED,
        'FrameRate': PxLapi.FEATURE_FRAME_RATE,
        'ROI': PxLapi.FEATURE_ROI,
        'Flip': PxLapi.FEATURE_FLIP,
        'PixelAddressing': PxLapi.FEATURE_PIXEL_ADDRESSING,
        'Decimation': PxLapi.FEATURE_PIXEL_ADDRESSING,
        'Binning': PxLapi.FEATURE_PIXEL_ADDRESSING,
        'PixelFormat': PxLapi.FEATURE_PIXEL_FORMAT,
        'ExtendedShutter': PxLapi.NOT_IMPLEMENTED,
        'AutoROI': PxLapi.NOT_IMPLEMENTED,
        'LookupTable': PxLapi.NOT_IMPLEMENTED,
        'MemoryChannel': PxLapi.FEATURE_MEMORY_CHANNEL,
        'WhiteShading': PxLapi.FEATURE_WHITE_SHADING,
        'Rotate': PxLapi.FEATURE_ROTATE,
        'TriggerWithControlledLight': PxLapi.NOT_IMPLEMENTED,
        'MaxPixelSize': PxLapi.FEATURE_MAX_PIXEL_SIZE,
        'BodyTemperature': PxLapi.FEATURE_BODY_TEMPERATURE,
        'MaxPacketSize': PxLapi.NOT_IMPLEMENTED,
        'BandwidthLimit': PxLapi.NOT_IMPLEMENTED,
        'ActualFrameRate': PxLapi.NOT_IMPLEMENTED,
        'SharpnessScore': PxLapi.FEATURE_SHARPNESS_SCORE,
        'SpecialCameraMode': PxLapi.NOT_IMPLEMENTED
    }

    def __init__(self, start_streaming=True, **kwargs):
        self._api = PxLapi()
        self._hCamera = self._api.Initialize(0)
        self._streaming = False
        self._last_frame = None

        if 'PixelFormat' in kwargs:
            self.set_property_value(PxLapi.FEATURE_PIXEL_FORMAT, kwargs.get('PixelFormat'))

        if start_streaming:
            self.streaming = True

    def is_open(self):
        """ Check if the camera is ready for communication. """
        return self._hCamera is not None

    # def __del__(self):
    #     # in case the user forgot to call the close method.
    #     self.close()

    def grab(self):
        """ Grab a single frame from the camera. """
        return self._get_frame()

    @synchronized(DEVICE_LOCK)
    def _get_frame(self):
        if self._streaming and self._api:
            data = self._api.GetNextFrame(self._hCamera)
            self._last_frame = data
        else:
            data = self._last_frame
        return data

    @staticmethod
    def get_feature_id(key):
        """ Convert the property key string to a PixeLINK feature id code. """
        if key in PixeLINK.feature_key_map:
            feature_id = PixeLINK.feature_key_map[key]
        else:
            feature_id = PxLapi.INVALID_FEATURE

        return feature_id

    @staticmethod
    def get_feature_len(feature_id):
        feature_len_map = {
            PxLapi.FEATURE_ROI: PxLapi.FEATURE_ROI_NUM_PARAMS,
            PxLapi.FEATURE_PIXEL_ADDRESSING: PxLapi.FEATURE_PIXEL_ADDRESSING_NUM_PARAMS,
            PxLapi.FEATURE_FLIP: PxLapi.FEATURE_FLIP_NUM_PARAMS,
            PxLapi.FEATURE_WHITE_SHADING: PxLapi.FEATURE_WHITE_BALANCE_NUM_PARAMS,
            PxLapi.FEATURE_SHARPNESS_SCORE: PxLapi.FEATURE_SHARPNESS_SCORE_NUM_PARAMS
        }
        if feature_id in feature_len_map:
            feature_len = feature_len_map[feature_id]
        else:
            feature_len = 1

        return feature_len

    @synchronized(DEVICE_LOCK)
    def get_property_value(self, key):
        """ Retrieve the current setting for a feature from the camera. """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)
        count = self.get_feature_len(feature_id)

        return self._api.GetFeature(self._hCamera, feature_id, count)

    @synchronized(DEVICE_LOCK)
    def get_property_flags(self, key):
        """ Retrieve the current flags for a feature from the camera. """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)
        count = self.get_feature_len(feature_id)

        return self._api.GetFeatureFlags(self._hCamera, feature_id, count)

    @synchronized(DEVICE_LOCK)
    def set_property_value(self, key, value):
        """ Send a configuration parameter to the camera. """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)

        self._api.SetFeature(self._hCamera, feature_id, value)

    @synchronized(DEVICE_LOCK)
    def set_property_flags(self, key, flags):
        """ Send a configuration parameter to the camera. """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)
        count = self.get_feature_len(feature_id)

        self._api.SetFeatureFlags(self._hCamera, feature_id, flags, count)

    @property
    def feature_names(self):
        names = sorted(self.feature_key_map.keys())
        return names

    @property
    def features_supported(self):
        result = {}
        for key in self.feature_key_map:
            try:
                result[key] = self.property_supported(key)
            except RuntimeWarning as exc:
                result[key] = str(exc)
        return result

    def property_supported(self, key):
        """ Test if a property is supported """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)
        try:
            flags = self.get_property_flags(feature_id)
            return (flags & PxLapi.FEATURE_FLAG_PRESENCE) != 0
        except PxLerror:
            return False

    def property_enabled(self, key):
        """ Test if a property is enabled """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)
        flags = self.get_property_flags(feature_id)
        return (flags & PxLapi.FEATURE_FLAG_OFF) == 0

    def enable_property(self, key, enable):
        """ Enable/disable a property """
        if isinstance(key, str):
            feature_id = self.get_feature_id(key)
            if feature_id == PxLapi.INVALID_FEATURE:
                raise RuntimeWarning('Invalid key: %s' % key)
        else:
            feature_id = key  # must be an PxLapi.FEATURE_* (int or long)
        if not isinstance(enable, bool):
            raise RuntimeWarning('enable_property: setting must be boolean')

        flags = self.get_property_flags(feature_id)
        if enable:
            flags = (flags & ~PxLapi.FEATURE_FLAG_MODE_BITS) | PxLapi.FEATURE_FLAG_MANUAL
        else:
            flags = (flags & ~PxLapi.FEATURE_FLAG_MODE_BITS) | PxLapi.FEATURE_FLAG_OFF
        self.set_property_flags(key, flags)

    @property
    def streaming(self):
        return self._streaming

    @streaming.setter
    @synchronized(DEVICE_LOCK)
    def streaming(self, state):
        if isinstance(state, (bool, int)):
            # convert to an int type
            if state:
                state = PxLapi.START_STREAM
            else:
                state = PxLapi.STOP_STREAM

        self._streaming = (state == PxLapi.START_STREAM)
        self._api.SetStreamState(self._hCamera, state)

    @property
    @synchronized(DEVICE_LOCK)
    def ffc_supported(self):
        ffc_settings = self._api.GetFFCSettings(self._hCamera)
        if not isinstance(ffc_settings, list) or len(ffc_settings) != 2:
            return False

        ffc_info, ffc_calibrated_gain = ffc_settings
        ffc_type = (ffc_info & 0xf0) >> 4
        if ffc_type == PxLapi.FFC_TYPE_UNKNOWN:
            if ffc_calibrated_gain == -1:
                return False
            else:
                return True
        if ffc_type == PxLapi.FFC_TYPE_UNCALIBRATED:
            return False
        if ffc_type == PxLapi.FFC_TYPE_FACTORY or ffc_type == PxLapi.FFC_TYPE_FIELD:
            return True
        return False

    @property
    @synchronized(DEVICE_LOCK)
    def ffc_type(self):
        ffc_settings = self._api.GetFFCSettings(self._hCamera)
        if not isinstance(ffc_settings, list) or len(ffc_settings) != 2:
            return PxLapi.FFC_TYPE_UNKNOWN

        ffc_info, ffc_calibrated_gain = ffc_settings
        ffc_type = ((ffc_info) & 0xF0) >> 4
        if ffc_type == PxLapi.FFC_TYPE_UNKNOWN:
            if ffc_calibrated_gain == -1:
                return PxLapi.FFC_TYPE_UNCALIBRATED
            else:
                return PxLapi.FFC_TYPE_UNKNOWN
        return ffc_type

    @property
    @synchronized(DEVICE_LOCK)
    def ffc_enabled(self):
        if not self.ffc_supported:
            return False

        ffc_settings = self._api.GetFFCSettings(self._hCamera)
        if not isinstance(ffc_settings, list) or len(ffc_settings) != 2:
            return False

        ffc_info = ffc_settings[0]
        return not (ffc_info & 0xf == 0)

    @ffc_enabled.setter
    @synchronized(DEVICE_LOCK)
    def ffc_enabled(self, state):
        if not isinstance(state, bool):
            return

        if not self.ffc_supported:
            return

        self._api.SetFFCSettings(self._hCamera, [0, 1][state])

    @property
    def binning(self):
        return self.get_property_value(PxLapi.FEATURE_PIXEL_ADDRESSING)

    @binning.setter
    @synchronized(DEVICE_LOCK)
    @safe_streaming
    def binning(self, value):
        return self.set_property_value(PxLapi.FEATURE_PIXEL_ADDRESSING, value)

    @property
    def brightness(self):
        return self.get_property_value(PxLapi.FEATURE_BRIGHTNESS)

    @brightness.setter
    def brightness(self, value):
        return self.set_property_value(PxLapi.FEATURE_BRIGHTNESS, value)

    @property
    def sharpness(self):
        return self.get_property_value(PxLapi.FEATURE_SHARPNESS)

    @sharpness.setter
    def sharpness(self, value):
        return self.set_property_value(PxLapi.FEATURE_SHARPNESS, value)

    @property
    def color_temp(self):
        return self.get_property_value(PxLapi.FEATURE_COLOR_TEMP)

    @color_temp.setter
    def color_temp(self, value):
        return self.set_property_value(PxLapi.FEATURE_COLOR_TEMP, value)

    @property
    def hue(self):
        return self.get_property_value(PxLapi.FEATURE_HUE)

    @hue.setter
    def hue(self, value):
        return self.set_property_value(PxLapi.FEATURE_HUE, value)

    @property
    def saturation(self):
        return self.get_property_value(PxLapi.FEATURE_SATURATION)

    @saturation.setter
    def saturation(self, value):
        return self.set_property_value(PxLapi.FEATURE_SATURATION, value)

    @property
    def gamma(self):
        return self.get_property_value(PxLapi.FEATURE_GAMMA)

    @gamma.setter
    def gamma(self, value):
        return self.set_property_value(PxLapi.FEATURE_GAMMA, value)

    @property
    def shutter(self):
        return self.get_property_value(PxLapi.FEATURE_SHUTTER)

    @shutter.setter
    def shutter(self, seconds):
        return self.set_property_value(PxLapi.FEATURE_SHUTTER, seconds)

    @property
    def gain(self):
        return self.get_property_value(PxLapi.FEATURE_GAIN)

    @gain.setter
    def gain(self, value):
        return self.set_property_value(PxLapi.FEATURE_GAIN, value)

    @property
    def sensor_temperature(self):
        return self.get_property_value(PxLapi.FEATURE_SENSOR_TEMPERATURE)

    @property
    def frame_rate(self):
        return self.get_property_value(PxLapi.FEATURE_FRAME_RATE)

    @frame_rate.setter
    @synchronized(DEVICE_LOCK)
    @safe_streaming
    def frame_rate(self, value):
        """ Setting the frame rate can only occur if the streaming
        is in a stopped state and the frame rate is enabled. Be sure to execute:

             cam.streaming=False

        before setting this property.
        """
        self.enable_property(PxLapi.FEATURE_FRAME_RATE, True)
        self.set_property_value(PxLapi.FEATURE_FRAME_RATE, value)

    @property
    def size(self):
        x0, y0, x1, y1 = self.roi
        return x1 - x0, y1 - y0

    @property
    def pixel_size(self):
        byte_count, pix_bits = self._api.GetPixelSize(self._hCamera)
        return byte_count

    @property
    def roi(self):
        roi = self.get_property_value(PxLapi.FEATURE_ROI)
        return [int(v) for v in roi]

    @roi.setter
    @synchronized(DEVICE_LOCK)
    @safe_streaming
    def roi(self, ltwh_tuple):
        """ Setting the region of interest can only occur if the streaming
        is in a stopped state. Be sure to execute::

             cam.streaming=False

        before setting this property.
        """
        self.set_property_value(PxLapi.FEATURE_ROI, ltwh_tuple)

    @property
    def flip(self):
        flip = self.get_property_value(PxLapi.FEATURE_FLIP)
        return [int(v) for v in flip]

    @flip.setter
    def flip(self, flip_tuple):
        self.set_property_value(PxLapi.FEATURE_FLIP, flip_tuple)

    @property
    def pixel_addressing(self):
        """ Also known as decimation, binning """
        pixel_addressing = self.get_property_value(PxLapi.FEATURE_PIXEL_ADDRESSING)
        return [int(v) for v in pixel_addressing]

    @pixel_addressing.setter
    @synchronized(DEVICE_LOCK)
    @safe_streaming
    def pixel_addressing(self, pxl_addr_tuple):
        """ Setting the pixel addressing can only occur if the streaming
        is in a stopped state. Be sure to execute::

             cam.streaming=False

        before setting this property.

        :param tuple pxl_addr_tuple: (value, mode)
            mode => 0: Decimate, 1: Average, 2: Bin, 3: Resample

        """
        return self.set_property_value(PxLapi.FEATURE_PIXEL_ADDRESSING, pxl_addr_tuple)

    @property
    def pixel_format(self):
        return int(self.get_property_value(PxLapi.FEATURE_PIXEL_FORMAT))

    @pixel_format.setter
    @synchronized(DEVICE_LOCK)
    @safe_streaming
    def pixel_format(self, value):
        """ Setting the pixel format can only occur if the streaming
        is in a stopped state. Be sure to execute::

             cam.streaming=False

        before setting this property.
        """
        return self.set_property_value(PxLapi.FEATURE_PIXEL_FORMAT, value)

    @property
    def memory_channel(self):
        return int(self.get_property_value(PxLapi.FEATURE_MEMORY_CHANNEL))

    @property
    def white_shading(self):
        white_shading_values = self.get_property_value(PxLapi.FEATURE_WHITE_SHADING)
        return [float(v) for v in white_shading_values]

    @white_shading.setter
    def white_shading(self, white_shading_tuple):
        return self.set_property_value(PxLapi.FEATURE_WHITE_SHADING, white_shading_tuple)

    @property
    def rotate(self):
        return self.get_property_value(PxLapi.FEATURE_ROTATE)

    @rotate.setter
    @synchronized(DEVICE_LOCK)
    @safe_streaming
    def rotate(self, value):
        return self.set_property_value(PxLapi.FEATURE_ROTATE, value)

    @property
    def max_pixel_size(self):
        return self.get_property_value(PxLapi.FEATURE_MAX_PIXEL_SIZE)

    @property
    def body_temperature(self):
        return self.get_property_value(PxLapi.FEATURE_BODY_TEMPERATURE)

    @property
    def sharpness_score(self):
        sharpness_score_values = self.get_property_value(PxLapi.FEATURE_SHARPNESS_SCORE)
        return [float(v) for v in sharpness_score_values]

    @sharpness_score.setter
    def sharpness_score(self, sharpness_score_tuple):
        return self.set_property_value(PxLapi.FEATURE_SHARPNESS_SCORE, sharpness_score_tuple)

    @synchronized(DEVICE_LOCK)
    def close(self):
        """ Stop streaming and close communication with the camera. """

        # disallow close more than once check.
        if self._hCamera is None:
            return

        self._api.SetStreamState(self._hCamera, PxLapi.STOP_STREAM)
        self._api.Uninitialize(self._hCamera)
        self._hCamera = None
        self._api = None  # no further calls are allowed to this class
