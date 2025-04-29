import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Institution Visual Analysis", layout="wide")
st.title("📊 Institution Visual Analysis")
st.markdown("Upload your Excel dataset to generate key insights.")

# Upload file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("📋 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Chart layout in 2 rows and 3 columns
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        row2_col1, row2_col2, row2_col3 = st.columns(3)

        # 1. Pie Chart: Trainer Qualification
        with row1_col1:
            st.markdown("**Trainer Qualification Distribution**")
            if 'Trainer Qualification' in df.columns:
                qual_counts = df['Trainer Qualification'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(qual_counts.values, labels=qual_counts.index, autopct='%1.1f%%', startangle=140)
                ax.set_title("Trainer Qualification")
                st.pyplot(fig)
                st.caption("Percentage distribution of trainer qualifications.")
            else:
                st.warning("Missing 'Trainer Qualification' column.")

        # 2. Bar Chart: Institutions per State
        with row1_col2:
            st.markdown("**Institutions by State**")
            if 'State' in df.columns:
                state_counts = df['State'].value_counts()
                fig, ax = plt.subplots()
                sns.barplot(x=state_counts.values, y=state_counts.index, ax=ax)
                ax.set_xlabel("Count")
                ax.set_ylabel("State")
                ax.set_title("Institutions by State")
                st.pyplot(fig)
                st.caption("Shows the number of institutions in each state.")
            else:
                st.warning("Missing 'State' column.")

        # 3. Bar Chart: Top 10 Cities by Student Count
        with row1_col3:
            st.markdown("**Top 10 Cities by Total Students**")
            if 'City' in df.columns and 'Total Number of Students' in df.columns:
                top_cities = df.groupby('City')['Total Number of Students'].sum().sort_values(ascending=False).head(10)
                fig, ax = plt.subplots()
                sns.barplot(x=top_cities.index, y=top_cities.values, ax=ax)
                ax.set_title("Top 10 Cities")
                ax.set_xlabel("City")
                ax.set_ylabel("Total Students")
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
                st.caption("Cities with the highest student enrollment.")
            else:
                st.warning("Missing 'City' or 'Total Number of Students' column.")

        # 4. Line Plot: Avg. of Average Marks (Top 10 Institutions)
        with row2_col1:
            st.markdown("**Top 10 Institutions by Avg. Marks**")
            if 'Name of School/College' in df.columns and 'Average Marks' in df.columns:
                avg_marks = df.groupby('Name of School/College')['Average Marks'].mean().sort_values(ascending=False).head(10)
                fig, ax = plt.subplots()
                sns.lineplot(x=avg_marks.index, y=avg_marks.values, marker='o', ax=ax)
                ax.set_title("Top 10 Institutions")
                ax.set_xlabel("Institution")
                ax.set_ylabel("Avg. Marks")
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
                st.caption("Institutions with highest average marks.")
            else:
                st.warning("Missing 'Name of School/College' or 'Average Marks' column.")

        # 5. Donut Chart: School vs College
        with row2_col2:
            st.markdown("**School vs College Distribution**")
            if 'School/College' in df.columns:
                counts = df['School/College'].value_counts()
                fig, ax = plt.subplots()
                wedges, texts, autotexts = ax.pie(
                    counts.values, labels=counts.index, autopct='%1.1f%%',
                    startangle=90, wedgeprops=dict(width=0.4)
                )
                ax.add_artist(plt.Circle((0, 0), 0.70, fc='white'))
                ax.set_title("School vs College")
                st.pyplot(fig)
                st.caption("Proportion of Schools and Colleges.")
            else:
                st.warning("Missing 'School/College' column.")

        # 6. Funnel Chart: Top 5 States by School/College Count
        with row2_col3:
            st.markdown("**Top 5 States by Institution Count (Funnel)**")
            if 'State' in df.columns and 'School/College' in df.columns:
                funnel_data = df.groupby(['State', 'School/College']).size().reset_index(name='Count')
                top_states = funnel_data.groupby('State')['Count'].sum().sort_values(ascending=False).head(5).index
                filtered = funnel_data[funnel_data['State'].isin(top_states)]
                filtered['Label'] = filtered['State'] + " - " + filtered['School/College']
                funnel_fig = px.funnel(
                    filtered, x="Count", y="Label",
                    title="Top 5 States by Institution Type",
                    color="School/College"
                )
                st.plotly_chart(funnel_fig, use_container_width=True)
                st.caption("Visual breakdown of top 5 states by School/College count.")
            else:
                st.warning("Missing 'State' or 'School/College' column.")

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload an Excel file to begin analysis.")
