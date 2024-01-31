from models.IsothermModeling import IsothermModel
from units.Extraction import Extraction
from units.Stripping import Stripping
from utils.Stream import Stream

from numpy.polynomial import Polynomial

if __name__ == "__main__":
    #stream definitions
    pls = Stream(
        stream_number=1,
        origin="Filtration",
        target="Extraction",
        U_concentration=17.5,
        volume=2,
    )
    
    barren_organic = Stream(
        stream_number=2,
        origin="Stripping",
        target="Extraction",
        U_concentration=
    )
    
    
    
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
        inlet_streams=[]
        outlet_streams=[]
        efficiency=0.85,
        plot=True,
    )

    # stripping_unit = Stripping(
    #     name="Stripping",
    #     isotherm_model=stripping_isotherm,
    #     operating_line=Polynomial([0, 3]),
    #     inlet_Uconcentration=extraction_unit.get_loaded_organic_Uconcentration(),
    #     num_stages=5,
    #     efficiency=0.85,
    #     plot=True,
    # )
