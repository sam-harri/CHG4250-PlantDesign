from utils.Components import *
from utils.Stream import Stream
from units.PLSMixer import AcidMixer

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

acidic_pls = Stream(stream_number=3,
    origin="PLSMixer",
    destination="Extraction"
)

pls_mixer = AcidMixer(
    name="PLSMixer",
    pls_stream=overflow,
    acid_stream=pls_acid,
    acidic_pls=acidic_pls,
)

print(overflow)
print()
print(pls_acid)
print()
print(acidic_pls)
print(f"Mass Balance : {overflow.total_mass+pls_acid.total_mass-acidic_pls.total_mass}")