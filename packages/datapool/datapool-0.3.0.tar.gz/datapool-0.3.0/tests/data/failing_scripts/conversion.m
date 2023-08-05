% SWW-DWH: Example MatLab conversion script
%
% 12/09/16 - Frank Blumensaat
% -------------------------------------------------------

function conversion(fNameIn,fNameOut)

% read full content of the file into 'data'
fid = fopen(fullfile(fNameIn), 'r');
data0 = textscan(fid, '%f %s %f %s %f %f %f %f %f', Inf, 'Delimiter','\t','TreatAsEmpty',...
                 {'null'},'HeaderLines',1);
fclose(fid);

% should fail:
data0{1000, 1000}

% parse POSIX time (TST) into ML number; append US level values - ver. 2014b
datTime = data0{1,3}(:)/86400 + datenum(1970,1,1);

% do something (here: remove NaNs) and write data to a struct
dat = excise([datTime data0{1,9}]);

% write processed data to a cell array
for i = 1:length(dat)
    celldata{i,1} = datestr(dat(i,1));
    celldata{i,2} = dat(i,2);
end

%% write data to TXT file
fid = fopen(fNameOut,'w');
fprintf(fid, '%s\t %s\n', 'Date', 'Level [mm]');
[nrows] = size(celldata);
for row = 1:nrows
    fprintf(fid,'%s\t %d \n',celldata{row,:});
end
fclose(fid); 


%% function to remove NaN values
function X = excise(X)
X(any(isnan(X)'),:) = [];
