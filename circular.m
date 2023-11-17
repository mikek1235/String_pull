% Read data from CSV
filename = 'C:\Users\mikek\Desktop\July13.23_5_HeidiOwen_Raw_1.MP4DLC_resnet50_String_model_2Jul3shuffle1_101500.csv';
data = readtable(filename);

% Extract x and y coordinates from the 2nd and 3rd columns
x = data{:, 2}; % Assuming x coordinates are in the 2nd column
y = data{:, 3}; % Assuming y coordinates are in the 3rd column

% Plotting the raw trajectory on a Cartesian plot
figure;
plot(x, y, 'b-', 'LineWidth', 1.5);
title('Raw Trajectory');
xlabel('X Coordinate');
ylabel('Y Coordinate');
axis equal;
grid on;

% Calculate angles of movement
dx = diff(x); % Change in x
dy = diff(y); % Change in y
angles = atan2(dy, dx);

% Convert and align angles
angles = mod(angles, 2*pi);
angles = [angles; NaN]; % Append NaN
angles = angles(~isnan(angles)); % Remove NaN values

% Polar plot of movement direction
figure;
polarhistogram(angles, 36, 'Normalization', 'probability');
title('Polar Histogram of Movement Directions');

% Circular Statistics
sum_sin = sum(sin(angles));
sum_cos = sum(cos(angles));
mean_direction = atan2(sum_sin, sum_cos);
mean_direction = mod(mean_direction, 2*pi);
R = sqrt(sum_sin^2 + sum_cos^2) / length(angles);
circular_variance = 1 - R;

% Display the results
fprintf('Mean Direction: %f radians\n', mean_direction);
fprintf('Circular Variance: %f\n', circular_variance);
