from io import StringIO
import pandas as pd

csv_data = """sample_id,sample_type,concentration_uM,replicate,absorbance
blank_1,blank,0,1,0.010
blank_2,blank,0,2,0.011
std_2_1,standard,2,1,0.171
std_2_2,standard,2,2,0.169
std_4_1,standard,4,1,0.329
std_4_2,standard,4,2,0.331
std_6_1,standard,6,1,0.489
std_6_2,standard,6,2,0.491
std_6_3,standard,6,3,
unknown_1,unknown,,1,0.603
unknown_2,unknown,,2,0.606
"""

raw_data = pd.read_csv(StringIO(csv_data))
clean_data = raw_data.dropna(subset=["absorbance"]).copy()
standards = clean_data[clean_data["sample_type"] == "standard"]
summary = standards.groupby("concentration_uM")["absorbance"].agg(["count", "mean", "std", "min", "max"])

print("Missing values in the raw data:")
print(raw_data.isna().sum())
print("\nSummary of calibration standards:")
print(summary)
