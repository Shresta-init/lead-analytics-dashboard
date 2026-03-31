import pandas as pd

# Load datasets
leads = pd.read_csv("leads.csv")
funnel = pd.read_csv("funnel.csv")
cost = pd.read_csv("marketing_cost.csv")

# Show data
print("Leads Data:")
print(leads)

print("\nFunnel Data:")
print(funnel)

print("\nCost Data:")
print(cost)

# Merge datasets
df = leads.merge(funnel, on="Lead_ID")

print("\nMerged Data:")
print(df)

# Leads per channel
leads_count = df.groupby("Lead_Source")["Lead_ID"].count()
print("\nLeads per Channel:")
print(leads_count)

# Enrollments per channel
enrollments = df[df["Enrolled"]=="Yes"].groupby("Lead_Source")["Lead_ID"].count()
print("\nEnrollments per Channel:")
print(enrollments)

# Conversion rate
conversion = (enrollments / leads_count) * 100
print("\nConversion Rate (%):")
print(conversion)

# Combine leads & enrollments
channel_stats = pd.DataFrame({
    "Leads": leads_count,
    "Enrollments": enrollments
}).fillna(0)

print("\nChannel Stats:")
print(channel_stats)

channel_stats = channel_stats.merge(cost, left_index=True, right_on="Channel")

print("\nAfter Adding Cost:")
print(channel_stats)

channel_stats["Cost_per_Enrollment"] = channel_stats["Cost"] / channel_stats["Enrollments"]

print("\nFinal Analysis:")
print(channel_stats)

import matplotlib.pyplot as plt

leads_count.plot(kind="bar", title="Leads by Channel")
plt.ylabel("Number of Leads")
plt.show()

conversion.plot(kind="bar", title="Conversion Rate (%)")
plt.ylabel("Percentage")
plt.show()

channel_stats.set_index("Channel")["Cost_per_Enrollment"].plot(
    kind="bar", title="Cost per Enrollment"
)
plt.ylabel("Cost")
plt.show()

print("\n--- INSIGHTS ---")

print("1. LinkedIn has higher conversion rate compared to other channels.")
print("2. Instagram generates more leads but lower conversion efficiency.")
print("3. Some channels have high cost per enrollment, indicating poor ROI.")
print("4. Channels with low cost per enrollment should receive more marketing budget.")

print("\n=== FINAL CHANNEL PERFORMANCE ===")
print(channel_stats[["Channel", "Leads", "Enrollments", "Cost", "Cost_per_Enrollment"]])

# Sorting
channel_stats = channel_stats.sort_values(by="Cost_per_Enrollment")

print("\n=== BEST CHANNELS (LOWEST COST FIRST) ===")
print(channel_stats)

# Smart insights
best_channel = channel_stats.iloc[0]["Channel"]
worst_channel = channel_stats.iloc[-1]["Channel"]

print("\n--- SMART INSIGHTS ---")
print(f"Best channel based on cost efficiency: {best_channel}")
print(f"Worst channel based on cost efficiency: {worst_channel}")

print(f"Recommendation: Increase budget on {best_channel} and reduce spending on {worst_channel}")

channel_stats.set_index("Channel")["Cost_per_Enrollment"].plot(kind="bar", title="Cost Efficiency by Channel")
plt.ylabel("Cost per Enrollment")
plt.xticks(rotation=45)
plt.show()