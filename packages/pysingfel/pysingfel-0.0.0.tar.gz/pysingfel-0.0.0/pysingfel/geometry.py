import numpy as np
import math

######################################################################
# The following functions are utilized to get corrections
######################################################################
def reshape_pixels_position_arrays_to_1d(array):
    
    array_1d = np.reshape(array, [np.prod(array.shape[:-1]),3])
    return array_1d

def _reciprocal_space_pixel_position(pixel_center, wave_vector, polarization):
    
    ## reshape the array into a 1d position array
    pixel_center_1d = reshape_pixels_position_arrays_to_1d(pixel_center)
    
    ## Calculate the reciprocal position of each pixel
    wave_vector_norm = np.sqrt(np.sum(np.square(wave_vector)))
    wave_vector_direction = wave_vector/ wave_vector_norm
    
    pixel_center_norm = np.sqrt(np.sum(np.square(pixel_center_1d),axis=1))
    pixel_center_direction = pixel_center_1d / pixel_center_norm[:,np.newaxis]
    
    pixel_position_reciprocal_1d = wave_vector_norm*(pixel_center_direction - wave_vector_direction)
    
    ## restore the pixels shape
    pixel_position_reciprocal = np.reshape(pixel_position_reciprocal_1d, pixel_center.shape)
    
    return pixel_position_reciprocal

def _polarization_correction(pixel_center, wave_vector, polarization):
    
    ## reshape the array into a 1d position array
    pixel_center_1d = reshape_pixels_position_arrays_to_1d(pixel_center)
    
    #print pixel_center_1d.shape
    
    pixel_center_norm = np.sqrt(np.sum(np.square(pixel_center_1d),axis=1))
    pixel_center_direction = pixel_center_1d / pixel_center_norm[:,np.newaxis]
    
    ## Calculate the polarization correction
    polarization_norm = np.sqrt(np.sum(np.square(polarization)))
    polarization_direction = polarization/polarization_norm

    
    polarization_correction_1d = np.sum(np.square(np.cross(pixel_center_direction, polarization_direction)),axis=1)
    
    #print polarization_correction_1d.shape
    
    polarization_correction = np.reshape(polarization_correction_1d, pixel_center.shape[0:-1])
    
    return polarization_correction
    
def _geometry_correction(pixel_center, orientation):
    
    ## reshape the array into a 1d position array
    pixel_center_1d = reshape_pixels_position_arrays_to_1d(pixel_center)
    distance = pixel_center_1d[0,2]
    pixel_center_norm = np.sqrt(np.sum(np.square(pixel_center_1d),axis=1))
    pixel_center_direction = pixel_center_1d / pixel_center_norm[:,np.newaxis]
    
    ## Calculate the solid angle correction
    orientation_norm = np.sqrt(np.sum(np.square(orientation)))
    orientation_normalized = orientation/orientation_norm
    
    ## The correction induced by the orientation
    geometry_correction_1d = np.abs(np.dot(pixel_center_direction, orientation_normalized))
    ## The correction induced by the distance
    distance_correction = np.square(distance/pixel_center_norm)
    geometry_correction_1d = np.multiply(geometry_correction_1d, distance_correction)
    
    geometry_correction = np.reshape(geometry_correction_1d, pixel_center.shape[0:-1])
    
    return geometry_correction
    
def reciprocal_space_pixel_position_and_correction(pixel_center, wave_vector, polarization, orientation):

    pixel_position_reciprocal = _reciprocal_space_pixel_position(pixel_center, wave_vector, polarization)
    pixel_position_reciprocal_norm = np.sqrt(np.sum(np.square(pixel_position_reciprocal),axis=-1))*( 1e-10/2. )
    
    polarization_correction = _polarization_correction(pixel_center, wave_vector, polarization)
    geometry_correction = _geometry_correction(pixel_center, orientation)
    
    return pixel_position_reciprocal, pixel_position_reciprocal_norm, polarization_correction, geometry_correction

######################################################################
# The following functions are utilized to get reciprocal space grid mesh
######################################################################
def get_reciprocal_mesh(pixel_position_reciprocal_norm, voxel_length):
    
    reciprocal_space_range = np.max(pixel_position_reciprocal_norm)
    ## The voxel number along 1 dimension is 2*voxel_half_num_1d+1 
    voxel_half_num_1d = np.floor_divide(reciprocal_space_range, voxel_length) + 1
    voxel_num_1d = 2*voxel_half_num_1d+1

    x_meshgrid = (np.array(range(voxel_num_1d)) - voxel_half_num_1d)*voxel_length
    reciprocal_mesh_stack = np.meshgrid(x_meshgrid, x_meshgrid, x_meshgrid )  

    reciprocal_mesh= np.zeros((voxel_num_1d, voxel_num_1d, voxel_num_1d, 3))
    for l in range(3):
        reciprocal_mesh[:,:,:,l] = reciprocal_mesh_stack[l][:,:,:]
    
    return reciprocal_mesh , voxel_half_num_1d, voxel_num_1d
    
def get_weight_in_reciprocal_space(pixel_position_reciprocal, voxel_length, voxel_half_num_1d):
    
    ##convert_to_voxel_unit 
    pixel_position_reciprocal_voxel = pixel_position_reciprocal / voxel_length
    
    ## Get the indexes of the eight nearest points.
    num_x, num_y, _ = pixel_position_reciprocal.shape
    _indexes = np.zeros(( num_x, num_y, 2 ,3))
    for l in range(3):
        _indexes[:,:,0,l] = (np.floor(pixel_position_reciprocal_voxel[:,:,l])
                                                         + voxel_half_num_1d).astype('int')
        _indexes[:,:,1,l] = (np.floor(pixel_position_reciprocal_voxel[:,:,l])
                                                         + voxel_half_num_1d +1).astype('int')
                
    indexes = np.zeros((num_x, num_y, 8, 3))
    for l in range(2):
        for m in range(2):
            for n in range(2):
                indexes[:,:, l*4+m*2+n,0] = _indexes[:,:,l,0] 
                indexes[:,:, l*4+m*2+n,1] = _indexes[:,:,m,1] 
                indexes[:,:, l*4+m*2+n,2] = _indexes[:,:,n,2] 
    
    del _indexes
    
    difference = indexes - pixel_position_reciprocal_voxel[:,:, np.newaxis, :]
    distance = np.sqrt(np.sum(np.square(difference),axis=-1))
    
    del difference
    
    summation = np.sum(distance,axis=-1)
    weight = distance/summation[:,:,np.newaxis]
    
    return indexes, weight

######################################################################
# The following functions are utilized to assemble the images
######################################################################
def assemble_image_from_index_and_panel(image_stack, index):
    # get boundary
    index_max_x = np.max(index[:,:,:,0])
    index_max_y = np.max(index[:,:,:,1])
    # set holder
    image = np.zeros((index_max_x, index_max_y))
    # loop through the panels
    for l in range(index.shape[0]):
        image[index[l,:,:,:]] = image_stack[l,:,:]
        
    return image

def batch_assemble_image_from_index_and_panel(image_stack, index):
    pass

######################################################################
# The following functions are utilized to rotate the pixels in reciprocal space
######################################################################
def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def rotate_pixels_in_reciprocal_space(rotation_matrix, pixels_position):
    pixels_position_1d = reshape_pixels_position_arrays_to_1d(pixels_positions)
    pixels_position_1d = pixels_position_1d.dot(rotation_matrix)
    return np.reshape(pixels_position_1d, pixels_position.shape)