from collections import namedtuple

ParaList = namedtuple(
    "ParaList",
    "Application Camera Acquisition Grabber DisplayLUT ExternalDevices StreakCamera Spectrograph DelayBox Delay2Box Scaling Comment",
)
Application = namedtuple(
    "Application",
    "Date Time Software Application ApplicationTitle SoftwareVersion SoftwareDate",
)
Camera = namedtuple(
    "Camera",
    "AMD NMD EMD SMD ADS SHT FBL EST SHA SFD SPX TNS ATP CEG CEO ESC TimingMode TriggerMode TriggerSource VerticalBinning TapNo TriggerPolarity CCDArea Binning ScanMode NoLines CameraName Type SubType",
)
Acquisition = namedtuple(
    "Acquisition",
    "NrExposure NrTrigger ExposureTime AcqMode DataType DataTypeOfSingleImage CurveCorr DefectCorrection areSource areGRBScan pntOrigCh pntOrigFB pntBinning BytesPerPixel IsLineData BacksubCorr ShadingCorr ZAxisLabel ZAxisUnit",
)
Grabber = namedtuple("Grabber", "ConfigFile Type SubType ICPMemSize")
DisplayLUT = namedtuple(
    "DisplayLUT",
    "EntrySize LowerValue UpperValue BitRange Color LUTType LUTInverted DisplayNegative Gamma First812OvlCol Lut16xShift Lut16xOvlVal",
)
ExternalDevices = namedtuple(
    "ExternalDevices",
    "TriggerDelay PostTriggerTime ExposureTime TDStatusCableConnected ConnectMonitorOut ConnectResetIn TriggerMethod UseDTBE A6538Connected CounterBoardInstalled CounterBoardIOBase GPIBIOBase",
)
Streakcamera = namedtuple(
    "Streakcamera",
    "DeviceName PluginName InstalledOption1 GPIBBase TimeRange Mode GateMode MCPGain Shutter BlankingAmp Delay Phase FocusTimeOver PLLmode PLLstatus InpPower",
)
Spectrograph = namedtuple(
    "Spectrograph",
    "DeviceName PluginName GPIBBase Wavelength Grating SlitWidth Blaze Ruling",
)
Delaybox = namedtuple("Delaybox", "UseDevice")
Delay2box = namedtuple("Delay2box", "UseDevice")
Scaling = namedtuple(
    "Scaling",
    "ScalingXType ScalingXScale ScalingXUnit ScalingXScalingFile ScalingYType ScalingYUnit ScalingYScalingFile",
)
Comment = namedtuple("Comment", "UserComment")


def build_parameters_tuple(para_dict: dict):
    # build the category tuples from the category dicts
    app_tuple = Application(**para_dict["Application"])
    cam_tuple = Camera(**para_dict["Camera"])
    acq_tuple = Acquisition(**para_dict["Acquisition"])
    grabber_tuple = Grabber(**para_dict["Grabber"])
    display_tuple = DisplayLUT(**para_dict["DisplayLUT"])
    extdevices_tuple = ExternalDevices(**para_dict["ExternalDevices"])
    streak_tuple = Streakcamera(**para_dict["Streakcamera"])
    spec_tuple = Spectrograph(**para_dict["Spectrograph"])
    delaybox_tuple = Delaybox(**para_dict["Delaybox"])
    delay2box_tuple = Delay2box(**para_dict["Delay2box"])
    scaling_tuple = Scaling(**para_dict["Scaling"])
    comment_tuple = Comment(**para_dict["Comment"])

    # build the parameters tuple from the category tuples
    para_tuple = ParaList(
        app_tuple,
        cam_tuple,
        acq_tuple,
        grabber_tuple,
        display_tuple,
        extdevices_tuple,
        streak_tuple,
        spec_tuple,
        delaybox_tuple,
        delay2box_tuple,
        scaling_tuple,
        comment_tuple,
    )

    return para_tuple
