import pandas as pd
import os
from scipy import interpolate


def get_mono_correction(camera_name: str):
    if camera_name == "C4742-95":
        return uv_vis_mono_correction()()
    if camera_name == "C4742-95-12ER":
        return ir_mono_correction()


def uv_vis_mono_correction(camera_name: str, data: pd.Dataframe, extrapolate=False):
    disp = pd.read_csv(
        os.path.join(
            os.path.dirname(__file__),
            f"correction_data/{camera_name}_corrections/{camera_name}_mono.dat",
        ),
        delimiter="\t",
        index_col=0,
        names=[""],
        squeeze=True,
    )
    wls = data.columns.values
    if (
        wls[0] < disp.index.values[0] or wls[-1] > disp.index.values[-1]
    ) and not extrapolate:
        raise IndexError(
            "Data bounds exceed the measured mono correction. To use interpolation explicitly set extrapolate=True"
        )
    else:
        interpolate_disp = interpolate.interp1d(
            disp.index.values, disp.values, fill_value="extrapolate"
        )
        corr = interpolate_disp(wls)
        data /= corr


def ir_mono_correction():
    pass
