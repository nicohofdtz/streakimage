from collections import namedtuple
from types import SimpleNamespace

ParaList = namedtuple(
    "ParaList",
    "Application Camera Acquisition Grabber DisplayLUT ExternalDevices StreakCamera Spectrograph DelayBox Delay2Box Scaling Comment",
    defaults=(None, None, None, None, None, None, None, None, None, None, None, None),
)
Application = namedtuple(
    "Application",
    "Date Time Software Application ApplicationTitle SoftwareVersion SoftwareDate",
    defaults=(None, None, None, None, None, None, None),
)
Camera = namedtuple(
    "Camera",
    "AMD EMD NMD SMD ADS SHT FBL EST SHA SFD SPX TNS ATP CEG CEO ESC TimingMode TriggerMode TriggerSource VerticalBinning TapNo TriggerPolarity CCDArea Binning ScanMode NoLines CameraName Type SubType",
    defaults=(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ),
)
Acquisition = namedtuple(
    "Acquisition",
    "NrExposure NrTrigger ExposureTime AcqMode DataType DataTypeOfSingleImage CurveCorr DefectCorrection areSource areGRBScan pntOrigCh pntOrigFB pntBinning BytesPerPixel IsLineData BacksubCorr ShadingCorr ZAxisLabel ZAxisUnit",
    defaults=(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ),
)
Grabber = namedtuple("Grabber", "ConfigFile Type SubType ICPMemSize")
DisplayLUT = namedtuple(
    "DisplayLUT",
    "EntrySize LowerValue UpperValue BitRange Color LUTType LUTInverted DisplayNegative Gamma First812OvlCol Lut16xShift Lut16xOvlVal",
    defaults=(None, None, None, None, None, None, None, None, None, None, None, None),
)
ExternalDevices = namedtuple(
    "ExternalDevices",
    "TriggerDelay PostTriggerTime ExposureTime TDStatusCableConnected ConnectMonitorOut ConnectResetIn TriggerMethod UseDTBE A6538Connected CounterBoardInstalled GPIBInstalled CounterBoardIOBase GPIBIOBase",
    defaults=(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ),
)
Streakcamera = namedtuple(
    "Streakcamera",
    "UseDevice DeviceName PluginName InstalledOption1 GPIBCableConnected GPIBBase TimeRange Mode GateMode MCPGain Shutter BlankingAmp Delay Phase FocusTimeOver PLLmode PLLstatus InpPower",
    defaults=(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ),
)
Spectrograph = namedtuple(
    "Spectrograph",
    "UseDevice DeviceName PluginName GPIBCableConnected GPIBBase Wavelength Grating SlitWidth Blaze Ruling",
    defaults=(None, None, None, None, None, None, None, None, None, None),
)
Delaybox = namedtuple("Delaybox", "UseDevice")
Delay2box = namedtuple("Delay2box", "UseDevice")
Scaling = namedtuple(
    "Scaling",
    "ScalingXType ScalingXScale ScalingXUnit ScalingXScalingFile ScalingYType ScalingYScale ScalingYUnit ScalingYScalingFile",
    defaults=(None, None, None, None, None, None, None, None),
)
Comment = namedtuple("Comment", "UserComment")


# def build_parameters_tuple(para_dict: dict) -> ParaList:
#     """ Builds the category tuples from the category dicts
    
#     args:
#         para_dict: the comment dictionary

#     return:
#         The returned object ist a namedtuple of all parameters.

#     """
#     app_tuple = Application(**para_dict["Application"])
#     cam_tuple = Camera(**para_dict["Camera"])
#     acq_tuple = Acquisition(**para_dict["Acquisition"])
#     grabber_tuple = Grabber(**para_dict["Grabber"])
#     display_tuple = DisplayLUT(**para_dict["DisplayLUT"])
#     extdevices_tuple = ExternalDevices(**para_dict["ExternalDevices"])
#     streak_tuple = Streakcamera(**para_dict["Streakcamera"])
#     spec_tuple = Spectrograph(**para_dict["Spectrograph"])
#     delaybox_tuple = Delaybox(**para_dict["Delaybox"])
#     delay2box_tuple = Delay2box(**para_dict["Delay2box"])
#     scaling_tuple = Scaling(**para_dict["Scaling"])
#     comment_tuple = Comment(**para_dict["Comment"])

#     # build the parameters tuple from the category tuples
#     para_tuple = ParaList(
#         app_tuple,
#         cam_tuple,
#         acq_tuple,
#         grabber_tuple,
#         display_tuple,
#         extdevices_tuple,
#         streak_tuple,
#         spec_tuple,
#         delaybox_tuple,
#         delay2box_tuple,
#         scaling_tuple,
#         comment_tuple,
#     )

#     return para_tuple
    
def build_parameters_tuple(para_dict: dict) -> SimpleNamespace:
    return get_namespace(para_dict)

def get_namespace(dict_: dict) -> SimpleNamespace:
    return SimpleNamespace(**{k:(v if not isinstance(v, dict) else get_namespace(v)) for k,v in dict_.items()})