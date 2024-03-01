import numpy as np
import json
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
        return 0

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
        return 0

    return_dict = {
        "params" : {
            "num_stage_extract" : num_stage_extract,
            "num_stage_strip" : num_stage_strip,
            "OA_extract" : OA_extract,
            "OA_strip" : OA_strip,
            "tentative_BO" : tentative_BO,
            "tentative_DR" : tentative_DR,
        },
        "results" : {
            "wasted_uranium" : depleted_raffinate.get_component_property("UO2SO4", "mass_flow"),
            "strip_liq_conc" : Stripping_unit.get_strip_concentration(),
            "extraction_per_stage" : Extraction_unit.extraction_per_stage(),
            "stripping_per_stage" : Stripping_unit.stripping_per_stage(),
        }
    }

    return return_dict


extraction_stages = [4]
stripping_stages = [5]
oa_extraction = list(np.linspace(1.2, 1.75, 7))
oa_stripping = list(np.linspace(2.0, 3.5, 7))
tentative_BO = list(np.linspace(0.005, 0.008, 7))
tentative_DR = list(np.linspace(0.1, 0.8, 7))

number_of_trials =  len(extraction_stages) * len(stripping_stages) * len(oa_extraction) * len(oa_stripping) * len(tentative_BO) * len(tentative_DR)
print(number_of_trials)

run = 1
data = {}

for extract_stage in extraction_stages:
    for strip_stage in stripping_stages:
        for oa_extract in oa_extraction:
            for oa_strip in oa_stripping:
                for bo in tentative_BO:
                    for dr in tentative_DR:
                        result = SXSimulator(
                            num_stage_extract=extract_stage,
                            num_stage_strip=strip_stage,
                            OA_extract=oa_extract,
                            OA_strip=oa_strip,
                            tentative_BO=bo,
                            tentative_DR=dr,
                        )
                        if isinstance(result, dict):
                            data[run] = result.copy()
                            if run % 100 == 0:
                                print(f"{((run/number_of_trials) * 100):.2}% complete")
                        run += 1
with open('data_4_5.json', 'w') as fp:
    json.dump(data, fp)