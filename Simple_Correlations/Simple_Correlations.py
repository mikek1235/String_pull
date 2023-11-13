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
        data_trimmed = data_cleaned.iloc[10:-10]
        # Extract the Lhand and Rhand y values
        lhand_y = data_trimmed.iloc[:, 1]  # Assuming the Lhand y values are in the second column
        rhand_y = data_trimmed.iloc[:, 4]  # Assuming the Rhand y values are in the fifth column
        # Calculate the correlation
        correlation = lhand_y.corr(rhand_y)
        return correlation
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def analyze_spreadsheets(folder_path):
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    correlations = {'File Path': [], 'Filtered': [], 'Unfiltered': []}
    
    for file_path in file_paths:
        correlation = calculate_correlation(file_path)
        correlations['File Path'].append(file_path)
        if "filtered" in file_path.lower():
            correlations['Filtered'].append(correlation)
            correlations['Unfiltered'].append(None)
        else:
            correlations['Unfiltered'].append(correlation)
            correlations['Filtered'].append(None)

    # Save correlations to a CSV file
    correlation_data = pd.DataFrame(correlations)
    correlation_data.to_csv('correlations.csv', index=False)
    
    # Calculate the mean correlations and save to a CSV file
    mean_correlation_data = pd.DataFrame({
        'Mean Filtered Correlation': [pd.Series(correlations['Filtered']).mean()],
        'Mean Unfiltered Correlation': [pd.Series(correlations['Unfiltered']).mean()]
    })
    mean_correlation_data.to_csv('mean_correlation.csv', index=False)
    
    return correlation_data, mean_correlation_data

# Example usage:
# Replace 'path_to_directory_with_csv_files' with the actual path to the directory containing your CSV files
folder_path = 'C:\\Users\\Mkarkus\\Desktop\\Nov data heidi'
correlation_data, mean_correlation_data = analyze_spreadsheets(folder_path)

print("Correlation Data:\n", correlation_data)
print("\nMean Correlation Data:\n", mean_correlation_data)
