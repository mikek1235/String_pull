% Specify the path to your CSV file
filename = 'C:\Users\Mkarkus\Desktop\sample\July13.23_5_HeidiOwen_Raw_1.MP4DLC_resnet50_String_model_2Jul3shuffle1_101500_filtered.csv'; 

% Define the number of header lines
numHeaderLines = 3; % Adjust this based on your file

% Read the header lines
opts = detectImportOptions(filename, 'NumHeaderLines', 0);
opts.DataLines = [1, numHeaderLines];  % Read only the header lines
header = readcell(filename, opts);

% Now read the actual data, skipping the header rows
data = readmatrix(filename, 'NumHeaderLines', numHeaderLines);

% Extract X/Y position values using the correct column indices
% Adjust these indices based on your actual file structure
Lx_pos = data(:,5);
Ly_pos = data(:,6);
Rx_pos = data(:,8);
Ry_pos = data(:,9);

% Frames, as a measure of time
Frames = data(:,1);

% Define your window size for smoothing
windowSize = 4; % example value, adjust as needed

% Smooth the data
smoothLeftPawY = smoothdata(Ly_pos, 'movmean', windowSize);
smoothRightPawY = smoothdata(Ry_pos, 'movmean', windowSize);

% Replace the original Y position data with the smoothed data
data(:,6) = smoothLeftPawY;
data(:,9) = smoothRightPawY;

% Create a new filename for the smoothed data
[path, name, ~] = fileparts(filename);
newFileName = fullfile(path, [name '_smoothened.csv']);

% Write the header and data to the new file
fid = fopen(newFileName, 'w');

% Write header lines with handling missing data
for i = 1:numHeaderLines
    for j = 1:size(header,2)
        if ismissing(header{i,j})
            fprintf(fid, '%s', ''); % Write an empty string for missing entries
        else
            fprintf(fid, '%s', header{i,j});
        end
        if j < size(header,2)
            fprintf(fid, ','); % Add comma between entries
        end
    end
    fprintf(fid, '\n'); % New line at the end of each header row
end

% Write data
for i = 1:size(data,1)
    fprintf(fid, '%g,', data(i,1:end-1));
    fprintf(fid, '%g\n', data(i,end));
end

fclose(fid);
disp(['Smoothed data written to ' newFileName]);

% Plotting the results
figure;

% Plot Left Paw Y - Original and Smoothed
subplot(3,1,1);
plot(Ly_pos, 'b');
hold on;
plot(smoothLeftPawY, 'r');
title('Left Paw Y - Original and Smoothed');
legend('Original', 'Smoothed');
hold off;

% Plot Right Paw Y - Original and Smoothed
subplot(3,1,2);
plot(Ry_pos, 'b');
hold on;
plot(smoothRightPawY, 'r');
title('Right Paw Y - Original and Smoothed');
legend('Original', 'Smoothed');
hold off;

% Overlay of Smoothed Left and Right Paw Y
subplot(3,1,3);
plot(smoothLeftPawY, 'r');
hold on;
plot(smoothRightPawY, 'g');
title('Overlay of Smoothed Left and Right Paw Y');
legend('Smoothed Left Paw Y', 'Smoothed Right Paw Y');
hold off;

% Correlation calculations
R = corrcoef(Ly_pos, Ry_pos);
disp('Raw Left and Right y value correlation:');
disp(R);

R2 = corrcoef(smoothLeftPawY, smoothRightPawY);
disp('Smoothed Left and Right y value correlation:');
disp(R2);
