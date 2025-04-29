# Import pandas library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import Image, display




# Load the data from the identified sheet
df = pd.read_excel("scrd-data.xlsx")

# Display the first few rows and column names to understand the data structure
print(df.head())

fig, axs = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Institution Visual Analysis (4 Key Charts)", fontsize=18)
plt.tight_layout(pad=5)

# 1. Pie Chart: Trainer Qualification
qual_counts = df['Trainer Qualification'].value_counts()
axs[0, 0].pie(qual_counts.values, labels=qual_counts.index, autopct='%1.1f%%', startangle=140)
axs[0, 0].set_title("Trainer Qualification Distribution")

# 2. Bar Chart: Institutions per State
state_counts = df['State'].value_counts()
sns.barplot(x=state_counts.values, y=state_counts.index, ax=axs[0, 1])
axs[0, 1].set_title("Institutions by State")
axs[0, 1].set_xlabel("Count")
axs[0, 1].set_ylabel("State")

# 3. Column Chart: Top 10 Cities by Student Count
top_cities = df.groupby('City')['Total Number of Students'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_cities.index, y=top_cities.values, ax=axs[1, 0])
axs[1, 0].set_title("Top 10 Cities by Total Students")
axs[1, 0].set_xlabel("City")
axs[1, 0].set_ylabel("Total Students")
axs[1, 0].tick_params(axis='x', rotation=45)

# 4. Scatter Plot: Avg. Marks vs Total Students
sns.scatterplot(x='Total Number of Students', y='Average Marks', data=df, ax=axs[1, 1])
axs[1, 1].set_title("Avg. Marks vs Total Students")
axs[1, 1].set_xlabel("Total Number of Students")
axs[1, 1].set_ylabel("Average Marks")

# Save and show
fig.savefig("Institution_Charts_1_Plots.png")
plt.show()