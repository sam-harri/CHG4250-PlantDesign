from models.IsothermModeling import IsothermModel
from units.Extraction import Extraction

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
        isotherm_model=extraction_isotherm,
        ratio=1 / 1.5,
        inlet_Uconcentration=17.5,
        num_stages=4,
        efficiency=0.7,
    )
