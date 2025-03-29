import pandas as pd

# Load CSV (ensure proper encoding)
df = pd.read_csv("JobsForLebanon.csv", encoding="utf-8")

print("Null Values: ", df.isnull().sum())
print("###################################")
print("")
print("duplicates: ", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("duplicates after drop: ", df.duplicated().sum())

# Fix encoding issues by replacing misinterpreted symbols with the actual bullet
df["Job Nature"] = df["Job Nature"].str.replace("â€¢", "•", regex=False)

# Split 'Job Nature' into 'Employment Type' and 'Experience Level' using the bullet separator
df[["Employment Type", "Experience Level"]] = df["Job Nature"].str.split(" • ", n=1, expand=True)

# Drop the original 'Job Nature' column
df.drop(columns=["Job Nature"], inplace=True)

# Save the cleaned dataset
df.to_csv("cleaned_jobs.csv", index=False, encoding="utf-8")
