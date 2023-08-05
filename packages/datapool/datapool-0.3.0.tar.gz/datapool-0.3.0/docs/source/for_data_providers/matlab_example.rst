.. code-block:: matlab

    %
    % SWW-DWH: Example MatLab conversion script
    %
    % 19/12/2016 - Frank Blumensaat
    % Example: conversion('raw_data\data-001.raw','out.dat');
    % -------------------------------------------------------

    function conversion(fNameIn,fNameOut)

    % read full content of the file into 'data'
    fid = fopen(fullfile(fNameIn), 'r');
    dataRaw = textscan(fid, '%s %f %f %f %f %f %f %f %f %f %f %f', Inf, 'Delimiter','\t','TreatAsEmpty',...
        {'NA'},'HeaderLines',1);
    fclose(fid);

    % possible to include check if 12 columns and numeric val's in col2 - col12

    fid = fopen(fullfile(fNameIn), 'r');
    names = textscan(fid, '%s %s %s %s %s %s %s %s %s %s %s %s', 1,'Delimiter','\t','HeaderLines',0);
    fclose(fid);

    % % parse string of TRANSFER time (time stamp) into ML number
    datTime = datenum(dataRaw{1,1}(:),'DD.mm.YYYY hh:MM');

    % define coordinates
    xcoor = ones(length(dataRaw{1}),1).*682558;
    ycoor = ones(length(dataRaw{1}),1).*239404;
    zcoor = zeros(length(dataRaw{1}),1);

    % split data matrix acc. to parameter and remove NaNs
    for j = 2:size(dataRaw,2)
        dataSplit(j-1).var = excise([datTime dataRaw{1,j} xcoor ycoor zcoor]);
    end

    % some parameter names are not conforming to parameters.yaml:
    parametersRaw =  {'Level', 'Velocity', 'Surface Velocity', 'PMR', 'NOS', 'Power Supply'};
    parametersUniform = {'Water Level', 'Average Flow Velocity', 'Surface Flow Velocity',...
                        'Peak to Mean Ratio', 'Number of Samples', 'Battery Voltage'};

    fixNames = containers.Map(parametersRaw,parametersUniform);

    % write processed data to a cell array
    celldata = {};
    clear celldataTemp
    for k = 1:length(dataSplit)
        for i = 1:length(dataSplit(k).var)
            celldataTemp{i,1} = datestr(dataSplit(k).var(i,1),'yyyy-mm-dd HH:MM:SS'); % following the ISO 8601 data standard
            name = char(names{k+1});
            % our parameters.yaml does not have the units in (..), so we remove them:
            name = regexprep(name, '\(.*\)', '');
            % correct some names:
            if isKey(fixNames, name)
                name = fixNames(name);
            end
            celldataTemp{i,2} = name;
            celldataTemp{i,3} = dataSplit(k).var(i,2);
            celldataTemp{i,4} = dataSplit(k).var(i,3);
            celldataTemp{i,5} = dataSplit(k).var(i,4);
            celldataTemp{i,6} = '';
        end
        celldata = vertcat(celldata,celldataTemp);
        clear celldataTemp
    end

    %% write selected data to TXT file
    fid = fopen(fullfile(fNameOut),'w');
    fprintf(fid, '%s; %s; %s; %s; %s; %s \n', 'timestamp', 'parameter', 'value', 'x', 'y', 'z');
    [nrows] = size(celldata);
    for row = 1:nrows
        fprintf(fid,'%s; %s; %f; %d; %d; %d \n',celldata{row,:});
    end
    fclose(fid); 
    end

    %% function to remove NaN values
    function X = excise(X)
    X(any(isnan(X)'),:) = [];
    end
