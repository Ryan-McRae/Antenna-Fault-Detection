from src.utils import setup
from models import models
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np

import seaborn as sns

if __name__ == "__main__":
    # setup.create_tables()
    # setup.ttv_split()
    # df = setup.group_wise_comparison()

    # cmap = mcolors.ListedColormap(["red", "yellow", "green"])
    # bounds:list=[0.0, 0.3, 0.7, 1.0]
    # norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # # df = df.corr()
    # plt.figure(figsize=(8, 6))
    # sns.heatmap(
    #     df.abs(), annot=df, cmap=cmap, norm=norm, fmt=".2f", linewidths=0.5
    # )

    # plt.title("Feature Correlation Matrix")
    # plt.tight_layout()
    # plt.show()

    training_df = setup.get_table(table="train")
    x = training_df.iloc[:, [1,2,3,4,5,6,7]].to_numpy()
    # print(training_df.iloc[:, [1,2,3,4,5,6,7]].columns)
    # y = training_df.iloc[:, [-1]].to_numpy()

    # testing_df = setup.get_table(table="val")
    # x_predict = testing_df.iloc[:, [1,2,3,4,5,6,7]].to_numpy()
    # y_actual = testing_df.iloc[:, [-1]].to_numpy()
    # y_predict = models.decision_tree(x,y, x_predict)
    # print(y_actual)
    # print(y_predict[:, np.newaxis])

    # print(y_actual - y_predict[:, np.newaxis])
    # Assuming 'df' is your DataFrame containing your 7 features and a 'Fault_Type' column
# 1. Melt the DataFrame into long format
    features = [
        "S11 (dB)",
        "VSWR",
        "Gain (dBi)",
        "Eff (%)",
        "BW (MHz)",
        "Z_Real (Ohms)",
        "Z_Imag (Ohms)",
    ]

    df_melted = pd.melt(
        training_df,
        id_vars=["Fault_Type"],  # Keep your target label
        value_vars=features,  # The 7 RF features
        var_name="Feature",
        value_name="Z_Score",
    )

    # Optional: Map your integer fault types to readable names for a clean legend
    fault_mapping = {
        0: "Healthy",
        1: "Broken Element",
        2: "Length Variation",
        3: "Bad Connection",
        4: "Bending",
        5: "Humidity",
    }
    df_melted["Fault_Name"] = df_melted["Fault_Type"].map(fault_mapping)

    # 2. Set up the Seaborn plot
    plt.figure(figsize=(14, 7))

    # You can use sns.boxplot, sns.violinplot, or sns.stripplot here.
    # A boxplot is great for seeing the median and spread of Z-scores per feature per fault.
    sns.boxplot(
        data=df_melted,
        x="Feature",
        y="Z_Score",
        hue="Fault_Name",
        palette="Set2",
        showfliers=False,  # Set to True if you want to see outlier points
    )

    plt.title("Z-Score Distribution of RF Features Across Antenna Fault Types")
    plt.xlabel("RF Feature")
    plt.ylabel("Z-Score (Standard Deviations from Global Mean)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Fault Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    plt.show()
