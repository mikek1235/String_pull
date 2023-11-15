import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def plot_paw_coordinates(file_path):
    # Load the file
    df = pd.read_csv(file_path)

    # Finding the indices for 'Left Paw' and 'Right Paw' in the header row
    left_paw_index = df.columns.get_loc(df.iloc[0][df.iloc[0] == 'Left Paw'].index[0])
    right_paw_index = df.columns.get_loc(df.iloc[0][df.iloc[0] == 'Right Paw'].index[0])

    # The y-coordinate columns are immediately after these indices
    left_paw_y_col = df.columns[left_paw_index + 1]
    right_paw_y_col = df.columns[right_paw_index + 1]

    # Extracting the correct columns
    left_paw_y = pd.to_numeric(df[left_paw_y_col][2:], errors='coerce')
    right_paw_y = pd.to_numeric(df[right_paw_y_col][2:], errors='coerce')
    time_coords = df.index[2:]  # Time represented by row index

    # Print the first five rows of the analyzed data for inspection
    print(f"First 5 rows of analyzed data for {os.path.basename(file_path)}:")
    print(pd.DataFrame({'Time': time_coords[:5], 'Left Paw y': left_paw_y.head(5), 'Right Paw y': right_paw_y.head(5)}))
    print("\n")  # Adding a new line for better readability

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(time_coords, left_paw_y, label='Left Paw y')
    plt.plot(time_coords, right_paw_y, label='Right Paw y')
    plt.xlabel('Time Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'Left Paw y and Right Paw y Over Time for {os.path.basename(file_path)}')
    plt.legend()
    plt.show()

# Folder path containing the CSV files
folder_path = "C:\\Users\\mikek\\Desktop\\data"

# Finding all CSV files in the folder
file_paths = glob.glob(os.path.join(folder_path, '*.csv'))

# Plotting and printing data for each file in the folder
for file in file_paths:
    plot_paw_coordinates(file)
