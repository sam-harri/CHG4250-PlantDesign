from models.IsothermModeling import IsothermModel

if __name__ == "__main__":
    model = IsothermModel(
        data_path="data/UraniumEquilibriumData.csv",
        x_label="U(aq)",
        y_label="U(org)",
    )

