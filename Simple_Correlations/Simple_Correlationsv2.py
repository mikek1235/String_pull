import pandas as pd
import os

def clean_data(df):
    # Remove the first two rows containing metadata
    df_cleaned = df.iloc[2:]
    # Convert all columns to numeric, ignoring errors for columns that are non-numeric
    df_cleaned = df_cleaned.apply(pd.to_numeric, errors='ignore')
    return df_cleaned

def calculate_correlation(file_path):
    try:
        # Load the data
        data = pd.read_csv(file_path)
        # Clean the data
        data_cleaned = clean_data(data)
        # Trim the data
        data_trimmed = data_cleaned.iloc[:]
        # Extract the Lhand and Rhand y values
        lhand_y = data_trimmed.iloc[:, 5]  # Adjust the column index if necessary
        rhand_y = data_trimmed.iloc[:, 8]  # Adjust the column index if necessary
        # Calculate the correlation
        correlation = lhand_y.corr(rhand_y)
        return correlation, lhand_y.head(5), rhand_y.head(5)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None, None

def analyze_spreadsheets(folder_path):
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    correlations = {'File Path': [], 'Correlation': [], 'Lhand_Y_Values': [], 'Rhand_Y_Values': []}
    
    for file_path in file_paths:
        correlation, lhand_y_values, rhand_y_values = calculate_correlation(file_path)
        correlations['File Path'].append(file_path)
        correlations['Correlation'].append(correlation)
        correlations['Lhand_Y_Values'].append(lhand_y_values.tolist())  # Convert to list for better CSV representation
        correlations['Rhand_Y_Values'].append(rhand_y_values.tolist())  # Convert to list for better CSV representation

    # Save correlations to a CSV file
    correlation_data = pd.DataFrame(correlations)
    correlation_data.to_csv('correlations.csv', index=False)
    
    return correlation_data

# Example usage:
# Replace 'path_to_directory_with_csv_files' with the actual path to the directory containing your CSV files
folder_path = 'C:\\Users\\Mkarkus\\Desktop\\data'
correlation_data = analyze_spreadsheets(folder_path)

# Print the first 5 datasets for lhand_y and rhand_y values along with the correlation
for i in range(min(5, len(correlation_data))):
    print(f"File: {correlation_data['File Path'][i]}")
    print(f"Correlation: {correlation_data['Correlation'][i]}")
    print("Lhand Y Values:\n", correlation_data['Lhand_Y_Values'][i])
    print("Rhand Y Values:\n", correlation_data['Rhand_Y_Values'][i])
    print()
