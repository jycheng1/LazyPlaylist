% Carnegie Mellon University
% 2015 Spring Computer Vision (16-385)
% Instructor: Kris M. Kitani
% Created by: Wei-Chiu Ma (weichium@andrew.cmu.edu)
%%
clear all;

%%% TYPE YOUR ANDREW ID BELOW %%%
andrew_id = 'jycheng1';


%%
% START SUBMISSION CHECK. DO NOT MODIFIY ANYTHING BELOW %
test = [andrew_id, '-test'];
mkdir(test);
unzip([andrew_id, '.zip'], test);

mustExist = {'matlab/myImageFilter.m';'matlab/myEdgeFilter.m'; 'matlab/myHoughTransform.m'; 'matlab/myHoughLines.m'};
mustRemove = {'data'; 'results'; 'matlab/drawLine.m'; 'matlab/houghScript.m'};
s = size(mustExist, 1);
mustExist{s+1, 1} = [andrew_id '.pdf'];

prefix = [test '/' andrew_id '/'];
mustExist = strcat(prefix, mustExist);
mustRemove = strcat(prefix, mustRemove);

for i = 1 : size(mustExist, 1)
    file_name = mustExist{i};
    disp(['Checking ' file_name '...']);
    if exist(file_name, 'file') ~= 2
        rmdir(test, 's');
        error([file_name, ' either does not exist or is in the wrong directory. Please check again.']);
    end
end

for i = 1 : size(mustRemove, 1)
    file_name = mustRemove{i};
    disp(['Checking ' file_name '...']);
    if exist(file_name, 'file') ~= 0
        rmdir(test, 's');
        error([file_name, ' should not exist. Please remove it.']);
    end
end

rmdir(test, 's');
disp('Passed submission check. Ready to submit.');