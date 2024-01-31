from models.IsothermModeling import IsothermModel
from units.Extraction import Extraction
from units.Stripping import Stripping

from numpy.polynomial import Polynomial

if __name__ == "__main__":
    extraction_isotherm = IsothermModel(
        data_path="data/UeqExtrationData.csv",
        x_label="U(aq)",
        y_label="U(org)",
    )

    stripping_isotherm = IsothermModel(
        data_path="data/UeqStrippingData.csv",
        x_label="U(org)",
        y_label="U(aq)",
    )

    extraction_unit = Extraction(
        name="Extraction",
        isotherm_model=extraction_isotherm,
        operating_line=Polynomial([0, 1 / 1.5]),
        inlet_Uconcentration=17.5,
        num_stages=4,
        efficiency=0.85,
        plot=True,
    )

    stripping_unit = Stripping(
        name="Stripping",
        isotherm_model=stripping_isotherm,
        operating_line=Polynomial([0, 3]),
        inlet_Uconcentration=extraction_unit.get_loaded_organic_Uconcentration(),
        num_stages=5,
        efficiency=0.85,
        plot=True,
    )
