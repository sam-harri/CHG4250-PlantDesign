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

if __name__ == "__main__":
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
        num_stages=4,
        efficiency=0.95,
        OA_ratio=1.625,
        tentative_BO=0.005,
        tentative_DR=0.0558,
        plot=False,
    )

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
        num_stages=5,
        OA_ratio=2.72,
        efficiency=0.95,
        plot=False,
    )

    print(f"overflow volume : {loaded_organic.total_mass/loaded_organic.total_volume}")
    print(overflow)
    print()
    print(pls_acid)
    print()
    print(acidic_pls)
    print()
    print(PLSMixer_unit.mass_balance())
    print()
    print(loaded_organic)
    print()
    print(barren_organic)
    print()
    print(depleted_raffinate)
    print()
    print(Extraction_unit.mass_balance())
    print()
    print(dilute_acid)
    print()
    print(strip_liquor.total_volume)
    print()
    print(Stripping_unit.mass_balance())
    print(strip_liquor.total_volume/3600)
    print(strip_liquor.total_mass/strip_liquor.total_volume)
    print(loaded_organic.total_volume/3600)