import numpy as np
from utils.Components import (
    Water,
    SO4_2m,
    H_1p,
    Mg,
    Fe,
    SiO2,
    UO2SO4,
    MN2_1p,
    Al_3p,
)
from utils.Stream import Stream
from models.IsothermModeling import IsothermModel
from units.PLSMixer import PLSMixer
from units.Extraction import Extraction
from units.Stripping import Stripping

BEST_REWARD = -np.inf
BEST_PARAMS = {}


def SXSimulator(
    num_stage_extract: int,
    num_stage_strip: int,
    OA_extract: float,
    OA_strip: float,
    tentative_BO: float,
    tentative_DR: float,
):
    global BEST_REWARD
    global BEST_PARAMS

    overflow = Stream(
        stream_number=1,
        origin="In",
        destination="PLSMixer",
        components=[
            Water(1075.428),
            H_1p(0.004993),
            UO2SO4(16.60078),
            SO4_2m(33.40968),
            Fe(6.3524),
            MN2_1p(1.063569),
            Mg(3.262506),
            SiO2(3.871035),
            Al_3p(1.331062),
        ],
    )

    pls_acid = Stream(
        stream_number=2,
        origin="In",
        destination="PLSMixer",
    )

    acidic_pls = Stream(stream_number=3, origin="PLSMixer", destination="Extraction")

    PLSMixer_unit = PLSMixer(
        name="PLSMixer",
        pls_stream=overflow,
        acid_stream=pls_acid,
        acidic_pls=acidic_pls,
    )

    loaded_organic = Stream(
        stream_number=4,
        origin="Extraction",
        destination="Stripping",
    )

    barren_organic = Stream(
        stream_number=5,
        origin="Stripping",
        destination="Extraction",
    )

    depleted_raffinate = Stream(
        stream_number=6,
        origin="Extraction",
        destination="Out",
    )

    Extraction_unit = Extraction(
        name="Extraction",
        isotherm_model=IsothermModel(
            data_path="data/UeqExtrationData.csv",
            x_label="U(aq)",
            y_label="U(org)",
            change_intercept=False,
            plot=False,
        ),
        pls=acidic_pls,
        stripped_organic=barren_organic,
        loaded_organic=loaded_organic,
        depleted_raffinate=depleted_raffinate,
        num_stages=num_stage_extract,
        efficiency=0.95,
        OA_ratio=OA_extract,
        tentative_BO=tentative_BO,
        tentative_DR=tentative_DR,
        plot=False,
    )

    if Extraction_unit.error():
        return -20

    dilute_acid = Stream(
        stream_number=7,
        origin="In",
        destination="Stripping",
    )

    strip_liquor = Stream(stream_number=8, origin="Extraction", destination="Out")

    Stripping_unit = Stripping(
        name="Stripping",
        isotherm_model=IsothermModel(
            data_path="data/UeqStrippingData.csv",
            x_label="U(org)",
            y_label="U(aq)",
            plot=False,
        ),
        loaded_organic=loaded_organic,
        stripping_agent=dilute_acid,
        stripped_organic=barren_organic,
        strip_liquor=strip_liquor,
        stripped_org_Uconc=Extraction_unit.stripped_org_Uconc,
        loaded_org_Uconc=Extraction_unit.loaded_org_Uconc,
        num_stages=num_stage_strip,
        efficiency=0.95,
        OA_ratio=OA_strip,
        plot=False,
    )

    if Stripping_unit.error():
        return -20

    wasted_uranium_penalty =  -5/1.61 * (depleted_raffinate.get_component_property("UO2SO4", "mass_flow")-0.23)
    high_concentration_reward = 1/8.97 * (Stripping_unit.get_strip_concentration()- 7.33)

    reward_vector = [
        wasted_uranium_penalty,
        high_concentration_reward,
    ]
    reward = sum(reward_vector)
    print(reward)
    if reward > BEST_REWARD:
        print(f'{depleted_raffinate.get_component_property("UO2SO4", "mass_flow")}kg Wasted Uranium\n{Stripping_unit.get_strip_concentration()}gU/L in SL\nOA_extract : {OA_extract}\nOA_strip : {OA_strip}')
        
        BEST_REWARD = reward
        BEST_PARAMS = {
            "num_stage_extract": num_stage_extract,
            "num_stage_strip": num_stage_strip,
            "OA_extract": OA_extract,
            "OA_strip": OA_strip,
            "tentative_BO": tentative_BO,
            "tentative_DR": tentative_DR,
        }

    return reward