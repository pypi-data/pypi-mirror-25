#!/usr/bin/env python
## THIS DOESNT WORK DONT USE IT ###

import matplotlib
matplotlib.use('Qt4Agg') 
from matplotlib import pyplot as plt
plt.rcParams['keymap.save'] = '' # Unbind 's' key saving
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica','Verdana','Bitstream Vera Sans','sans-serif']

from matplotlib import cm
import matplotlib.colors as mcolors
import numpy as np
import nibabel as nib
import scipy.ndimage
import sys
from PyQt4 import QtCore, QtGui
import matplotlib.patches as mpatches
import scipy.io
import os
import warnings
import math

from nibabel.processing import resample_from_to  
from nibabel.affines import apply_affine

# For affine registration
# from nipy.core.api import AffineTransform
# import nipy.algorithms
# import nipy.algorithms.resample


warnings.filterwarnings('ignore')

class acpc_picker:
	'''
	acpc_picker.py defines a class [acpc_picker] that allows the 
	user to take a co-registered CT and MRI scan and identify electrodes
	based on sagittal, coronal, and axial views of the scans as well as
	a maximum intensity projection of the CT scan. Inputs are the 
	subject directory and the hemisphere of implantation.  If stereo-EEG,
	choose 'stereo' as the hemisphere

	Usage: 
		python acpc_picker.py '/usr/local/freesurfer/subjects/S1' 'rh'

	This assumes that you have processed your data using freesurfer's pipeline
	and that you have a coregistered MRI and CT in subj_dir (e.g. '/usr/local/freesurfer/subjects/S1')
	as [subj_dir]/mri/brain.mgz and [subj_dir]/CT/rCT.nii

	Written by Liberty Hamilton, 2017

	'''
	def __init__(self, subj_dir, hem):
		'''
		Initialize the electrode picker with the user-defined MRI and co-registered
		CT scan in [subj_dir].  Images will be displayed using orientation information 
		obtained from the image header. Images will be resampled to dimensions 
		[256,256,256] for display.
		We will also listen for keyboard and mouse events so the user can interact
		with each of the subplot panels (zoom/pan) and add/remove electrodes with a 
		keystroke.
		'''
		QtCore.pyqtRemoveInputHook()
		self.subj_dir = subj_dir
		if hem == 'stereo':
			hem = 'lh' # For now, set to lh because hemisphere isn't used in stereo case
		self.hem = hem
		self.img_file = os.path.join(subj_dir, 'acpc', 'T1.nii')
		self.img = nib.load(self.img_file)
		self.ac = []
		self.pc = []
		
		# Get affine transform 
		self.affine = self.img.affine
		self.fsVox2RAS = np.array([[-1., 0., 0., 128.], 
								   [0., 0., 1., -128.], 
								   [0., -1., 0., 128.], 
								   [0., 0., 0., 1.]])
		self.reorient_affine = [] # For eventual reorient to ACPC
		
		# Apply orientation to the MRI so that the order of the dimensions will be
		# sagittal, coronal, axial
		self.codes = nib.orientations.axcodes2ornt(nib.orientations.aff2axcodes(self.affine))
		img_data = nib.orientations.apply_orientation(self.img.get_data(), self.codes)
		self.voxel_sizes = nib.affines.voxel_sizes(self.affine)
		nx,ny,nz = np.array(img_data.shape, dtype='float')

		self.inv_affine = np.linalg.inv(self.affine)
		self.img_clim = np.percentile(img_data, (1., 99.))		

		# Resample both images to the highest resolution
		#voxsz = (256, 256, 256)
		#if self.img.shape != voxsz:
		#	print("Resizing voxels in MRI")
		#	img_data = scipy.ndimage.zoom(img_data, [voxsz[0]/nx, voxsz[1]/ny, voxsz[2]/nz])
		
		self.img_data = img_data
		self.img_data_r = img_data # Initialize to non-reoriented
		self.elec_data = np.nan+np.zeros((img_data.shape))
		self.elec_data_r = self.elec_data # Initialize to non-reoriented
		self.bin_mat = '' # binary mask for electrodes
		self.device_num = 0 # Start with device 0, increment when we add a new electrode name type
		self.device_name = ''
		self.devices = [] # This will be a list of the devices (grids, strips, depths)
		self.elec_num = dict()
		self.elecmatrix = dict()# This will be the electrode coordinates 
		self.legend_handles = [] # This will hold legend entries

		#self.imsz = [256, 256, 256]
		self.imsz = img_data.shape

		self.current_slice = np.array([self.imsz[0]/2, self.imsz[1]/2, self.imsz[2]/2], dtype=np.float)
		
		self.fig=plt.figure(figsize=(12,10))
		self.fig.canvas.set_window_title('ACPC Picker')
		thismanager = plt.get_current_fig_manager()
		thismanager.window.setWindowIcon(QtGui.QIcon((os.path.join('icons','leftbrain_blackbg.png'))))
		
		self.im = []
		self.elec_im = []

		self.cursor = []
		self.cursor2 = []

		im_ranges = [[0, self.imsz[1], 0, self.imsz[2]],
					 [0, self.imsz[0], 0, self.imsz[2]],
					 [0, self.imsz[0], 0, self.imsz[1]],
					 [0, self.imsz[1], 0, self.imsz[2]],
					 [0, self.imsz[0], 0, self.imsz[2]],
					 [0, self.imsz[0], 0, self.imsz[1]]]
		im_labels = [['Inferior','Posterior'],
					 ['Inferior','Left'],
					 ['Posterior','Left'],
					 ['Inferior','Posterior'],
					 ['Inferior','Left'],
					 ['Posterior','Left']]

		self.ax = []
		self.contour = [False, False, False]
		self.pial_surf_on = True # Whether pial surface is visible or not
		
		# This is the current slice for indexing (as integers so python doesnt complain)
		cs = np.round(self.current_slice).astype(np.int)

		# Plot sagittal, coronal, and axial views 
		for i in np.arange(6):
			self.ax.append(self.fig.add_subplot(2,3,i+1))
			self.ax[i].set_axis_bgcolor('k')
			if i==0:
				imdata = self.img_data[cs[0],:,:].T
				edat   = self.elec_data[cs[0],:,:].T
			elif i==1:
				imdata = self.img_data[:,cs[1],:].T
				edat   = self.elec_data[:,cs[1],:].T
				plt.gca().set_title('Original image')
			elif i==2:
				imdata = self.img_data[:,:,cs[2]].T
				edat   = self.elec_data[:,:,cs[2]].T
			if i==3:
				imdata = self.img_data_r[cs[0],:,:].T
				edat   = self.elec_data_r[cs[0],:,:].T
			elif i==4:
				imdata = self.img_data_r[:,cs[1],:].T
				edat   = self.elec_data_r[:,cs[1],:].T
				plt.gca().set_title('Reoriented image')
			elif i==5:
				imdata = self.img_data_r[:,:,cs[2]].T
				edat   = self.elec_data_r[:,:,cs[2]].T

			# Show the MRI data in grayscale
			self.im.append(plt.imshow(imdata, cmap=cm.gray, aspect='auto'))

			# Overlay the electrodes image on top (starts as NaNs, is eventually filled in)
			self.elec_colors = mcolors.LinearSegmentedColormap.from_list('elec_colors', np.vstack (( cm.Set1(np.linspace(0., 1, 9)), cm.Set2(np.linspace(0., 1, 8)) )) )
			self.elec_im.append(plt.imshow(edat, cmap=self.elec_colors, aspect='auto', alpha=1, vmin=0, vmax=17))

			# Plot a green cursor
			self.cursor.append(plt.plot([cs[1], cs[1]], [self.ax[i].get_ylim()[0]+1, self.ax[i].get_ylim()[1]-1], color=[0, 1, 0] ))
			self.cursor2.append(plt.plot([self.ax[i].get_xlim()[0]+1, self.ax[i].get_xlim()[1]-1], [cs[2], cs[2]], color=[0, 1, 0] ))
			
			# Flip the y axis so brains are the correct side up
			plt.gca().invert_yaxis()

			# Get rid of tick labels
			self.ax[i].set_xticks([])
			self.ax[i].set_yticks([])

			# Label the axes
			self.ax[i].set_xlabel(im_labels[i][0])
			self.ax[i].set_ylabel(im_labels[i][1])
			self.ax[i].axis(im_ranges[i])

		self.elec_im.append(plt.imshow(self.elec_data[cs[0],:,:].T, cmap=self.elec_colors, aspect='auto', alpha=1, vmin=0, vmax=17))
		plt.gcf().suptitle("Press 'a' to add a point for the anterior commissure (AC), press 'p' to add the posterior commissure (PC), press 'r' to reorient, press 's' to save", fontsize=14)

		plt.tight_layout()
		plt.subplots_adjust(top=0.9)
		cid2 = self.fig.canvas.mpl_connect('scroll_event',self.on_scroll)
		cid3 = self.fig.canvas.mpl_connect('button_press_event',self.on_click)
		cid = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
		#cid4 = self.fig.canvas.mpl_connect('key_release_event', self.on_key)

		plt.show()
		self.fig.canvas.draw()

	def on_key(self, event):
		''' 
		Executes when the user presses a key.  Potential key inputs are:

		Electrode adding:
		----
		n: enter the name of a new device (e.g. 'frontalgrid','hippocampaldepth')
		e: insert an electrode at the current green crosshair position
		u: remove electrode at the current crosshair position (can be thought of like "undo")

		Views:
		----
		s: sagittal view for maximum intensity projection at bottom right
		c: coronal view for maximum intensity projection at bottom right
		a: axial view for maximum intensity projection at bottom right
		pagedown/pageup: move by one slice in currently selected pane
		arrow up/arrow down: pan by one voxel in currently selected pane
		'''
		#print('You pressed', event.key)
		bb1=self.ax[0].get_position()
		bb2=self.ax[1].get_position()
		bb3=self.ax[2].get_position()
		bb4=self.ax[3].get_position()
		bb5=self.ax[4].get_position()
		bb6=self.ax[5].get_position()

		# Transform coordinates to figure coordinates
		fxy = self.fig.transFigure.inverted().transform((event.x, event.y))

		slice_num = []
		if bb1.contains(fxy[0],fxy[1]):
			slice_num = 0
		if bb2.contains(fxy[0],fxy[1]):
			slice_num = 1
		if bb3.contains(fxy[0],fxy[1]):
			slice_num = 2
		if bb4.contains(fxy[0],fxy[1]):
			slice_num = 3
		if bb5.contains(fxy[0],fxy[1]):
			slice_num = 4
		if bb6.contains(fxy[0],fxy[1]):
			slice_num = 5

		if event.key == 'escape':
			plt.close()

		if event.key == 'h':
			# Show help 
			plt.gcf().suptitle("Help: 'n': name device, 'e': add electrode, 'u': remove electrode, 't': toggle pial surface\nMaximum intensity projection views: 's': sagittal, 'c': coronal, 'a': axial\nScroll to zoom, arrows to pan, pgup/pgdown or click to go to slice", fontsize=12)

		if event.key == 'a':
			self.add_landmark(point_type=event.key)

		if event.key == 'p':
			self.add_landmark(point_type=event.key)

		if event.key == 'r':
			self.reorient_image()

		if slice_num != []:
			this_ax = self.ax[slice_num]

			# Scrolling through slices
			if event.key == 'pageup' or event.key == 'pagedown':
				if event.key == 'pagedown':
					sgn = -1
				else:
					sgn = 1
				self.current_slice[slice_num] = self.current_slice[slice_num] + 1*sgn
				
			# Panning left/right/up/down
			if event.key == 'up' or event.key == 'down' or event.key == 'left' or event.key == 'right':
				if event.key == 'up' or event.key == 'down':
					if event.key == 'up':
						sgn = -1
					else:
						sgn = 1
					ylims = this_ax.get_ylim()
					this_ax.set_ylim([ylims[0]+1*sgn, ylims[1]+1*sgn])
					
				elif event.key == 'left' or event.key == 'right':
					if event.key == 'right':
						sgn = -1
					else:
						sgn = 1
					xlims = this_ax.get_xlim()
					this_ax.set_xlim(xlims[0]+1*sgn, xlims[1]+1*sgn)

		# Draw the figure
		self.update_figure_data(ax_clicked=slice_num)
		plt.gcf().canvas.draw()

	def on_scroll(self, event):
		''' Use mouse scroll wheel to zoom.  Scroll down zooms in, scroll up zooms out.
		'''
		stepsz = 5.

		for a in np.arange(3):
			xstep = event.step*stepsz
			ystep = event.step*stepsz
			if a==0:
				xstep *= np.float(self.imsz[1])/self.imsz[0]
				ystep *= np.float(self.imsz[2])/self.imsz[0]
			elif a==1:
				xstep *= np.float(self.imsz[0])/self.imsz[0]
				ystep *= np.float(self.imsz[2])/self.imsz[0]
			elif a==2:
				xstep *= np.float(self.imsz[0])/self.imsz[0]
				ystep *= np.float(self.imsz[1])/self.imsz[0]

			this_ax = self.ax[a]
			xlims = this_ax.get_xlim()
			ylims = this_ax.get_ylim()
			if xlims[0] + xstep > xlims[1] - xstep:
				this_ax.set_xlim(xlims[0], xlims[1])
			else:
				this_ax.set_xlim(xlims[0]+xstep, xlims[1] - xstep)
			if ylims[0] + ystep > ylims[1] - ystep:
				this_ax.set_ylim(ylims[0], ylims[1])
			else:
				this_ax.set_ylim(ylims[0]+ystep, ylims[1] - ystep)
			self.cursor[a][0].set_ydata ([self.ax[a].get_ylim()]) 
			self.cursor2[a][0].set_xdata([self.ax[a].get_xlim()])

		plt.gcf().canvas.draw()

	def on_click(self, event):
		'''
		Executes on mouse click events -- moves appropriate subplot axes to (x,y,z)
		view on MRI and CT views.
		'''

		#print('You scrolled %d steps at x: %d, y: %d', event.step, event.x, event.y)
		# Get the bounding box for each of the subplots
		bb1=self.ax[0].get_position()
		bb2=self.ax[1].get_position()
		bb3=self.ax[2].get_position()

		#print event.xdata, event.ydata
		# Transform coordinates to figure coordinates
		fxy = self.fig.transFigure.inverted().transform((event.x, event.y))
		
		x = np.int(np.round(event.xdata))
		y = np.int(np.round(event.ydata))

		# If you clicked the first subplot
		if bb1.contains(fxy[0],fxy[1]):
			self.current_slice[1] = event.xdata
			self.current_slice[2] = event.ydata
			ax_num = 0
			
		# If you clicked the second subplot
		elif bb2.contains(fxy[0],fxy[1]):
			self.current_slice[0] = event.xdata
			self.current_slice[2] = event.ydata
			ax_num = 1

		# If you clicked the third subplot
		elif bb3.contains(fxy[0],fxy[1]):
			self.current_slice[0] = event.xdata
			self.current_slice[1] = event.ydata
			ax_num = 2

		self.update_figure_data(ax_clicked=ax_num)

		#print("Current slice: %3.2f %3.2f %3.2f"%(self.current_slice[0], self.current_slice[1], self.current_slice[2]))
		plt.gcf().canvas.draw()

	def update_figure_data(self, ax_clicked=None):
		'''
		Updates all four subplots based on the crosshair position (self.current_slice)
		The subplots (in order) are the sagittal view, coronal view, and axial view,
		followed by the maximum intensity projection of the CT scan (in the user
		specified view, which is sagittal by default)
		'''
		cs = np.round(self.current_slice).astype(np.int) # Make integer for indexing the volume
		if self.reorient_affine != []:
			cs_reorient = apply_affine(self.reorient_affine, self.current_slice)
		else:
			cs_reorient = cs

		self.im[0].set_data(self.img_data[cs[0],:,:].T)
		self.im[1].set_data(self.img_data[:,cs[1],:].T)
		self.im[2].set_data(self.img_data[:,:,cs[2]].T)
		self.im[3].set_data(self.img_data_r[cs_reorient[0],:,:].T)
		self.im[4].set_data(self.img_data_r[:,cs_reorient[1],:].T)
		self.im[5].set_data(self.img_data_r[:,:,cs_reorient[2]].T)
		
		# Show the electrode volume data in the sagittal, coronal, and axial views
		self.elec_im[0].set_data(self.elec_data[cs[0],:,:].T)
		self.elec_im[1].set_data(self.elec_data[:,cs[1],:].T)
		self.elec_im[2].set_data(self.elec_data[:,:,cs[2]].T)

		# Set the crosshairs for the sagittal (0), coronal (1), and axial (2) views
		self.cursor[0][0].set_xdata ([self.current_slice[1], self.current_slice[1]])
		self.cursor[0][0].set_ydata ([self.ax[0].get_ylim()])
		self.cursor2[0][0].set_ydata([self.current_slice[2], self.current_slice[2]])
		self.cursor2[0][0].set_xdata ([self.ax[0].get_xlim()])
		self.cursor[1][0].set_xdata ([self.current_slice[0], self.current_slice[0]])
		self.cursor[1][0].set_ydata ([self.ax[1].get_ylim()])
		self.cursor2[1][0].set_ydata([self.current_slice[2], self.current_slice[2]])
		self.cursor2[1][0].set_xdata ([self.ax[1].get_xlim()])
		self.cursor[2][0].set_xdata ([self.current_slice[0], self.current_slice[0]])
		self.cursor[2][0].set_ydata ([self.ax[2].get_ylim()])
		self.cursor2[2][0].set_ydata([self.current_slice[1], self.current_slice[1]])
		self.cursor2[2][0].set_xdata ([self.ax[2].get_xlim()])

		# Re-center the plots at the crosshair location
		for a in np.arange(6):
			# Only re-center plots that you didn't click on (since it's annoying
			# when the plot that you just clicked moves...)
			if a!=ax_clicked:
				xlims = self.ax[a].get_xlim()
				xax_range = xlims[1]-xlims[0]
				ylims = self.ax[a].get_ylim()
				yax_range = ylims[1]-ylims[0]
				center_pt_x = self.cursor[a][0].get_xdata()[0]
				center_pt_y = self.cursor2[a][0].get_ydata()[0]
				self.ax[a].set_xlim(center_pt_x - xax_range/2., center_pt_x + xax_range/2.)
				self.ax[a].set_ylim(center_pt_y - yax_range/2., center_pt_y + yax_range/2.)
				self.cursor[a][0].set_ydata ([self.ax[a].get_ylim()]) 
				self.cursor2[a][0].set_xdata([self.ax[a].get_xlim()])

	def add_landmark(self, point_type):
		'''
		Add AC or PC landmark at the current crosshair point. 
		'''

		if point_type=='a':
			self.device_num = 1
			self.ac = self.current_slice
		elif point_type=='p':
			self.device_num = 2
			self.pc = self.current_slice

		# Make the current slice into an integer for indexing the volume
		cs = np.round(self.current_slice).astype(np.int) 

		# Create a sphere centered around the current point as a binary matrix
		radius = 2
		r2 = np.arange(-radius, radius+1)**2
		dist2 = r2[:,None,None]+r2[:,None]+r2
		bin_mat = np.array(dist2<=radius**2, dtype=np.float)
		bin_mat[bin_mat==0] = np.nan
		
		# The sphere part of the binary matrix will have a value that
		# increments with device number so that different devices
		# will show up in different colors
		bin_mat = bin_mat + self.device_num - 2
		self.bin_mat = bin_mat
		
		# Set the electrode data volume for this bounding box (add the
		# sphere to the electrode "volume" so it shows up in the brain
		# plots)
		self.elec_data[cs[0]-radius:cs[0]+radius+1, cs[1]-radius:cs[1]+radius+1, cs[2]-radius:cs[2]+radius+1] = bin_mat

		self.elec_im[0].set_data(self.elec_data[cs[0],:,:].T)
		self.elec_im[0].set_data(self.elec_data[:,cs[1],:].T)
		self.elec_im[0].set_data(self.elec_data[:,:,cs[2]].T)

		# As displayed, these coordinates are LSP, and we want RAS,
		# so we do that here
		elec = self.slice_to_surfaceRAS()

		plt.gcf().suptitle('surface RAS = [%3.3f, %3.3f, %3.3f]'%(elec[0], elec[1], elec[2]), fontsize=14)
		
	def reorient_image(self):
		'''
		Reorient the image using the identified AC-PC (AC as the origin, aligned to the acpc axis)
		'''

		if self.ac != [] and self.pc != []:
			self.reorient_affine = np.array([[ math.atan2(self.pc[0],self.ac[0]),  0.,  0.,  -self.ac[0]],
	       					[ 0.,  math.atan2(self.pc[1],self.ac[1]),  0.,  -self.ac[1]],
	       					[ 0.,  0.,  math.atan2(self.pc[2],self.ac[2]),  -self.ac[2]],
	       					[ 0.,  0.,  0.,  1.]])
			self.reorient_affine = np.array([[ 1.,  0.,  0.,  -self.ac[0]],
	       									 [ 0.,  1.,  0.,  -self.ac[1]],
	       									 [ 0.,  0.,  1.,  -self.ac[2]],
	       									 [ 0.,  0.,  0.,  1.]])

			print("Resampling data")
			r_img = self.img
			r_img.set_sform = r_img.affine + self.reorient_affine
			self.img_data_r = r_img.get_data()
			nib.save(r_img, '/Users/liberty/Desktop/test.nii')
			print("Done")
			self.update_figure_data()


	def slice_to_surfaceRAS(self, coord = None):
		'''
		Convert slice coordinate from the viewer to surface RAS
		'''
		if coord is None:
			coord = self.current_slice

		elec_CRS = np.hstack((self.imsz[0] - coord[0],
							  self.imsz[2] - coord[2],
							  coord[1], 1))
		
		# Convert CRS to RAS
		elec = np.dot(self.fsVox2RAS, elec_CRS.transpose()).transpose()
		elec = elec[:3]

		return elec

	def surfaceRAS_to_slice(self, elec):
		'''
		Convert surface RAS to coordinate to be used in the viewer
		'''
		elec = np.hstack((elec, 1))

		# Convert CRS to RAS
		elec_CRS = np.dot(np.linalg.inv(self.fsVox2RAS), elec.transpose()).transpose()

		print(elec_CRS)
		coord = np.hstack((self.imsz[0] - elec_CRS[0],
						   elec_CRS[2],
						   self.imsz[1] - elec_CRS[1]))
		
		return coord

	def update_legend(self, vmax=17.):
		''' 
		Update the legend with the electrode devices.
		'''
		self.legend_handles = []
		for i in self.devices:
			QtCore.pyqtRemoveInputHook()
			cmap = self.elec_colors
			num = self.devices.index(i)
			c = cmap(num/vmax)
			color_patch = mpatches.Patch(color=c, label=i)
			self.legend_handles.append(color_patch)
			plt.legend(handles=self.legend_handles, loc='upper right', fontsize='x-small')

			
if __name__ == '__main__':
	app = QtGui.QApplication([])
	app.setWindowIcon(QtGui.QIcon(os.path.join('icons','leftbrain.png')))
	subj_dir = sys.argv[1]
	hem = sys.argv[2]
	e = acpc_picker(subj_dir = subj_dir, hem = hem)
