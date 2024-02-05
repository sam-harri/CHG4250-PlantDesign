from utils.Components import (
    UO2_2p,
    Water,
    SO4_2m,
    H_1p,
    Mg,
    Fe,
    SiO2,
    Al2SiO5,
    UO2SO4,
)
from utils.Stream import Stream
from models.IsothermModeling import IsothermModel
from units.PLSMixer import PLSMixer
from units.Extraction import Extraction


overflow = Stream(
    stream_number=1,
    origin="Filtration",
    destination="PLSMixer",
    components=[
        UO2_2p(13.37),
        Water(2929.17),
        SO4_2m(97.09),
        H_1p(1.41),
        Mg(5.01),
        Fe(5.75),
        SiO2(7.43),
        Al2SiO5(10.02),
    ],
)

pls_acid = Stream(
    stream_number=2,
    origin="AcidTank",
    destination="PLSMixer",
)

acidic_pls = Stream(
    stream_number=3,
    origin="PLSMixer",
    destination="Extraction"
)

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
    components=[UO2SO4(0.0461)],
    recycle=True,
)

depleted_raffinate = Stream(
    stream_number=6,
    origin="Extraction",
    destination="Out",
)

Extraction_Unit = Extraction(
    name="Extraction",
    isotherm_model=IsothermModel(
        data_path="data/UeqExtrationData.csv",
        x_label="U(aq)",
        y_label="U(org)",
        change_intercept=False,
    ),
    pls=acidic_pls,
    stripped_organic=barren_organic,
    loaded_organic=loaded_organic,
    depleted_raffinate=depleted_raffinate,
    num_stages=4,
    efficiency=0.9,
    OA_ratio=1.5,
    plot=True,
)

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
print(Extraction_Unit.mass_balance())
