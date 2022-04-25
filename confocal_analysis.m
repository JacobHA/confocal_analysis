%% Initializations

XY_SCALE = 0.176; % um/pixel
Z_SCALE = 2.5; % um/pixel

disp("Relative voxel scale:");
disp(XY_SCALE / Z_SCALE);

% Working with a propietary filetype: .lsm 
% To access it, install:
% https://www.openmicroscopy.org/bioformats/downloads/ 
% And add it to the MATLAB path (HOME -> Set Path)

filename = "C:\Users\jacob\OneDrive\Desktop\Cancer Biophysics\Assignment 4\CONFOCAL phalloidinandDAPI.lsm";

data = bfopen(char(filename));

seriesCount = size(data, 1);
series1 = data{1, 1};
metadataList = data{1, 2};

num_z_slices = size(series1, 1);
PHALLOIDIN = series1(2:2:end,1);
DAPI = series1(1:2:end,1);

% 
DAPI_IMG = [];
for k = 1 : length(DAPI)
    dapi_slice = imfill(cell2mat(DAPI(k)));%, 'holes');
    DAPI_IMG(:,:,k) = dapi_slice; 
end

% Use Actin (Phalloidin) channel as edges of cells and then 
% fill holes to calculate area at each slice:

PHALL_VOL_Filled = 0;
PHALLOIDIN_IMG = [];
for k = 1 : length(PHALLOIDIN)
    phalloidin_slice = imfill(cell2mat(PHALLOIDIN(k)));%, 'holes');
    PHALLOIDIN_IMG(:,:,k) = phalloidin_slice; 
    stats = regionprops(phalloidin_slice, 'Area');
    slice_area = sum([stats.Area])*XY_SCALE^2 ;
    % Here we calculate the volume
    PHALL_VOL_Filled = PHALL_VOL_Filled + slice_area * Z_SCALE;
end

disp('Riemann Sum Approach [um^3]:')
disp(PHALL_VOL_Filled);


% This will allow you to view the data in MATLAB (alternatively, go to Volume Viewer in APPS)
% volshow(PHALLOIDIN_IMG, 'ScaleFactors', [XY_SCALE XY_SCALE Z_SCALE]);
% volshow(DAPI_IMG, 'ScaleFactors', [XY_SCALE XY_SCALE Z_SCALE]);

save phall.mat PHALLOIDIN_IMG
save dapi.mat DAPI_IMG
