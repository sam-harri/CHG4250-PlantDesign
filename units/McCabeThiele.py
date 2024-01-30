from numpy.polynomial import Polynomial

from models.IsothermModeling import IsothermModel

class McCabeThiele:
    def __init__(self, isotherm_model : IsothermModel, ratio : float) -> None:
        self.isotherm_poly = isotherm_model.characteristic_poly
        self.operating_poly = Polynomial([0, 1/ratio]) 