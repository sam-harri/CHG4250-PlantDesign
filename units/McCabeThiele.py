import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt


from models.IsothermModeling import IsothermModel


class McCabeThiele:
    def __init__(
        self,
        isotherm_model: IsothermModel,
        operating_line: float,  # OpLine = Va/Vo
        inlet_Uconcentration: float,
        num_stages: int,
        efficiency: float,
        plot: bool,
    ) -> None:
        self.isotherm_poly = isotherm_model.characteristic_poly
        self.operating_line = operating_line
        self.__inlet_Uconcentration = inlet_Uconcentration
        self.__efficiency = efficiency
        self.__num_stages = num_stages

        self.__create_staircase()

        if plot:
            self.__plot()

    def __plot(self) -> None:
        X_isotherm = np.linspace(0, self.__inlet_Uconcentration, 100)
        Y_isotherm = self.isotherm_poly(X_isotherm)

        plt.plot(X_isotherm, Y_isotherm)
        plt.plot(
            [0, self.__inlet_Uconcentration],
            [self.operating_line(0), self.operating_line(self.__inlet_Uconcentration)],
        )

        for i in range(len(self.__X_staircase)):
            plt.plot(self.__X_staircase[i], self.__Y_staircase[i], c="black")

        plt.xlim(left=0)
        plt.ylim(0, self.operating_line(self.__inlet_Uconcentration) * 1.05)
        # plt.xlabel("Uranium in Aqueous Phase (g/L)")
        # plt.ylabel("Uranium in Organic Phase (g/L)")
        # plt.title(
        #     f"Extraction Stripping McCabe-Thiele @ {self.__efficiency*100}% efficiency"
        # )
        plt.show()

    def __create_staircase(self) -> None:
        self.__X_staircase = [
            [self.__inlet_Uconcentration, self.__inlet_Uconcentration]
        ]
        self.__Y_staircase = [[0, self.operating_line(self.__inlet_Uconcentration)]]

        current = [
            self.__inlet_Uconcentration,
            self.operating_line(self.__inlet_Uconcentration),
        ]
        self.__loaded_organic_Uconcentration = current[1]

        for _ in range(self.__num_stages):
            intersection_poly = self.isotherm_poly - Polynomial([current[1]])
            roots = intersection_poly.roots()

            real_roots = [root.real for root in roots if np.isclose(root.imag, 0)]
            x = next(
                (
                    current[0] - ((current[0] - root) * self.__efficiency)
                    for root in real_roots
                    if 0 <= root <= self.__inlet_Uconcentration
                ),
                None,
            )
            if x is None:
                raise "No Real Roots found in McCabe and Thiele range"

            y = current[1]
            self.__X_staircase.append([current[0], x])
            self.__Y_staircase.append([current[1], y])
            current = [x, y]

            y = self.operating_line(x)
            self.__X_staircase.append([current[0], x])
            self.__Y_staircase.append([current[1], y])
            current = [x, y]

        self.__depleted_raffinate_Uconcentration = current[0]

    def get_loaded_organic(self) -> float:
        """returns the concentration of U in g/L in the loaded organic phase"""
        return self.__loaded_organic_Uconcentration

    def get_depleted_raffinate(self) -> float:
        """returns the concenrtation of U in g/L in the depleted raffinate"""
        return self.__depleted_raffinate_Uconcentration
