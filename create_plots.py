import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

base_folder = "./plots"


df1 = pd.read_excel("Hossein - Map 1.xlsx", sheet_name="Sheet1")
df2 = pd.read_excel("Hossein - Map 2.xlsx", sheet_name="Sheet1")


combined_df = pd.concat(
    [df1.assign(Map="Map 1"), df2.assign(Map="Map 2")], ignore_index=True
)

pallete_group = {"Sketch Map": "#d1ba24", "Verbal": "#35d124"}
pallete_group_dot = {"Sketch Map": "#333", "Verbal": "#333"}

pallete_order = {"first": "#f54242", "second": "#4287f5"}
pallete_order_dot = {"first": "#333", "second": "#333"}


def create_box_plot(
    data,
    title,
    filename,
    column,
    folder,
    label,
    yticks,
    ylabels,
    min,
    max,
    groupBy="Participant Group (for this video)",
    palette=pallete_group,
    pallete2=pallete_group_dot,
    order=["Verbal", "Sketch Map"],
):
    plt.figure(figsize=(8.5, 6))
    plot = sns.boxplot(
        x=groupBy,
        y=column,
        data=data,
        palette=palette,
        hue=groupBy,
        showfliers=False,
        order=order,
        medianprops={"linewidth": 2},
    )
    plot.set(yticks=yticks)
    plot.set(yticklabels=ylabels)
    sns.stripplot(
        x=groupBy,
        y=column,
        data=data,
        palette=pallete2,
        size=6,
        jitter=0.2,
        alpha=0.6,
        hue=groupBy,
        order=order,
    )
    plt.ylim(min, max)
    plt.ylabel(label)
    plt.title(title)
    plt.xlabel("")
    # plt.xticks(rotation=45)
    plt.tight_layout()

    path_main = Path(base_folder) / folder
    path_main.mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(path_main, f"{filename}.png")
    plt.savefig(filepath, dpi=300)
    plt.close()


only_first_as_Verbal_second_as_Sketch_Map = combined_df[
    (
        (combined_df["Experiment Order"] == "first")
        & (combined_df["Participant Group (for this video)"] == "Verbal")
    )
    | (
        (combined_df["Experiment Order"] == "second")
        & (combined_df["Participant Group (for this video)"] == "Sketch Map")
    )
]

only_first_as_Sketch_Map_second_as_Verbal = combined_df[
    (
        (combined_df["Experiment Order"] == "first")
        & (combined_df["Participant Group (for this video)"] == "Sketch Map")
    )
    | (
        (combined_df["Experiment Order"] == "second")
        & (combined_df["Participant Group (for this video)"] == "Verbal")
    )
]


# 1. Identify your sketch-only rows
sketch_mask = combined_df["Participant Group (for this video)"] == "Sketch Map"

# 2. Compute the median sketch score
median_score_task3 = combined_df.loc[sketch_mask, "Orientation Points"].median()

# 3. Find all Participant IDs whose sketch score is > median (top 50%)
top_sketch_ids = combined_df.loc[
    sketch_mask & (combined_df["Orientation Points"] > median_score_task3),
    "Participant ID",
].unique()

# 4. Keep only everyone *not* in that top-sketch list
low_50_sketch_task3 = combined_df.loc[
    ~combined_df["Participant ID"].isin(top_sketch_ids)
].copy()

# 5. Extract the top-50% sketch performers (both their sketch & verbal rows)
top_50_sketch_task3 = combined_df.loc[
    combined_df["Participant ID"].isin(top_sketch_ids)
].copy()

create_box_plot(
    data=low_50_sketch_task3,
    title="Orientation Estimation (Both Maps)",
    filename="low_50_sketch_orientation_estimation",
    column="Orientation Points",
    folder="task3_mean_filtered",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
)

create_box_plot(
    data=top_50_sketch_task3,
    title="Orientation Estimation (Both Maps)",
    filename="top_50_sketch_orientation_estimation",
    column="Orientation Points",
    folder="task3_mean_filtered",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
)

media_score_task2 = combined_df.loc[sketch_mask, "Distance Sum"].median()

# 3. Find all Participant IDs whose sketch score is > median (top 50%)
top_sketch_ids_task2 = combined_df.loc[
    sketch_mask & (combined_df["Distance Sum"] > media_score_task2), "Participant ID"
].unique()
# 4. Keep only everyone *not* in that top-sketch list
low_50_sketch_task2 = combined_df.loc[
    ~combined_df["Participant ID"].isin(top_sketch_ids_task2)
].copy()
# 5. Extract the top-50% sketch performers (both their sketch & verbal rows)
top_50_sketch_task2 = combined_df.loc[
    combined_df["Participant ID"].isin(top_sketch_ids_task2)
].copy()
create_box_plot(
    data=low_50_sketch_task2,
    title="Distance Estimation (Both Maps)",
    filename="low_50_sketch_distance_estimation",
    column="Distance Sum",
    folder="task2_mean_filtered",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
)
create_box_plot(
    data=top_50_sketch_task2,
    title="Distance Estimation (Both Maps)",
    filename="top_50_sketch_distance_estimation",
    column="Distance Sum",
    folder="task2_mean_filtered",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
)


# Task 1: Sequence Ordering ==>
create_box_plot(
    data=combined_df,
    title="Sequence Ordering (Both Maps)",
    filename="sequence_ordering_combined",
    column="best_spearman",
    folder="task1",
    label="Score",
    yticks=[-1, -0.5, 0, 0.5, 1],
    ylabels=["-1", "-0.5", "0", "0.5", "1 (max)"],
    min=-1,
    max=1.03,
)

create_box_plot(
    data=df1,
    title="Sequence Ordering (Map 1)",
    filename="sequence_ordering_map1",
    column="best_spearman",
    folder="task1",
    label="Score",
    yticks=[-1, -0.5, 0, 0.5, 1],
    ylabels=["-1", "-0.5", "0", "0.5", "1 (max)"],
    min=-1,
    max=1.03,
)

create_box_plot(
    data=df2,
    title="Sequence Ordering (Map 2)",
    filename="sequence_ordering_map2",
    column="best_spearman",
    folder="task1",
    label="Score",
    yticks=[-1, -0.5, 0, 0.5, 1],
    ylabels=["-1", "-0.5", "0", "0.5", "1 (max)"],
    min=-1,
    max=1.03,
)

# experiment ordering
create_box_plot(
    data=combined_df,
    title="Experience Order: Sequence Ordering",
    filename="eo_sequence_ordering_both",
    column="best_spearman",
    folder="order_task1",
    label="Score",
    yticks=[-1, -0.5, 0, 0.5, 1],
    ylabels=["-1", "-0.5", "0", "0.5", "1 (max)"],
    min=-1,
    max=1.03,
    groupBy="Experiment Order",
    palette=pallete_order,
    pallete2=pallete_order_dot,
    order=["first", "second"],
)


create_box_plot(
    data=only_first_as_Verbal_second_as_Sketch_Map,
    title="Experience Order: Sequence Ordering (First as Verbal)",
    filename="eo_sequence_ordering_first_as_verbal",
    column="best_spearman",
    folder="order_task1",
    label="Score",
    yticks=[-1, -0.5, 0, 0.5, 1],
    ylabels=["-1", "-0.5", "0", "0.5", "1 (max)"],
    min=-1,
    max=1.03,
    groupBy="Participant Group (for this video)",
)


create_box_plot(
    data=only_first_as_Sketch_Map_second_as_Verbal,
    title="Experience Order: Sequence Ordering (First as Sketch Map)",
    filename="eo_sequence_ordering_first_as_sketch_map",
    column="best_spearman",
    folder="order_task1",
    label="Score",
    yticks=[-1, -0.5, 0, 0.5, 1],
    ylabels=["-1", "-0.5", "0", "0.5", "1 (max)"],
    min=-1,
    max=1.03,
    groupBy="Participant Group (for this video)",
    order=["Sketch Map", "Verbal"],
)
# <== Task 1: Sequence Ordering

# Task 2: Distance Estimation ==>
create_box_plot(
    data=combined_df,
    title="Distance Estimation (Both Maps)",
    filename="distance_estimation_combined",
    column="Distance Sum",
    folder="task2",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
)

create_box_plot(
    data=df1,
    title="Distance Estimation (Map 1)",
    filename="distance_estimation_map1",
    column="Distance Sum",
    folder="task2",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
)
create_box_plot(
    data=df2,
    title="Distance Estimation (Map 2)",
    filename="distance_estimation_map2",
    column="Distance Sum",
    folder="task2",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
)

# experiment ordering Task 2

create_box_plot(
    data=combined_df,
    title="Experience Order: Distance Estimation",
    filename="eo_distance_estimation_both",
    column="Distance Sum",
    folder="order_task2",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
    groupBy="Experiment Order",
    palette=pallete_order,
    pallete2=pallete_order_dot,
    order=["first", "second"],
)

create_box_plot(
    data=only_first_as_Verbal_second_as_Sketch_Map,
    title="Experience Order: Distance Estimation (First as Verbal)",
    filename="eo_distance_estimation_first_as_verbal",
    column="Distance Sum",
    folder="order_task2",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
    groupBy="Participant Group (for this video)",
)

create_box_plot(
    data=only_first_as_Sketch_Map_second_as_Verbal,
    title="Experience Order: Distance Estimation (First as Sketch Map)",
    filename="eo_distance_estimation_first_as_sketch_map",
    column="Distance Sum",
    folder="order_task2",
    label="Number of correctly estimated distances",
    yticks=[0, 1, 2, 3, 4, 5],
    ylabels=["0", "1", "2", "3", "4", "5 (max)"],
    min=0,
    max=5.2,
    groupBy="Participant Group (for this video)",
    order=["Sketch Map", "Verbal"],
)


# <== Task 2: Distance Estimation

# Task 3: Orientation Estimation ==>

create_box_plot(
    data=combined_df,
    title="Orientation Estimation (Both Maps)",
    filename="orientation_estimation_combined",
    column="Orientation Points",
    folder="task3",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
)


create_box_plot(
    data=df1,
    title="Orientation Estimation (Map 1)",
    filename="orientation_estimation_map1",
    column="Orientation Points",
    folder="task3",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
)
create_box_plot(
    data=df2,
    title="Orientation Estimation (Map 2)",
    filename="orientation_estimation_map2",
    column="Orientation Points",
    folder="task3",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
)


# experiment ordering Task 3

create_box_plot(
    data=combined_df,
    title="Experience Order: Orientation Estimation",
    filename="eo_orientation_estimation_both",
    column="Orientation Points",
    folder="order_task3",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
    groupBy="Experiment Order",
    palette=pallete_order,
    pallete2=pallete_order_dot,
    order=["first", "second"],
)

create_box_plot(
    data=only_first_as_Verbal_second_as_Sketch_Map,
    title="Experience Order: Orientation Estimation (First as Verbal)",
    filename="eo_orientation_estimation_first_as_verbal",
    column="Orientation Points",
    folder="order_task3",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
    groupBy="Participant Group (for this video)",
)
create_box_plot(
    data=only_first_as_Sketch_Map_second_as_Verbal,
    title="Experience Order: Orientation Estimation (First as Sketch Map)",
    filename="eo_orientation_estimation_first_as_sketch_map",
    column="Orientation Points",
    folder="order_task3",
    label="Score",
    yticks=[0, 8, 16, 24, 32, 40],
    ylabels=["0", "8", "16", "24", "32", "40 (max)"],
    min=0,
    max=41,
    groupBy="Participant Group (for this video)",
    order=["Sketch Map", "Verbal"],
)
# <== Task 3: Orientation Estimation


print("Plots created successfully.")
