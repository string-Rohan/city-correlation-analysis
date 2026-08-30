# ============================================================
# BDA MINI PROJECT
# Correlation Visualization:
# Compare Data Spread Across Multiple Cities
# Using Statistical Measures
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="City Correlation Analysis",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.metric-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #f5f7fa;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📊 City Correlation & Statistical Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Compare data spread across multiple cities using statistical measures'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA GENERATION
# ============================================================

@st.cache_data
def generate_dataset():

    np.random.seed(42)

    cities = [
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Chennai",
        "Kolkata"
    ]

    data = []

    for city in cities:

        # ----------------------------------------
        # Generate city-specific data
        # ----------------------------------------

        if city == "Mumbai":

            temperature = np.random.normal(
                29, 2.0, 50
            )

            humidity = np.random.normal(
                78, 5, 50
            )

            rainfall = np.random.exponential(
                8, 50
            )

            aqi = np.random.normal(
                140, 20, 50
            )

        elif city == "Delhi":

            temperature = np.random.normal(
                34, 3.0, 50
            )

            humidity = np.random.normal(
                52, 8, 50
            )

            rainfall = np.random.exponential(
                4, 50
            )

            aqi = np.random.normal(
                190, 30, 50
            )

        elif city == "Bangalore":

            temperature = np.random.normal(
                25, 1.8, 50
            )

            humidity = np.random.normal(
                65, 6, 50
            )

            rainfall = np.random.exponential(
                5, 50
            )

            aqi = np.random.normal(
                85, 15, 50
            )

        elif city == "Chennai":

            temperature = np.random.normal(
                32, 2.2, 50
            )

            humidity = np.random.normal(
                72, 5, 50
            )

            rainfall = np.random.exponential(
                7, 50
            )

            aqi = np.random.normal(
                125, 20, 50
            )

        else:

            temperature = np.random.normal(
                30, 2.3, 50
            )

            humidity = np.random.normal(
                70, 6, 50
            )

            rainfall = np.random.exponential(
                6, 50
            )

            aqi = np.random.normal(
                130, 22, 50
            )

        # ----------------------------------------
        # Add observations
        # ----------------------------------------

        for i in range(50):

            data.append([
                city,
                temperature[i],
                humidity[i],
                rainfall[i],
                aqi[i]
            ])

    df = pd.DataFrame(
        data,
        columns=[
            "City",
            "Temperature",
            "Humidity",
            "Rainfall",
            "AQI"
        ]
    )

    # ----------------------------------------
    # Clean / constrain values
    # ----------------------------------------

    df["Temperature"] = (
        df["Temperature"]
        .round(2)
    )

    df["Humidity"] = (
        df["Humidity"]
        .clip(20, 100)
        .round(2)
    )

    df["Rainfall"] = (
        df["Rainfall"]
        .round(2)
    )

    df["AQI"] = (
        df["AQI"]
        .clip(20, 500)
        .round()
        .astype(int)
    )

    return df


df = generate_dataset()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Analysis Controls")

cities = sorted(
    df["City"].unique()
)

selected_cities = st.sidebar.multiselect(
    "Select Cities",
    cities,
    default=cities
)

variables = [
    "Temperature",
    "Humidity",
    "Rainfall",
    "AQI"
]

selected_variable = st.sidebar.selectbox(
    "Select Variable",
    variables,
    index=0
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Dataset contains 250 observations "
    "across 5 cities."
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["City"].isin(selected_cities)
]


# ============================================================
# CHECK CITY SELECTION
# ============================================================

if len(selected_cities) == 0:

    st.warning(
        "Please select at least one city from the sidebar."
    )

    st.stop()


# ============================================================
# TOP METRICS
# ============================================================

st.subheader("📌 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Observations",
        len(filtered_df)
    )

with col2:

    st.metric(
        "Cities",
        filtered_df["City"].nunique()
    )

with col3:

    st.metric(
        f"Average {selected_variable}",
        f"{filtered_df[selected_variable].mean():.2f}"
    )

with col4:

    st.metric(
        f"Std. Deviation",
        f"{filtered_df[selected_variable].std():.2f}"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Dataset",
    "📈 Statistics",
    "🔗 Correlation",
    "📊 Visualizations",
    "💡 Findings"
])


# ============================================================
# TAB 1 — DATASET
# ============================================================

with tab1:

    st.subheader("Dataset")

    st.write(
        "The dataset contains simulated environmental "
        "observations for five major Indian cities."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=450
    )

    st.subheader("Dataset Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write("**Columns:**")

        st.write(
            "• City\n"
            "• Temperature\n"
            "• Humidity\n"
            "• Rainfall\n"
            "• AQI"
        )

    with info_col2:

        st.write("**Dataset Size:**")

        st.write(
            f"Rows: {len(filtered_df)}"
        )

        st.write(
            f"Columns: {len(filtered_df.columns)}"
        )

    # Download dataset

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Dataset",
        data=csv,
        file_name="city_environmental_data.csv",
        mime="text/csv"
    )


# ============================================================
# TAB 2 — STATISTICAL ANALYSIS
# ============================================================

with tab2:

    st.subheader(
        "📐 Statistical Measures"
    )

    st.write(
        "The following statistical measures are used "
        "to understand the central tendency and spread "
        "of data across cities."
    )

    # ----------------------------------------
    # City-wise statistics
    # ----------------------------------------

    statistics = (
        filtered_df
        .groupby("City")[variables]
        .agg([
            "mean",
            "median",
            "var",
            "std"
        ])
        .round(2)
    )

    st.write(
        "**Mean, Median, Variance and Standard Deviation**"
    )

    st.dataframe(
        statistics,
        use_container_width=True
    )

    # ----------------------------------------
    # Selected variable
    # ----------------------------------------

    st.markdown("---")

    st.subheader(
        f"📌 {selected_variable} — City Comparison"
    )

    variable_stats = (
        filtered_df
        .groupby("City")[selected_variable]
        .agg([
            "mean",
            "median",
            "var",
            "std",
            "min",
            "max"
        ])
        .round(2)
    )

    variable_stats.columns = [
        "Mean",
        "Median",
        "Variance",
        "Standard Deviation",
        "Minimum",
        "Maximum"
    ]

    st.dataframe(
        variable_stats,
        use_container_width=True
    )

    # ----------------------------------------
    # Mathematical explanation
    # ----------------------------------------

    st.markdown("---")

    st.subheader(
        "🧮 Mathematical Foundation"
    )

    st.latex(
        r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i"
    )

    st.write(
        "**Mean:** Measures the average value "
        "of the observations."
    )

    st.latex(
        r"s^2 = \frac{\sum (x_i-\bar{x})^2}{n-1}"
    )

    st.write(
        "**Variance:** Measures how far observations "
        "are spread from the mean."
    )

    st.latex(
        r"s = \sqrt{s^2}"
    )

    st.write(
        "**Standard Deviation:** Represents the "
        "typical spread of observations."
    )


# ============================================================
# TAB 3 — CORRELATION
# ============================================================

with tab3:

    st.subheader(
        "🔗 Pearson Correlation Analysis"
    )

    st.write(
        "Pearson correlation measures the strength "
        "and direction of the linear relationship "
        "between two numerical variables."
    )

    st.latex(
        r"""
        r =
        \frac{
        \sum (x_i-\bar{x})(y_i-\bar{y})
        }{
        \sqrt{
        \sum(x_i-\bar{x})^2
        \sum(y_i-\bar{y})^2
        }
        }
        """
    )

    # ----------------------------------------
    # Correlation matrix
    # ----------------------------------------

    correlation_matrix = (
        filtered_df[variables]
        .corr(method="pearson")
    )

    st.subheader(
        "Correlation Matrix"
    )

    st.dataframe(
        correlation_matrix.round(3),
        use_container_width=True
    )

    # ----------------------------------------
    # Heatmap
    # ----------------------------------------

    fig, ax = plt.subplots(
        figsize=(9, 6)
    )

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        vmin=-1,
        vmax=1,
        ax=ax
    )

    ax.set_title(
        "Pearson Correlation Heatmap"
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

    # ----------------------------------------
    # Correlation interpretation
    # ----------------------------------------

    def interpret_correlation(r):

        absolute_r = abs(r)

        if absolute_r >= 0.90:
            strength = "Very Strong"

        elif absolute_r >= 0.70:
            strength = "Strong"

        elif absolute_r >= 0.50:
            strength = "Moderate"

        elif absolute_r >= 0.30:
            strength = "Weak"

        else:
            strength = "Very Weak"

        if r > 0:
            direction = "Positive"

        elif r < 0:
            direction = "Negative"

        else:
            direction = "No"

        return f"{strength} {direction}"

    st.subheader(
        "Correlation Interpretation"
    )

    correlation_pairs = []

    for i in range(
        len(variables)
    ):

        for j in range(
            i + 1,
            len(variables)
        ):

            variable_1 = variables[i]
            variable_2 = variables[j]

            value = correlation_matrix.loc[
                variable_1,
                variable_2
            ]

            correlation_pairs.append({
                "Variable 1": variable_1,
                "Variable 2": variable_2,
                "Correlation": round(value, 3),
                "Interpretation":
                    interpret_correlation(value)
            })

    correlation_df = pd.DataFrame(
        correlation_pairs
    )

    st.dataframe(
        correlation_df,
        use_container_width=True
    )


# ============================================================
# TAB 4 — VISUALIZATIONS
# ============================================================

with tab4:

    st.subheader(
        "📊 Interactive Statistical Visualizations"
    )

    # ----------------------------------------
    # 1. Bar Chart
    # ----------------------------------------

    st.markdown(
        "### 1. Average Value by City"
    )

    city_mean = (
        filtered_df
        .groupby("City")[selected_variable]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        x=city_mean.index,
        y=city_mean.values,
        ax=ax
    )

    ax.set_title(
        f"Average {selected_variable} by City"
    )

    ax.set_xlabel("City")

    ax.set_ylabel(
        selected_variable
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

    # ----------------------------------------
    # 2. Box Plot
    # ----------------------------------------

    st.markdown(
        "### 2. Data Spread Across Cities"
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    sns.boxplot(
        data=filtered_df,
        x="City",
        y=selected_variable,
        ax=ax
    )

    ax.set_title(
        f"{selected_variable} Distribution Across Cities"
    )

    ax.set_xlabel("City")

    ax.set_ylabel(
        selected_variable
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

    # ----------------------------------------
    # 3. Scatter Plot
    # ----------------------------------------

    st.markdown(
        "### 3. Correlation Scatter Plot"
    )

    scatter_col1, scatter_col2 = st.columns(2)

    with scatter_col1:

        x_variable = st.selectbox(
            "X-axis Variable",
            variables,
            index=0
        )

    with scatter_col2:

        y_variable = st.selectbox(
            "Y-axis Variable",
            variables,
            index=1
        )

    if x_variable == y_variable:

        st.warning(
            "Please select two different variables."
        )

    else:

        correlation_value = (
            filtered_df[x_variable]
            .corr(
                filtered_df[y_variable]
            )
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.scatterplot(
            data=filtered_df,
            x=x_variable,
            y=y_variable,
            hue="City",
            s=70,
            ax=ax
        )

        ax.set_title(
            f"{x_variable} vs {y_variable}"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

        st.metric(
            "Pearson Correlation",
            f"{correlation_value:.3f}"
        )

        st.info(
            interpret_correlation(
                correlation_value
            )
        )

    st.markdown("### 4. Data Distribution (Density Plot)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.kdeplot(data=filtered_df, x=selected_variable, hue="City", fill=True, ax=ax, common_norm=False)
    ax.set_title(f"{selected_variable} Distribution/Density by City")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ============================================================
# TAB 5 — FINDINGS
# ============================================================

with tab5:

    st.subheader(
        "💡 Automated Project Findings"
    )

    # ----------------------------------------
    # Highest average city
    # ----------------------------------------

    city_means = (
        filtered_df
        .groupby("City")[selected_variable]
        .mean()
    )

    highest_mean_city = (
        city_means.idxmax()
    )

    highest_mean_value = (
        city_means.max()
    )

    # ----------------------------------------
    # Lowest average city
    # ----------------------------------------

    lowest_mean_city = (
        city_means.idxmin()
    )

    lowest_mean_value = (
        city_means.min()
    )

    # ----------------------------------------
    # Highest standard deviation
    # ----------------------------------------

    city_std = (
        filtered_df
        .groupby("City")[selected_variable]
        .std()
    )

    highest_spread_city = (
        city_std.idxmax()
    )

    highest_spread_value = (
        city_std.max()
    )

    # ----------------------------------------
    # Lowest standard deviation
    # ----------------------------------------

    lowest_spread_city = (
        city_std.idxmin()
    )

    lowest_spread_value = (
        city_std.min()
    )

    # ----------------------------------------
    # Display findings
    # ----------------------------------------

    st.markdown(
        f"""
        ### 📈 Average

        **{highest_mean_city}** has the highest
        average **{selected_variable}**
        with a value of **{highest_mean_value:.2f}**.

        **{lowest_mean_city}** has the lowest
        average **{selected_variable}**
        with a value of **{lowest_mean_value:.2f}**.
        """
    )

    st.markdown("---")

    st.markdown(
        f"""
        ### 📊 Data Spread

        **{highest_spread_city}** has the highest
        variation in **{selected_variable}**
        with a standard deviation of
        **{highest_spread_value:.2f}**.

        **{lowest_spread_city}** has the lowest
        variation with a standard deviation of
        **{lowest_spread_value:.2f}**.
        """
    )

    st.markdown("---")

    # ----------------------------------------
    # Strongest correlation
    # ----------------------------------------

    correlation_matrix = (
        filtered_df[variables]
        .corr()
    )

    correlation_pairs = (
        correlation_matrix
        .where(
            np.triu(
                np.ones(
                    correlation_matrix.shape
                ),
                k=1
            ).astype(bool)
        )
        .stack()
    )

    if len(correlation_pairs) > 0:

        strongest_pair = (
            correlation_pairs
            .abs()
            .idxmax()
        )

        strongest_value = (
            correlation_pairs[
                strongest_pair
            ]
        )

        st.markdown(
            f"""
            ### 🔗 Strongest Correlation

            The strongest relationship is between
            **{strongest_pair[0]}** and
            **{strongest_pair[1]}**.

            Pearson correlation coefficient:

            **r = {strongest_value:.3f}**

            This represents a
            **{interpret_correlation(strongest_value).lower()}**.
            """
        )

    st.markdown("---")

    # ----------------------------------------
    # Conclusion
    # ----------------------------------------

    st.subheader(
        "🎓 Project Conclusion"
    )

    st.write(
        """
        This project demonstrates how mathematical and
        statistical techniques can be applied to analyze
        data across multiple cities.

        Mean and median were used to understand central
        tendency, while variance and standard deviation
        were used to measure data spread.

        Covariance and Pearson correlation were used to
        identify relationships between environmental
        variables.

        Bar charts, box plots, scatter plots, and
        correlation heatmaps provide visual insights
        into the distribution and relationships within
        the dataset.

        The analysis demonstrates the practical use of
        Mathematical Foundation of Big Data concepts
        using Python and Streamlit.

        Correlation indicates association between
        variables and does not by itself establish
        causation.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "BDA Mini Project | Mathematical Foundation of Big Data | "
    "Python + Pandas + NumPy + Matplotlib + Seaborn + Streamlit"
)
