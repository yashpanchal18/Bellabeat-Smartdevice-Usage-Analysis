import pandas as pd

# Define base paths for both months (adjust paths as needed)
base_path_month1 = r"mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/"
base_path_month2 = r"mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/"
base_paths = [base_path_month1, base_path_month2]

# Helper function: load and concatenate CSV files from both months
def load_and_concat(filename):
    dfs = []
    for path in base_paths:
        df = pd.read_csv(path + filename)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# -----------------------
# Load Datasets
# -----------------------
daily_activity = load_and_concat("dailyActivity_merged.csv")
heart_rate = load_and_concat("heartrate_seconds_merged.csv")
minute_sleep = load_and_concat("minuteSleep_merged.csv")
weight_log = load_and_concat("weightLogInfo_merged.csv")

# -----------------------
# Cleaning and Formatting
# -----------------------

# --- Daily Activity ---
# dailyActivity_merged.csv contains only date values in ActivityDate.
daily_activity["ActivityDate"] = pd.to_datetime(daily_activity["ActivityDate"], format='%m/%d/%Y')
# Drop rows with any missing values (for activity)
daily_activity.dropna(inplace=True)

# --- Heart Rate ---
# The "Time" column contains both date and time (e.g., "4/5/2016 11:59:59 PM").
heart_rate["Time"] = pd.to_datetime(heart_rate["Time"], format='%m/%d/%Y %I:%M:%S %p')
# Create separate Date and TimeOnly columns
heart_rate["Date"] = heart_rate["Time"].dt.date
heart_rate["TimeOnly"] = heart_rate["Time"].dt.time
# Drop rows with missing values
heart_rate.dropna(inplace=True)

# --- Minute Sleep ---
# The "date" column contains both date and time.
minute_sleep["date"] = pd.to_datetime(minute_sleep["date"], format='%m/%d/%Y %I:%M:%S %p')
# Create separate Date and TimeOnly columns for sleep data
minute_sleep["Date"] = minute_sleep["date"].dt.date
minute_sleep["TimeOnly"] = minute_sleep["date"].dt.time
# Drop rows with missing values
minute_sleep.dropna(inplace=True)

# --- Weight Log ---
# The "Date" column in weightLogInfo may have both date and time.
weight_log["Date"] = pd.to_datetime(weight_log["Date"], format='%m/%d/%Y %I:%M:%S %p')
# Create separate Date and TimeOnly columns for weight data
weight_log["DateOnly"] = weight_log["Date"].dt.date
weight_log["TimeOnly"] = weight_log["Date"].dt.time
# Drop the "Fat" column as specified (do not drop rows for missing values in weight)
if "Fat" in weight_log.columns:
    weight_log.drop(columns=["Fat"], inplace=True)
# (Do not drop rows with missing values for weight_log)

# -----------------------
# Create Star Schema Tables
# -----------------------

# -- Dimension Tables --

# DimUsers: Unique user IDs (using daily_activity as the source)
dim_users = pd.DataFrame({"UserID": daily_activity["Id"].unique()})
dim_users.to_csv("DimUsers.csv", index=False)

# DimTime: Calendar table covering the entire date range from daily_activity
dim_time = pd.DataFrame({"Date": pd.date_range(start=daily_activity["ActivityDate"].min(),
                                               end=daily_activity["ActivityDate"].max())})
dim_time["Day"] = dim_time["Date"].dt.day
dim_time["Month"] = dim_time["Date"].dt.month
dim_time["Weekday"] = dim_time["Date"].dt.day_name()
dim_time.to_csv("DimTime.csv", index=False)

# -- Fact Tables --

# FactActivity: Using dailyActivity data (we select key columns)
fact_activity = daily_activity[["Id", "ActivityDate", "TotalSteps", "TotalDistance", "Calories",
                                  "VeryActiveMinutes", "FairlyActiveMinutes", "LightlyActiveMinutes", "SedentaryMinutes"]].copy()
fact_activity.rename(columns={"Id": "UserID", "ActivityDate": "Date"}, inplace=True)
fact_activity.to_csv("FactActivity.csv", index=False)

# FactHeartRate: Aggregate heart rate data to hourly averages and split Date and Time
heart_rate["Hour"] = heart_rate["Time"].dt.floor("H")
fact_heart_rate = heart_rate.groupby(["Id", "Hour"])["Value"].mean().reset_index()
fact_heart_rate.rename(columns={"Id": "UserID", "Hour": "DateTime", "Value": "AvgHeartRate"}, inplace=True)
# Split the DateTime column into separate Date and TimeOnly columns
fact_heart_rate["Date"] = fact_heart_rate["DateTime"].dt.date
fact_heart_rate["TimeOnly"] = fact_heart_rate["DateTime"].dt.time
# Optionally, drop the combined DateTime column if not needed
fact_heart_rate = fact_heart_rate[["UserID", "Date", "TimeOnly", "AvgHeartRate"]]
fact_heart_rate.to_csv("FactHeartRate.csv", index=False)

# FactSleep: Aggregate minute-level sleep data to daily total sleep per user
fact_sleep = minute_sleep.groupby(["Id", minute_sleep["Date"]]).agg({"value": "sum"}).reset_index()
fact_sleep.rename(columns={"Id": "UserID", "Date": "Date", "value": "TotalSleepMinutes"}, inplace=True)
# Convert Date column to datetime
fact_sleep["Date"] = pd.to_datetime(fact_sleep["Date"])
fact_sleep.to_csv("FactSleep.csv", index=False)

# FactWeight: Process weight data and split Date into DateOnly and TimeOnly columns
fact_weight = weight_log[["Id", "Date", "WeightKg", "BMI"]].copy()
fact_weight.rename(columns={"Id": "UserID"}, inplace=True)
# Split the Date column
fact_weight["DateOnly"] = fact_weight["Date"].dt.date
fact_weight["TimeOnly"] = fact_weight["Date"].dt.time
# Rearranging columns for clarity
fact_weight = fact_weight[["UserID", "DateOnly", "TimeOnly", "WeightKg", "BMI"]]
fact_weight.to_csv("FactWeight.csv", index=False)

print("✅ Data Cleaning and Star Schema CSV files created for both months!")
