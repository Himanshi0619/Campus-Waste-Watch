import pandas as pd


def load_dataset():

    df = pd.read_excel(
        "Campus_Waste_Watch.xlsx",
        sheet_name="Observations"
    )

    return df


def basic_analysis(df):

    total_observations = len(df)

    total_bins = df["Bin_ID"].nunique()

    average_fill = df["Fill_Level_Percent"].mean()

    highest_fill = df["Fill_Level_Percent"].max()

    overflow_cases = (
        df["Overflow_Before_Next_Collection"].sum()
    )

    return {
        "Total Observations": total_observations,
        "Total Bins": total_bins,
        "Average Fill Level": round(average_fill, 2),
        "Highest Fill Level": highest_fill,
        "Overflow Cases": int(overflow_cases)
    }


def location_analysis(df):

    result = (
        df.groupby("Location")["Fill_Level_Percent"]
        .mean()
        .sort_values(ascending=False)
    )

    return result


def waste_type_analysis(df):

    result = (
        df.groupby("Waste_Type")["Fill_Level_Percent"]
        .mean()
        .sort_values(ascending=False)
    )

    return result


def event_analysis(df):

    result = (
        df.groupby("Event_Day")["Fill_Level_Percent"]
        .mean()
    )

    return result


def generate_insights(df):

    insights = []

    average_fill = df["Fill_Level_Percent"].mean()

    if average_fill >= 70:

        insights.append(
            "The overall average fill level is high. "
            "Review collection frequency."
        )

    else:

        insights.append(
            "The overall average fill level is below 70%."
        )

    location_data = location_analysis(df)

    highest_location = location_data.idxmax()

    insights.append(
        f"{highest_location} has the highest average fill level."
    )

    overflow_cases = (
        df["Overflow_Before_Next_Collection"].sum()
    )

    insights.append(
        f"The dataset contains {int(overflow_cases)} recorded overflow labels."
    )

    return insights
