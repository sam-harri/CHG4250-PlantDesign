import numpy as np
from numpy.polynomial import Polynomial
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


class IsothermModel:
    def __init__(
        self,
        data_path: str,
        x_label: str,
        y_label: str,
        min_degree=2,
        max_degree=5,
        plot: bool = False,
        change_intercept: bool = True,
    ):
        self.__equilibrium_dataframe = pd.read_csv(data_path)
        self.x_label = x_label
        self.y_label = y_label
        self.__intercept = change_intercept
        # sk learn expects 2D tensor of shape (Features, Samples)
        self.__X = self.__equilibrium_dataframe[[self.x_label]].values
        self.__Y = self.__equilibrium_dataframe[self.y_label].values

        self.__min_poly_degree = min_degree
        self.__max_poly_degree = max_degree

        self.__mse_scores = {}
        self.__best_degree = self.__find_best_degree()
        self.characteristic_poly = self.__train_and_convert_to_numpy_poly()

        if plot:
            self.__plot_mse_vs_degree()
            self.__plot_predictions()

    def __fit_poly_to_dataset(self, n):
        model = make_pipeline(
            PolynomialFeatures(n, include_bias=self.__intercept),
            LinearRegression(fit_intercept=False),
        )
        scores = cross_val_score(
            model,
            self.__X,
            self.__Y,
            cv=LeaveOneOut(),
            scoring="neg_mean_squared_error",
        )
        # remove last element
        return -np.mean(scores)  # returns MSE

    def __find_best_degree(self):
        best_score = float("inf")
        best_degree = None

        for degree in range(self.__min_poly_degree, self.__max_poly_degree + 1):
            score = self.__fit_poly_to_dataset(degree)
            self.__mse_scores[degree] = score

            if score < best_score:
                best_score = score
                best_degree = degree

        return best_degree

    def __plot_mse_vs_degree(self):
        degrees = list(self.__mse_scores.keys())
        scores = list(self.__mse_scores.values())

        plt.plot(degrees, scores, marker="o")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Mean Squared Error (MSE)")
        plt.title("MSE vs. Polynomial Degree")

        plt.xticks(degrees)

        for i, score in enumerate(scores):
            plt.text(degrees[i], score, f"{score:.2f}", ha="center", va="bottom")

        plt.show()

    def __plot_for_degree(self, ax, degree):
        model = make_pipeline(
            PolynomialFeatures(degree, include_bias=self.__intercept),
            LinearRegression(fit_intercept=False),
        )
        model.fit(self.__X, self.__Y)
        y_pred = model.predict(self.__X)

        ax.scatter(self.__X, self.__Y, alpha=0.7, label="Actual")
        ax.scatter(self.__X, y_pred, alpha=0.7, label="Predicted")
        ax.set_title(f"Polynomial Degree {degree}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

    def __plot_predictions(self):
        num_plots = self.__max_poly_degree - self.__min_poly_degree + 1
        n_rows = num_plots // 2 + num_plots % 2
        n_cols = 2 if self.__max_poly_degree - self.__min_poly_degree + 1 > 1 else 1
        _, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 5))
        axs = axs.flatten() if n_rows > 1 else [axs]

        for i, degree in enumerate(
            range(self.__min_poly_degree, self.__max_poly_degree + 1)
        ):
            self.__plot_for_degree(axs[i], degree)

        plt.tight_layout()
        plt.show()

    def __train_and_convert_to_numpy_poly(self):
        best_model = make_pipeline(
            PolynomialFeatures(self.__best_degree, include_bias=self.__intercept),
            LinearRegression(fit_intercept=False),
        )
        best_model.fit(self.__X, self.__Y)
        coefs = best_model.named_steps["linearregression"].coef_
        if not self.__intercept:
            coefs = np.concatenate([[0], coefs])
        self.characteristic_poly = Polynomial(coefs)
        return self.characteristic_poly
