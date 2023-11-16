import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from matplotlib.lines import Line2D

def find_increasing_decreasing_segments(y_data, merge_threshold=10):
    increasing_segments = []
    decreasing_segments = []

    if len(y_data) < 2:
        return increasing_segments, decreasing_segments

    current_segment = [(0, y_data.iloc[0])]

    for i in range(1, len(y_data)):
        if y_data.iloc[i] > y_data.iloc[i - 1]:
            current_segment.append((i, y_data.iloc[i]))
        else:
            if len(current_segment) > 1:
                increasing_segments.append(current_segment)
            current_segment = [(i, y_data.iloc[i])]

    if len(current_segment) > 1:
        increasing_segments.append(current_segment)

    current_segment = [(0, y_data.iloc[0])]

    for i in range(1, len(y_data)):
        if y_data.iloc[i] < y_data.iloc[i - 1]:
            current_segment.append((i, y_data.iloc[i]))
        else:
            if len(current_segment) > 1:
                decreasing_segments.append(current_segment)
            current_segment = [(i, y_data.iloc[i])]

    if len(current_segment) > 1:
        decreasing_segments.append(current_segment)

    # Merge segments that are within merge_threshold frames of each other
    increasing_segments = merge_segments(increasing_segments, merge_threshold)
    decreasing_segments = merge_segments(decreasing_segments, merge_threshold)

    return increasing_segments, decreasing_segments

def merge_segments(segments, merge_threshold):
    merged_segments = []
    if len(segments) > 0:
        current_segment = [segments[0]]
        for i in range(1, len(segments)):
            if segments[i][0][0] - current_segment[-1][-1][0] <= merge_threshold:
                current_segment.append(segments[i])
            else:
                merged_segments.append([item for sublist in current_segment for item in sublist])
                current_segment = [segments[i]]
        merged_segments.append([item for sublist in current_segment for item in sublist])
    return merged_segments

def segment_length(segment):
    return segment[-1][0] - segment[0][0] + 1

def calculate_and_print_segment_lengths(y_data, min_segment_length, hand_name):
    increasing_segments, decreasing_segments = find_increasing_decreasing_segments(y_data)
    
    # Calculate mean length per segment
    increasing_lengths = [segment_length(segment) for segment in increasing_segments]
    decreasing_lengths = [segment_length(segment) for segment in decreasing_segments]
    mean_increasing_length = sum(increasing_lengths) / len(increasing_lengths)
    mean_decreasing_length = sum(decreasing_lengths) / len(decreasing_lengths)
    
    # Print significant segment lengths for the hand
    print(f"Significant Segment Lengths for {hand_name} Paw:")
    for segment in increasing_segments:
        length = segment_length(segment)
        if length >= min_segment_length * mean_increasing_length:
            print(f"Increasing Length: {length}")
    for segment in decreasing_segments:
        length = segment_length(segment)
        if length >= min_segment_length * mean_decreasing_length:
            print(f"Decreasing Length: {length}")

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

    # Reset the index of y_data to ensure it starts from 0
    left_paw_y = left_paw_y.reset_index(drop=True)
    right_paw_y = right_paw_y.reset_index(drop=True)

    # Calculate mean increasing length for left paw
    increasing_segments_left, decreasing_segments_left = find_increasing_decreasing_segments(left_paw_y, merge_threshold=10)
    increasing_lengths_left = [segment_length(segment) for segment in increasing_segments_left]
    mean_increasing_length_left = sum(increasing_lengths_left) / len(increasing_lengths_left)

    # Calculate mean increasing length for right paw
    increasing_segments_right, decreasing_segments_right = find_increasing_decreasing_segments(right_paw_y, merge_threshold=10)
    increasing_lengths_right = [segment_length(segment) for segment in increasing_segments_right]
    mean_increasing_length_right = sum(increasing_lengths_right) / len(increasing_lengths_right)

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot left paw y
    plt.plot(time_coords, left_paw_y, color='lightcoral', alpha=0.7)

    # Highlight significant increasing segments in blue
    for segment in increasing_segments_left:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_left:
            plt.plot([time_coords[i] for i in indices], values, color='blue', alpha=0.8,)

    # Highlight significant decreasing segments in red
    for segment in decreasing_segments_left:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_left:
            plt.plot([time_coords[i] for i in indices], values, color='red', alpha=0.8)

    plt.xlabel('Time Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'{os.path.basename(file_path)} - Left Paw y')
    # Create custom legend handles and labels for increasing and decreasing segments
    legend_handles_left = [Line2D([0], [0], color='blue', alpha=0.8), Line2D([0], [0], color='red', alpha=0.8)]
    legend_labels_left = ['Increasing', 'Decreasing']

    # Add a single legend entry for left paw with custom handles and labels
    plt.legend(legend_handles_left, legend_labels_left)
    plt.show()


    plt.figure(figsize=(12, 6))

    # Plot right paw y
    plt.plot(time_coords, right_paw_y, color='gold', alpha=0.7)

    # Highlight significant increasing segments in purple
    for segment in increasing_segments_right:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_right:
            plt.plot([time_coords[i] for i in indices], values, color='purple', alpha=0.8)

    # Highlight significant decreasing segments in green
    for segment in decreasing_segments_right:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_right:
            plt.plot([time_coords[i] for i in indices], values, color='green', alpha=0.8)

    plt.xlabel('Time Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'{os.path.basename(file_path)} - Right Paw y')
    # Create custom legend handles and labels for increasing and decreasing segments
    legend_handles_right = [Line2D([0], [0], color='purple', alpha=0.8), Line2D([0], [0], color='green', alpha=0.8)]
    legend_labels_right = ['Increasing', 'Decreasing']

    # Add a single legend entry for right paw with custom handles and labels
    plt.legend(legend_handles_right, legend_labels_right)
    plt.show()

    # Overlay both plots
    plt.figure(figsize=(12, 6))

    # Plot left paw y
    plt.plot(time_coords, left_paw_y, color='lightcoral', alpha=0.7)

    ###########overlay

    # Highlight significant increasing segments in blue
    for segment in increasing_segments_left:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_left:
            plt.plot([time_coords[i] for i in indices], values, color='blue', alpha=0.8)

    # Highlight significant decreasing segments in red
    for segment in decreasing_segments_left:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_left:
            plt.plot([time_coords[i] for i in indices], values, color='red', alpha=0.8)

    # Plot right paw y
    plt.plot(time_coords, right_paw_y, color='gold', alpha=0.7)

    # Highlight significant increasing segments in purple
    for segment in increasing_segments_right:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_right:
            plt.plot([time_coords[i] for i in indices], values, color='purple', alpha=0.8)

    # Highlight significant decreasing segments in green
    for segment in decreasing_segments_right:
        indices, values = zip(*segment)
        length = segment_length(segment)
        if length >= 0.5 * mean_increasing_length_right:
            plt.plot([time_coords[i] for i in indices], values, color='green', alpha=0.8)

        # Create custom legend handles and labels
    legend_handles = [
        Line2D([0], [0], color='blue', alpha=0.8),
        Line2D([0], [0], color='red', alpha=0.8),
        Line2D([0], [0], color='purple', alpha=0.8),
        Line2D([0], [0], color='green', alpha=0.8)
    ]

    legend_labels = [
        'Significant Increasing (Left)',
        'Significant Decreasing (Left)',
        'Significant Increasing (Right)',
        'Significant Decreasing (Right)'
    ]
        # Create the custom legend
    plt.legend(legend_handles, legend_labels)

    plt.xlabel('Time Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'{os.path.basename(file_path)} - Overlay')
    
    plt.show()

    ###########overlay

# Folder path containing the CSV files
folder_path = "c:\\Users\\Mkarkus\\Desktop\\sample"

# Finding all CSV files in the folder
file_paths = glob.glob(os.path.join(folder_path, '*.csv'))

# Plotting and printing data for each file in the folder
for file in file_paths:
    plot_paw_coordinates(file)
