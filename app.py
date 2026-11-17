import streamlit as st
import pandas as pd
import pickle
import os
import plotly.express as px

from data_analysis import (
    basic_analysis,
    location_analysis,
    waste_type_analysis,
    event_analysis,
    generate_insights
)


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Campus Waste Watch",
    page_icon="♻️",
    layout="wide"
)


# --------------------------------
# TITLE
# --------------------------------

st.title("♻️ Campus Waste Watch")

st.subheader(
    "Smart Waste Monitoring and Overflow Risk Analysis"
)

st.write(
    "A data-driven dashboard designed to monitor waste-bin "
    "fill levels, analyse collection patterns and identify "
    "bins that may require attention."
)

st.divider()


# --------------------------------
# LOAD DATA
# --------------------------------

@st.cache_data
def load_observations():

    return pd.read_excel(
        "Campus_Waste_Watch.xlsx",
        sheet_name="Observations"
    )


@st.cache_data
def load_collections():

    return pd.read_excel(
        "Campus_Waste_Watch.xlsx",
        sheet_name="Collection_Records"
    )


@st.cache_data
def load_bins():

    return pd.read_excel(
        "Campus_Waste_Watch.xlsx",
        sheet_name="Bin_Master"
    )


try:

    df = load_observations()

    collection_df = load_collections()

    bin_df = load_bins()

except Exception as error:

    st.error(
        f"Unable to load Excel workbook: {error}"
    )

    st.stop()


# --------------------------------
# DATA VALIDATION
# --------------------------------

required_columns = [
    "Observation_ID",
    "Date",
    "Time",
    "Bin_ID",
    "Location",
    "Fill_Level_Percent",
    "Hours_Since_Collection",
    "Waste_Type",
    "Event_Day",
    "Overflow_Before_Next_Collection"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Missing columns in Observations sheet: {missing_columns}"
    )

    st.stop()


# Convert numeric columns
df["Fill_Level_Percent"] = pd.to_numeric(
    df["Fill_Level_Percent"],
    errors="coerce"
)

df["Hours_Since_Collection"] = pd.to_numeric(
    df["Hours_Since_Collection"],
    errors="coerce"
)

df["Event_Day"] = pd.to_numeric(
    df["Event_Day"],
    errors="coerce"
)

df["Overflow_Before_Next_Collection"] = pd.to_numeric(
    df["Overflow_Before_Next_Collection"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "Fill_Level_Percent",
        "Hours_Since_Collection",
        "Event_Day"
    ]
)

df["DateTime"] = pd.to_datetime(
    df["Date"].astype(str) + " " + df["Time"].astype(str),
    errors="coerce"
)


# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Dashboard",
        "Observations",
        "Collection Records",
        "Bin Information",
        "Data Analysis",
        "Overflow Risk Estimation"
    ]
)


# --------------------------------
# DASHBOARD
# --------------------------------

if page == "Dashboard":

    st.header("Dashboard Overview")

    analysis = basic_analysis(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Observations",
        analysis["Total Observations"]
    )

    col2.metric(
        "Total Bins",
        analysis["Total Bins"]
    )

    col3.metric(
        "Average Fill Level",
        f'{analysis["Average Fill Level"]}%'
    )

    col4.metric(
        "Recorded Overflow Labels",
        analysis["Overflow Cases"]
    )

    st.divider()

    st.subheader("Location-wise Average Fill Level")

    location_data = (
        location_analysis(df)
        .reset_index()
    )

    fig = px.bar(
        location_data,
        x="Location",
        y="Fill_Level_Percent",
        title="Average Bin Fill Level by Location",
        labels={
            "Fill_Level_Percent": "Average Fill Level (%)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Latest Recorded Status of Each Bin")

    latest_data = (
        df.dropna(subset=["DateTime"])
        .sort_values("DateTime")
        .groupby("Bin_ID")
        .tail(1)
        .sort_values(
            "Fill_Level_Percent",
            ascending=False
        )
    )

    st.dataframe(
        latest_data[
            [
                "Bin_ID",
                "Location",
                "Fill_Level_Percent",
                "Waste_Type"
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "Latest status is based on the most recent observation "
        "available in the dataset."
    )


# --------------------------------
# OBSERVATIONS
# --------------------------------

elif page == "Observations":

    st.header("Waste Bin Observations")

    st.write(
        "View the recorded fill levels and conditions of waste bins."
    )

    st.dataframe(
        df.drop(columns=["DateTime"], errors="ignore"),
        use_container_width=True
    )

    st.download_button(
        "Download Observations CSV",
        df.drop(columns=["DateTime"], errors="ignore").to_csv(
            index=False
        ),
        file_name="observations.csv",
        mime="text/csv"
    )


# --------------------------------
# COLLECTION RECORDS
# --------------------------------

elif page == "Collection Records":

    st.header("Waste Collection Records")

    st.dataframe(
        collection_df,
        use_container_width=True
    )

    st.subheader("Collection Completion")

    if "Collection_Completed" in collection_df.columns:

        completion = (
            collection_df["Collection_Completed"]
            .value_counts()
            .reset_index()
        )

        completion.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            completion,
            names="Status",
            values="Count",
            title="Collection Completion Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------
# BIN INFORMATION
# --------------------------------

elif page == "Bin Information":

    st.header("Bin Information")

    st.dataframe(
        bin_df,
        use_container_width=True
    )

    st.metric(
        "Total Registered Bins",
        len(bin_df)
    )


# --------------------------------
# DATA ANALYSIS
# --------------------------------

elif page == "Data Analysis":

    st.header("Data Analysis and Insights")

    st.subheader("Waste Type Analysis")

    waste_data = (
        waste_type_analysis(df)
        .reset_index()
    )

    fig = px.bar(
        waste_data,
        x="Waste_Type",
        y="Fill_Level_Percent",
        title="Average Fill Level by Waste Type",
        labels={
            "Fill_Level_Percent": "Average Fill Level (%)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Event Day Comparison")

    event_data = (
        event_analysis(df)
        .rename(index={
            0: "Non-event Day",
            1: "Event Day"
        })
        .reset_index()
    )

    event_data.columns = [
        "Day Type",
        "Average Fill Level"
    ]

    fig = px.bar(
        event_data,
        x="Day Type",
        y="Average Fill Level",
        title="Average Fill Level: Event vs Non-event Days"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Automatic Insights")

    insights = generate_insights(df)

    for insight in insights:

        st.info(insight)

    st.subheader("Suggested Actions")

    average_fill = df["Fill_Level_Percent"].mean()

    if average_fill >= 70:

        st.warning(
            "Review collection frequency in locations "
            "with consistently high fill levels."
        )

    else:

        st.success(
            "The overall average fill level is below 70%. "
            "Continue monitoring individual bins."
        )

    highest_location = (
        location_analysis(df).idxmax()
    )

    st.write(
        f"*Priority for review:* {highest_location}"
    )


# --------------------------------
# OVERFLOW RISK ESTIMATION
# --------------------------------

elif page == "Overflow Risk Estimation":

    st.header("Overflow Risk Estimation")

    st.write(
        "Enter the current bin conditions to estimate "
        "the possibility of overflow before the next collection."
    )

    st.warning(
        "This model is trained on illustrative sample data. "
        "Its estimates are for demonstration only and are not "
        "validated real-world predictions."
    )

    location = st.selectbox(
        "Select Location",
        sorted(df["Location"].dropna().unique())
    )

    fill_level = st.slider(
        "Current Fill Level (%)",
        0,
        100,
        50
    )

    hours = st.number_input(
        "Hours Since Last Collection",
        min_value=0.0,
        max_value=72.0,
        value=4.0
    )

    waste_type = st.selectbox(
        "Waste Type",
        ["Dry", "Wet", "Mixed"]
    )

    event_day = st.selectbox(
        "Is it an Event Day?",
        ["No", "Yes"]
    )

    if st.button("Estimate Overflow Risk"):

        if not os.path.exists("waste_model.pkl"):

            st.error(
                "Model not found. Run model.py first."
            )

        else:

            try:

                with open(
                    "waste_model.pkl",
                    "rb"
                ) as file:

                    model = pickle.load(file)

                input_data = pd.DataFrame(
                    [[
                        location,
                        fill_level,
                        hours,
                        waste_type,
                        1 if event_day == "Yes" else 0
                    ]],
                    columns=[
                        "Location",
                        "Fill_Level_Percent",
                        "Hours_Since_Collection",
                        "Waste_Type",
                        "Event_Day"
                    ]
                )

                probability = model.predict_proba(
                    input_data
                )[0]

                classes = list(
                    model.named_steps[
                        "classifier"
                    ].classes_
                )

                overflow_index = classes.index(1)

                risk = probability[overflow_index] * 100

                st.metric(
                    "Estimated Overflow Score",
                    f"{risk:.2f}%"
                )

                if risk >= 70:

                    st.error(
                        "High estimated risk. "
                        "Verify the bin and consider priority collection."
                    )

                elif risk >= 40:

                    st.warning(
                        "Moderate estimated risk. "
                        "Monitor the bin."
                    )

                else:

                    st.success(
                        "Low estimated risk. "
                        "Continue routine monitoring."
                    )

                st.caption(
                    "The score is a model output, not a verified "
                    "probability of actual overflow."
                )

            except Exception as error:

                st.error(
                    f"Prediction error: {error}"
                )


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "Campus Waste Watch | Waste Monitoring and Data Analysis Prototype"
)

st.caption(
    "Sample data is illustrative. Actual campus observations "
    "are required for real-world evaluation."
)
