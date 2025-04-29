import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Streamlit page configuration
st.set_page_config(page_title="Institution Visual Analysis", layout="wide")
st.title("📊 Institution Visual Analysis")
st.markdown("Upload your Excel dataset to generate key insights.")

# Upload file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

# If a file is uploaded
if uploaded_file is not None:
    try:
        # Load dataset
        df = pd.read_excel(uploaded_file)

        # Show first few rows
        st.subheader("📋 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Create a 2x2 subplot
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("Institution Visual Analysis (4 Key Charts)", fontsize=18)
        plt.tight_layout(pad=5)

        # 1. Pie Chart: Trainer Qualification
        if 'Trainer Qualification' in df.columns:
            qual_counts = df['Trainer Qualification'].value_counts()
            axs[0, 0].pie(qual_counts.values, labels=qual_counts.index, autopct='%1.1f%%', startangle=140)
            axs[0, 0].set_title("Trainer Qualification Distribution")
        else:
            axs[0, 0].text(0.5, 0.5, "Missing 'Trainer Qualification' column", ha='center')

        # 2. Bar Chart: Institutions per State
        if 'State' in df.columns:
            state_counts = df['State'].value_counts()
            sns.barplot(x=state_counts.values, y=state_counts.index, ax=axs[0, 1])
            axs[0, 1].set_title("Institutions by State")
            axs[0, 1].set_xlabel("Count")
            axs[0, 1].set_ylabel("State")
        else:
            axs[0, 1].text(0.5, 0.5, "Missing 'State' column", ha='center')

        # 3. Column Chart: Top 10 Cities by Student Count
        if 'City' in df.columns and 'Total Number of Students' in df.columns:
            top_cities = df.groupby('City')['Total Number of Students'].sum().sort_values(ascending=False).head(10)
            sns.barplot(x=top_cities.index, y=top_cities.values, ax=axs[1, 0])
            axs[1, 0].set_title("Top 10 Cities by Total Students")
            axs[1, 0].set_xlabel("City")
            axs[1, 0].set_ylabel("Total Students")
            axs[1, 0].tick_params(axis='x', rotation=45)
        else:
            axs[1, 0].text(0.5, 0.5, "Missing 'City' or 'Total Number of Students' column", ha='center')

        # 4. Scatter Plot: Avg. Marks vs Total Students
        if 'Total Number of Students' in df.columns and 'Average Marks' in df.columns:
            sns.scatterplot(x='Total Number of Students', y='Average Marks', data=df, ax=axs[1, 1])
            axs[1, 1].set_title("Avg. Marks vs Total Students")
            axs[1, 1].set_xlabel("Total Number of Students")
            axs[1, 1].set_ylabel("Average Marks")
        else:
            axs[1, 1].text(0.5, 0.5, "Missing 'Total Number of Students' or 'Average Marks' column", ha='center')

        # Display the figure in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload an Excel file to begin analysis.")
