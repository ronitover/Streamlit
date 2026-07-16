import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("CSV Viewer & Visualizer")
st.write("Upload a CSV file and choose visualizations (correlation heatmap, histograms, scatter, etc.).")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("Data Preview")
        if st.checkbox("Show raw data"):
            st.dataframe(df)

        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        all_cols = df.columns.tolist()

        viz = st.selectbox(
            "Choose visualization",
            [
                "Correlation Heatmap",
                "Missing Values Heatmap",
                "Histogram",
                "Boxplot",
                "Scatter Plot",
                "Pairplot (small datasets)",
            ],
        )

        if viz == "Correlation Heatmap":
            if len(numeric_cols) < 2:
                st.warning("Need at least two numeric columns for correlation.")
            else:
                corr = df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

        elif viz == "Missing Values Heatmap":
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.isnull(), cbar=False, cmap="viridis", ax=ax)
            ax.set_ylabel("Rows")
            st.pyplot(fig)

        elif viz == "Histogram":
            if not numeric_cols:
                st.warning("No numeric columns available for histogram.")
            else:
                col = st.selectbox("Select column", numeric_cols)
                bins = st.slider("Bins", 5, 200, 30)
                fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}")
                st.plotly_chart(fig, use_container_width=True)

        elif viz == "Boxplot":
            if not numeric_cols:
                st.warning("No numeric columns available for boxplot.")
            else:
                col = st.selectbox("Select column for boxplot", numeric_cols)
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.boxplot(x=df[col], ax=ax)
                ax.set_title(f"Boxplot of {col}")
                st.pyplot(fig)

        elif viz == "Scatter Plot":
            if len(numeric_cols) < 2:
                st.warning("Need at least two numeric columns for scatter plot.")
            else:
                x_col = st.selectbox("X axis", numeric_cols, index=0)
                y_col = st.selectbox("Y axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                color_col = st.selectbox("Color (optional)", [None] + all_cols)
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)

        elif viz == "Pairplot (small datasets)":
            if not numeric_cols:
                st.warning("No numeric columns available for pairplot.")
            else:
                max_points = st.slider("Max rows to sample for pairplot", 100, 2000, 500)
                sample = df[numeric_cols].dropna().sample(n=min(len(df), max_points))
                # seaborn PairGrid returns a FacetGrid with .fig
                grid = sns.pairplot(sample)
                st.pyplot(grid.fig)

        st.info("Requires: pandas, seaborn, matplotlib, plotly. Install with `pip install pandas seaborn matplotlib plotly` if missing.")

    except Exception as error:
        st.error(f"Could not read or visualize the CSV file: {error}")