fprintf(1,'Executing %s at %s:\n',mfilename,datestr(now));
ver,
try,
addpath('/Users/liberty/Documents/MATLAB/spm12');
addpath(genpath(['/Users/liberty/anaconda/lib/python2.7/site-packages/img_pipe' filesep 'surface_warping_scripts']));                             addpath(genpath(['/Users/liberty/anaconda/lib/python2.7/site-packages/img_pipe' filesep 'plotting']));                             load(['/Applications/freesurfer/subjects' filesep 'EC145' filesep 'elecs' filesep 'individual_elecs' filesep 'temporal_grid_orig.mat']);                              save(['/Applications/freesurfer/subjects' filesep 'EC145' filesep 'elecs' filesep 'individual_elecs' filesep 'preproc' filesep 'temporal_grid_orig.mat'],'elecmatrix');                             load(['/Applications/freesurfer/subjects' filesep 'EC145' filesep 'Meshes' filesep 'EC145_lh_dural.mat']);                             hem = 'lh';debug_plots = 0; [elecs_proj] = project_electrodes_anydirection(cortex,                              elecmatrix, [0.949344 -0.277898 -0.114676], debug_plots,'convex_hull');                             elecmatrix = elecs_proj;                             save(['/Applications/freesurfer/subjects' filesep 'EC145' filesep 'elecs' filesep 'individual_elecs' filesep 'temporal_grid.mat'], 'elecmatrix');                             
,catch ME,
fprintf(2,'MATLAB code threw an exception:\n');
fprintf(2,'%s\n',ME.message);
if length(ME.stack) ~= 0, fprintf(2,'File:%s\nName:%s\nLine:%d\n',ME.stack.file,ME.stack.name,ME.stack.line);, end;
end;