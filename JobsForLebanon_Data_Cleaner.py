import pandas as pd

# Load raw scraped data
df = pd.read_csv("JobsForLebanon.csv", encoding="utf-8")

# Fix encoding issues in "Job Nature"
df["Job Nature"] = df["Job Nature"].str.replace("â€¢", "•", regex=False)

# Split 'Job Nature' into 'Employment Type' and 'Experience Level' using "•" separator
df[["Employment Type", "Experience Level"]] = df["Job Nature"].str.split(" • ", n=1, expand=True)

# Drop the original "Job Nature" column
df.drop(columns=["Job Nature"], inplace=True)

# Drop duplicates based on "Job Title" and "Job Link" (keeping the latest by date)
df.drop_duplicates(subset=["Job Title", "Job Link"], keep="last", inplace=True)

# Save the cleaned dataset (overwrite)
df.to_csv("cleaned_jobs.csv", index=False, encoding="utf-8")

print("Data Cleaning Complete. Cleaned data saved to 'cleaned_jobs.csv'.")
