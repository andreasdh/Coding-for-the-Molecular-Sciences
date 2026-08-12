from io import StringIO
import pandas as pd

csv_data = """sample_id,sample_type,concentration_uM,replicate,absorbance
blank_1,blank,0,1,0.010
blank_2,blank,0,2,0.011
std_2_1,standard,2,1,0.171
std_2_2,standard,2,2,0.169
std_6_3,standard,6,3,
unknown_1,unknown,,1,0.603
unknown_2,unknown,,2,0.606
"""

raw_data = pd.read_csv(StringIO(csv_data))

print("First rows:")
print(raw_data.head())
print("\nShape:", raw_data.shape)
print("\nData types:")
print(raw_data.dtypes)
print("\nMissing values:")
print(raw_data.isna().sum())
