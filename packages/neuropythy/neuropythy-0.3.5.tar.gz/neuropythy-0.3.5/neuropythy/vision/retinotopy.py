####################################################################################################
# neuropythy/vision/retinotopy.py
# Tools for registering the cortical surface to a particular potential function
# By Noah C. Benson

import numpy                        as np
import scipy                        as sp
import nibabel.freesurfer.io        as fsio
import nibabel.freesurfer.mghformat as fsmgh

import os, sys, gzip, abc

from numpy.linalg import norm
from math         import pi
from numbers      import Number
from pysistence   import make_dict

from neuropythy.cortex       import (CorticalMesh, mesh_property)
from neuropythy.freesurfer   import (freesurfer_subject, add_subject_path,
                                     cortex_to_ribbon, cortex_to_ribbon_map,
                                     Hemisphere, subject_paths)
from neuropythy.topology     import (Registration)
from neuropythy.registration import (mesh_register, java_potential_term)
from neuropythy.java         import (to_java_doubles, to_java_ints)

from .models import (RetinotopyModel, SchiraModel, RetinotopyMeshModel, RegisteredRetinotopyModel,
                     load_fmm_model)

# Tools for extracting retinotopy data from a subject:
_empirical_retinotopy_names = {
    'polar_angle':  ['prf_polar_angle',       'empirical_polar_angle',  'measured_polar_angle',
                     'training_polar_angle',  'polar_angle'],
    'eccentricity': ['prf_eccentricity',      'empirical_eccentricity', 'measured_eccentricity',
                     'training_eccentricity', 'eccentricity'],
    'weight':       ['prf_weight',       'prf_variance_explained',       'prf_vexpl',
                     'empirical_weight', 'empirical_variance_explained', 'empirical_vexpl',
                     'measured_weight',  'measured_variance_explained',  'measured_vexpl',
                     'training_weight',  'training_variance_explained',  'training_vexpl',
                     'weight',           'variance_explained',           'vexpl']}

# handy function for picking out properties automatically...
def empirical_retinotopy_data(hemi, retino_type):
    '''
    empirical_retinotopy_data(hemi, t) yields a numpy array of data for the given hemisphere object
    and retinotopy type t; it does this by looking at the properties in hemi and picking out any
    combination that is commonly used to denote empirical retinotopy data. These common names are
    stored in _empirical_retintopy_names, in order of preference, which may be modified.
    The argument t should be one of 'polar_angle', 'eccentricity', 'weight'.
    '''
    dat = _empirical_retinotopy_names[retino_type.lower()]
    hdat = {s.lower(): s for s in hemi.property_names}
    return next((hemi.prop(hdat[s.lower()]) for s in dat if s.lower() in hdat), None)

_predicted_retinotopy_names = {
    'polar_angle':  ['predicted_polar_angle',   'model_polar_angle',
                     'registered_polar_angle',  'template_polar_angle'],
    'eccentricity': ['predicted_eccentricity',  'model_eccentricity',
                     'registered_eccentricity', 'template_eccentricity'],
    'visual_area':  ['predicted_visual_area',   'model_visual_area',
                     'registered_visual_area',  'template_visual_area']}

def predicted_retinotopy_data(hemi, retino_type):
    '''
    predicted_retinotopy_data(hemi, t) yields a numpy array of data for the given hemisphere object
    and retinotopy type t; it does this by looking at the properties in hemi and picking out any
    combination that is commonly used to denote empirical retinotopy data. These common names are
    stored in _predicted_retintopy_names, in order of preference, which may be modified.
    The argument t should be one of 'polar_angle', 'eccentricity', 'visual_area'.
    '''
    dat = _predicted_retinotopy_names[retino_type.lower()]
    hdat = {s.lower(): s for s in hemi.property_names}
    return next((hemi.prop(hdat[s]) for s in dat if s.lower() in hdat), None)

_retinotopy_names = {
    'polar_angle':  set(['polar_angle']),
    'eccentricity': set(['eccentricity']),
    'visual_area':  set(['visual_area', 'visual_roi', 'visual_region', 'visual_label']),
    'weight':       set(['weight', 'variance_explained'])}

def retinotopy_data(hemi, retino_type):
    '''
    retinotopy_data(hemi, t) yields a numpy array of data for the given hemisphere object
    and retinotopy type t; it does this by looking at the properties in hemi and picking out any
    combination that is commonly used to denote empirical retinotopy data. These common names are
    stored in _predicted_retintopy_names, in order of preference, which may be modified.
    The argument t should be one of 'polar_angle', 'eccentricity', 'visual_area', or 'weight'.
    Unlike the related functions empirical_retinotopy_data and predicted_retinotopy_data, this
    function calls both of these (predicted first then empirical) in the case that it does not
    find a valid property.
    '''
    dat = _retinotopy_names[retino_type.lower()]
    val = next((hemi.prop(s) for s in hemi.property_names if s.lower() in dat), None)
    if val is None and retino_type.lower() != 'weight':
        val = predicted_retinotopy_data(hemi, retino_type)
    if val is None and retino_type.lower() != 'visual_area':
        val = empirical_retinotopy_data(hemi, retino_type)
    return val

def extract_retinotopy_argument(obj, retino_type, arg, default='any'):
    '''
    extract_retinotopy_argument(o, retino_type, argument) yields retinotopy data of the given
    retinotopy type (e.g., 'polar_angle', 'eccentricity', 'variance_explained', 'visual_area',
    'weight') from the given hemisphere or cortical mesh object o, according to the given
    argument. If the argument is a string, then it is considered a property name and that is
    returned regardless of its value. If the argument is an iterable, then it is returned. If
    the argument is None, then retinotopy will automatically be extracted, if found, by calling
    the retinotopy_data function.
    The option default (which, by default, is 'any') specifies which function should be used to
    extract retinotopy in the case that the argument is None. The value 'any' indicates that the
    function retinotopy_data should be used, while the values 'empirical' and 'predicted' specify
    that the empirical_retinotopy_data and predicted_retinotopy_data functions should be used,
    respectively.
    '''
    if isinstance(arg, basestring): values = obj.prop(arg)
    elif hasattr(arg, '__iter__'):  values = arg
    elif arg is not None:           raise ValueError('cannot interpret retinotopy arg: %s' % arg)
    elif default == 'predicted':    values = predicted_retinotopy_data(obj, retino_type)
    elif default == 'empirical':    values = empirical_retinotopy_data(obj, retino_type)
    elif default == 'any':          values = retinotopy_data(obj, retino_type)
    else:                           raise ValueError('bad default retinotopy: %s' % default)
    if values is None:
        raise RuntimeError('No %s retinotopy data found given argument: %s' % (retino_type, arg))
    n = obj.vertex_count
    if len(values) != n:
        found = False
        # could be that we were given a mesh data-field for a map
        try:
            s = obj.meta_data['source_mesh']
            if s.vertex_count == len(values):
                values = np.asarray(values)[obj.vertex_list]
                found = True
        except: pass
        if not found:
            raise RuntimeError('Given %s data has incorrect length (%s instead of %s)!' \
                               % (retino_type, len(values), n))
    return np.array(values)

_default_polar_angle_units = {
    'polar_angle': 'deg',
    'polar angle': 'deg',
    'angle':       'rad',
    'theta':       'rad',
    'polang':      'deg',
    'ang':         'rad'}
_default_polar_angle_axis = {
    'polar_angle': 'UVM',
    'polar angle': 'UVM',
    'angle':       'RHM',
    'theta':       'RHM',
    'polang':      'UVM',
    'ang':         'RHM'}
_default_polar_angle_dir = {
    'polar_angle': 'cw',
    'polar angle': 'cw',
    'angle':       'ccw',
    'theta':       'ccw',
    'polang':      'cw',
    'ang':         'ccw'}
_default_eccentricity_units = {
    'eccentricity': 'deg',
    'eccen':        'deg',
    'rho':          'rad',
    'ecc':          'deg',
    'radius':       'rad'}
_default_x_units = {
    'x':            'rad',
    'longitude':    'deg',
    'lon':          'deg'}
_default_y_units = {
    'y':            'rad',
    'latitude':     'deg',
    'lat':          'deg'}
_default_z_units = {
    'z':            'rad',
    'complex':      'deg',
    'complex-rad':  'rad',
    'coordinate':   'deg'}
def _clean_angle_deg(polang):
    polang = np.asarray(polang)
    clean = np.mod(polang + 180, 360) - 180
    is180 = np.isclose(polang, -180)
    clean[is180] = np.abs(clean[is180]) * np.sign(polang[is180])
    return clean
def _clean_angle_rad(polang):
    polang = np.asarray(polang)
    clean = np.mod(polang + np.pi, np.pi*2) - np.pi
    return clean
_retinotopy_style_fns = {
    'visual':       lambda t,e: (_clean_angle_deg(90.0 - 180.0/np.pi * t), e),
    'visual-rad':   lambda t,e: (_clean_angle_rad(np.pi/2 - t), e * np.pi/180.0),
    'spherical':    lambda t,e: (_clean_angle_rad(t), e*np.pi/180.0),
    'standard':     lambda t,e: (_clean_angle_rad(t), e),
    'cartesian':    lambda t,e: (np.pi/180.0 * e * np.cos(t), np.pi/180.0 * e * np.sin(t)),
    'geographical': lambda t,e: (e * np.cos(t), e * np.sin(t)),
    'complex':      lambda t,e: e * np.exp(t * 1j),
    'complex-rad':  lambda t,e: np.pi/180.0 * e * np.exp(t * 1j),
    'z':            lambda t,e: np.pi/180.0 * e * np.exp(t * 1j)}

def as_retinotopy(data, output_style='visual', units=Ellipsis, prefix=None, suffix=None):
    '''
    as_retinotopy(data) converts the given data, if possible, into a 2-tuple, (polar_angle, eccen),
      both in degrees, with 0 degrees of polar angle corresponding to the upper vertical meridian
      and negative values corresponding to the left visual hemifield.
    as_retinotopy(data, output_style) yields the given retinotopy data in the given output_style;
      as_retinotopy(data) is equivalent to as_retinotopy(data, 'visual').

    This function is intended as a general conversion routine between various sources of retinotopy
    data. All lookups are done in a case insensitive manner. Data may be specified in any of the
    following ways:
      * A cortical mesh containing recognized properties (such as 'polar_angle' and 'eccentricity'
        or 'latitude' and 'longitude'.
      * A dict with recognized fields.
      * A tuple of (polar_angle, eccentricity) (assumed to be in 'visual' style).
      * A numpy vector of complex numbers (assumed in 'complex' style).
      * An n x 2 or 2 x n matrix whose rows/columns are (polar_angle, eccentricity) values (assumed
        in 'visual' style).

    The following output_styles are accepted:
      * 'visual':       polar-axis:         upper vertical meridian
                        positive-direction: clockwise
                        fields:             ['polar_angle' (degrees), 'eccentricity' (degrees)]
      * 'spherical':    polar-axis:         right horizontal meridian
                        positive-direction: counter-clockwise
                        fields:             ['theta' (radians), 'rho' (radians)]
      * 'standard':     polar-axis:         right horizontal meridian
                        positive-direction: counter-clockwise
                        fields:             ['angle' (radians), 'eccentricity' (degrees)]
      * 'cartesian':    axes:               x/y correspond to RHM/UVM
                        positive-direction: left/up
                        fields:             ('x' (radians), 'y' (radians))
      * 'geographical': axes:               x/y correspond to RHM/UVM
                        positive-direction: left/up
                        fields:             ('longitude' (degrees), 'latitude' (degrees))
      * 'complex':      axes:               x/y correspond to RHM/UVM
                        positive-direction: left/up
                        fields:             longitude (degrees) + I*latitude (degrees)
      * 'complex-rad':  axes:               x/y correspond to RHM/UVM
                        positive-direction: left/up
                        fields:             longitude (radians) + I*latitude (radians)
      * 'visual-rad':   polar-axis:         upper vertical meridian
                        positive-direction: clockwise
                        fields:             ['angle' (radians), 'eccentricity' (radians)]

    The following options may be given:
      * units (Ellipsis) specifies the unit that should be assumed (degrees or radians);
        if Ellipsis is given, then auto-detect the unit if possible. This may be a map whose keys are
        'polar_angle' and 'eccentricity' (or the equivalent titles in data) and whose keys are the
        individual units.
      * prefix (None) specifies a prefix that is required for any keys or property names.
      * suffix (None) specifies a suffix that is required for any keys or property names.
    '''
    # simple sanity check:
    output_style = output_style.lower()
    if output_style not in _retinotopy_style_fns:
        raise ValueError('Unrecognized output style: %s' % output_style)
    # First step: get the retinotopy into a format we can deal with easily
    if isinstance(data, tuple) and len(data) == 2:
        data = {'polar_angle': data[0], 'eccentricity': data[1]}
    if isinstance(data, list):
        data = np.asarray(data)
    if isinstance(data, np.ndarray):
        if len(data.shape) == 1 and np.issubdtype(data.dtype, np.complex):
            data = {'complex': data}
        else:
            if data.shape[1] == 2: data = data.T
            data = {'polar_angle': data[0], 'eccentricity': data[1]}
    # We now assume that data is a dict type; or is a mesh;
    # figure out the data we have and make it into theta/rho
    if isinstance(data, CorticalMesh) or isinstance(data, Hemisphere):
        pnames = {k.lower():k for k in data.property_names}
        mem_dat = lambda k: k in pnames
        get_dat = lambda k: data.prop(pnames[k])
    else:
        data = {k.lower():v for (k,v) in data.iteritems()}
        mem_dat = lambda k: k in data
        get_dat = lambda k: data[k]
    # Check in a particular order:
    suffix = '' if suffix is None else suffix.lower()
    prefix = '' if prefix is None else prefix.lower()
    (angle_key, eccen_key, x_key, y_key, z_key) = [
        next((k for k in aliases if mem_dat(prefix + k + suffix)), None)
        for aliases in [['polar_angle', 'polar angle', 'angle', 'ang', 'polang', 'theta'],
                        ['eccentricity', 'eccen', 'ecc', 'rho'],
                        ['x', 'longitude', 'lon'], ['y', 'latitude', 'lat'],
                        ['z', 'complex', 'complex-rad', 'coordinate']]]
    rad2deg = 180.0 / np.pi
    deg2rad = np.pi / 180.0
    (hpi, dpi) = (np.pi / 2.0, np.pi * 2.0)
    if angle_key and eccen_key:
        akey = prefix + angle_key + suffix
        ekey = prefix + eccen_key + suffix
        theta = np.asarray(get_dat(akey))
        rho   = np.asarray(get_dat(ekey))
        theta = theta * (deg2rad if _default_polar_angle_units[angle_key]  == 'deg' else 1)
        rho   = rho   * (rad2deg if _default_eccentricity_units[eccen_key] == 'rad' else 1)
        if _default_polar_angle_axis[angle_key] == 'UVM': theta = theta - hpi
        if _default_polar_angle_dir[angle_key] == 'cw':   theta = -theta
        ok = np.where(np.isfinite(theta))[0]
        theta[ok[theta[ok] < -np.pi]] += dpi
        theta[ok[theta[ok] >  np.pi]] -= dpi
    elif x_key and y_key:
        (x,y) = [np.asarray(get_dat(prefix + k + suffix)) for k in [x_key, y_key]]
        if _default_x_units[x_key] == 'rad': x *= rad2deg
        if _default_y_units[y_key] == 'rad': y *= rad2deg
        theta = np.arctan2(y, x)
        rho   = np.sqrt(x*x + y*y)
    elif z_key:
        z = get_dat(prefix + z_key + suffix)
        theta = np.angle(z)
        rho   = np.abs(z)
        if _default_z_units[z_key] == 'rad': rho *= rad2deg
    else:
        raise ValueError('could not identify a valid retinotopic representation in data')
    # Now, we just have to convert to the requested output style
    f = _retinotopy_style_fns[output_style]
    return f(theta, rho)

def mesh_retinotopy(m, source='any'):
    '''
    mesh_retinotopy(m) yields a dict containing a retinotopy dataset the keys 'polar_angle',
      'eccentricity', and any other related fields for the given retinotopy type; for example,
      'pRF_size' and 'variance_explained' may be included for measured retinotopy datasets and
      'visual_area' may be included for atlas or model datasets. The coordinates are always in the
      'visual' retinotopy style, but can be reinterpreted with as_retinotopy.
    mesh_retinotopy(m, source) may be used to specify a particular source for the data; this may be
      either 'empirical', 'model', or 'any'; or it may be a prefix or suffix beginning or ending with
      an _ character.
    '''
    source = source.lower()
    model_rets = ['predicted', 'model', 'template', 'atlas', 'inferred']
    empir_rets = ['empirical', 'measured', 'prf', 'data']
    wild = False
    extra_fields = {'empirical': [('variance_explained', ['varexp', 'vexpl', 'weight']),
                                  ('radius', ['size', 'prf_size', 'prf_radius'])],
                    'model':     [('visual_area', ['visual_roi', 'visual_label']),
                                  ('radius', ['size', 'radius', 'prf_size', 'prf_radius'])]}
    check_fields = []
    if source in empir_rets:
        fixes = empir_rets
        check_fields = extra_fields['empirical']
    elif source in model_rets:
        fixes = model_rets
        check_fields = extra_fields['model']
    elif source in ['any', '*', 'all']:
        fixes = model_rets + empir_rets
        check_fields = extra_fields['model'] + extra_fields['empirical']
        wild = True
    elif source in ['none', 'basic']:
        fixes = []
        check_fields = extra_fields['model'] + extra_fields['empirical']
        wild = True
    else: fixes = []
    # first, try all the fixes as prefixes then suffixes
    (z, prefix, suffix) = (None, None, None)
    if wild:
        try: z = as_retinotopy(m, 'visual')
        except: pass
    for fix in fixes:
        if z: break
        try:
            z = as_retinotopy(m, 'visual', prefix=(fix + '_'))
            prefix = fix + '_'
        except: pass
    for fix in fixes:
        if z: break
        try:
            z = as_retinotopy(m, 'visual', suffix=('_' + fix))
            suffix = fix + '_'
        except: pass
    # if none of those worked, try with no prefix/suffix
    if not z:
        try:
            z = as_retinotopy(m, 'visual', prefix=(source + '_'))
            prefix = source + '_'
        except:
            try:
                z = as_retinotopy(m, 'visual', suffix=('_' + source))
                suffix = source + '_'
            except: pass
    # if still not z... we couldn't figure it out
    if not z: raise ValueError('Could not find an interpretation for source %s' % source)
    # okay, we found it; make it into a dict
    res = {'polar_angle': z[0], 'eccentricity': z[1]}
    # check for extra fields if relevant
    pnames = {k.lower():k for k in m.property_names} if check_fields else {}
    for (fname, aliases) in check_fields:
        for f in [fname] + aliases:
            if prefix: f = prefix + f
            if suffix: f = f + suffix
            f = f.lower()
            if f in pnames: res[fname] = m.prop(pnames[f])
    # That's it
    return res

_Kay2013_pRF_data = {k.lower():v for (k,v) in {
    "V1":  {'m':0.168833, 'b':0.021791}, "V2":  {'m':0.169119, 'b':0.147386},
    "V3":  {'m':0.263966, 'b':0.342211}, "hV4": {'m':0.529626, 'b':0.445005},
    "V3a": {'m':0.357224, 'b':1.00189},  "V3b": {'m':0.357224, 'b':1.00189},
    "VO1": {'m':0.685053, 'b':0.479878}, "VO2": {'m':0.93893,  'b':0.261769},
    "LO1": {'m':0.856446, 'b':0.3614},   "LO2": {'m':0.74762,  'b':0.458872},
    "TO1": {'m':1.37441,  'b':0.172395}, "TO2": {'m':1.65694,  'b':0.0}}.iteritems()}
_pRF_data = {'kay2013': _Kay2013_pRF_data}
def predict_pRF_radius(eccentricity, visual_area='V1', source='Kay2013'):
    '''
    predict_pRF_radius(eccentricity) yields an estimate of the pRF size for a patch of cortex at the
      given eccentricity in V1.
    predict_pRF_radius(eccentricity, area) yields an estimate in the given visual area (may be given
      by the keyword visual_area).
    predict_pRF_radius(eccentricity, area, source) uses the given source to estimate the pRF size
      (may be given by the keyword source).

    The following visual areas can be specified:
      * 'V1' (default), 'V2', 'V3'
      * 'hV4'
      * 'V3a', 'V3b'
      * 'VO1', 'VO2'
      * 'LO1', 'LO2'
      * 'TO1', 'TO2'

    The following sources may be given:
      * 'Kay2013': Kay KN, Winawer J, Mezer A, Wandell BA (2013) Compressive spatial summation in
                   human visual cortex. J Neurophysiol. 110(2):481-94.
    '''
    visual_area = visual_area.lower()
    source = source.lower()
    dat = _pRF_data[source]
    adat = dat[visual_area]
    return dat['m']*eccentricity + dat['b']

def _retinotopic_field_sign_triangles(m, retinotopy):
    # get the polar angle and eccen data as a complex number in degrees
    if isinstance(retinotopy, basestring):
        (x,y) = as_retinotopy(mesh_retinotopy(m, retinotopy), 'geographical')
    elif retinotopy is Ellipsis:
        (x,y) = as_retinotopy(mesh_retinotopy(m, 'any'), 'geographical')
    else:
        (x,y) = as_retinotopy(retinotopy, 'geographical')
    # Okay, now we want to make some coordinates...
    coords = np.asarray([x, y])
    us = coords[:, m.indexed_faces[1]] - coords[:, m.indexed_faces[0]]
    vs = coords[:, m.indexed_faces[2]] - coords[:, m.indexed_faces[0]]
    (us,vs) = [np.concatenate((xs, np.full((1, m.face_count), 0.0))) for xs in [us,vs]]
    xs = np.cross(us, vs, axis=0)[2]
    xs[np.isclose(xs, 0)] = 0
    return np.sign(xs)

def retinotopic_field_sign(m, element='vertices', retinotopy=Ellipsis, invert_field=False):
    '''
    retinotopic_field_sign(mesh) yields a property array of the field sign of every vertex in the 
    mesh m; this value may not be exactly 1 (same as VF) or -1 (mirror-image) but some value
    in-between; this is because the field sign is calculated exactly (1, 0, or -1) for each triangle
    in the mesh then is average onto the vertices. To get only the triangle field signs, use
    retinotopic_field_sign(m, 'triangles').

    The following options are accepted:
      * element ('vertices') may be 'vertices' to specify that the vertex signs should be returned
        or 'triangles' (or 'faces') to specify that the triangle field signs should be returned.
      * retinotopy (Ellipsis) specifies the retinotopic dataset to be used. If se to 'empirical' or
        'predicted', the retinotopy data is auto-detected from the given categories; if set to
        Ellipsis, a property pair like 'polar_angle' and 'eccentricity' or 'lat' and 'lon' are
        searched for using the as_retinotopy function; otherwise, this may be a retinotopy dataset
        recognizable by as_retinotopy.
      * invert_field (False) specifies that the inverse of the field sign should be returned.
    '''
    tsign = _retinotopic_field_sign_triangles(m, retinotopy)
    if invert_field: tsign = -tsign
    element = element.lower()
    if element == 'triangles' or element == 'faces': return tsign
    fidx = m.vertex_face_index
    vfs = np.asarray([np.mean(tsign[ii]) if len(ii) > 0 else 0 for ii in fidx])
    return vfs    

# Tools for retinotopy model loading:
_default_schira_model = None
def get_default_schira_model():
    global _default_schira_model
    if _default_schira_model is None:
        try:
            _default_schira_model = RegisteredRetinotopyModel(
                SchiraModel(),
                registration='fsaverage_sym',
                chirality='lh',
                center=[-7.03000, -82.59000, -55.94000],
                center_right=[58.58000, -61.84000, -52.39000],
                radius=np.pi/2.5,
                method='orthographic')
        except:
            pass
    return _default_schira_model

__loaded_retinotopy_models = {}
_retinotopy_model_paths = [
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'lib', 'models')]
def retinotopy_model(name='benson17', hemi=None,
                     radius=pi/2.5, sphere_radius=100.0,
                     search_paths=None, update=False):
    '''
    retinotopy_model() yields a standard retinotopy model of V1, V2, and V3 as well as other areas
    (depending on the options). The model itself is represented as a RegisteredRetinotopyModel
    object, which may internally store a set of meshes with values at the vertices that define the
    polar angle and eccentricity, or as another object (such as with the SchiraModel). The mesh
    models are loaded from files in the neuropythy lib directory. Because the model's class is
    RegisteredRetinotopyModel, so the details of the model's 2D projection onto the cortical surface
    are included in the model.
    
    The following options may be given:
      * name (default: 'benson17') indicates the name of the model to load; the Benson17 model is
        included with the neuropythy library along with various others. If name is a filename, this
        file is loaded (must be a valid fmm or fmm.gz file). Currently, models that are included
        with neuropythy are: Benson17, Benson17-uncorrected, Schira10, and Benson14 (which is
        identical to Schira10, as Schira10 was used by Benson14).
      * hemi (default: None) specifies that the model should go with a particular hemisphere, either
        'lh' or 'rh'. Generally, model files are names lh.<model>.fmm.gz or rh.<model>.fmm.gz, but
        models intended for the fsaverage_sym don't necessarily get a prefix. Note that you can
        leave this as none and just specify that the model name is 'lh.model' instead.
      * radius, sphere_radius (defaults: pi/2.5 and 100.0, respectively) specify the radius of the
        projection (on the surface of the sphere) and the radius of the sphere (100 is the radius
        for Freesurfer spheres). See neuropythy.registration.load_fmm_model for mode details.
      * search_paths (default: None) specifies directories in which to look for fmm model files. No
        matter what is included in these files, the neuropythy library's folders are searched last.
    '''
    origname = name
    low = name.lower()
    if name in __loaded_retinotopy_models:
        return __loaded_retinotopy_models[name]
    if low in __loaded_retinotopy_models:
        return __loaded_retinotopy_models[low]
    if os.path.isfile(name):
        fname = name
        name = None
    elif low in ['schira', 'schira10', 'schira2010', 'benson14', 'benson2014']:
        return get_default_schira_model()
    else:
        for name in [origname, low]:
            name = name if hemi is None else ('%s.%s' % (hemi.lower(), name))
            if len(name) > 4 and name[-4:] == '.fmm':
                fname = name
                name = name[:-4]
            elif len(name) > 7 and name[-7:] == '.fmm.gz':
                fname = name
                name = name[:-7]
            else:
                fname = name + '.fmm'
                # Find it in the search paths...
                spaths = ([] if search_paths is None else search_paths) + _retinotopy_model_paths
            fname = next(
                (os.path.join(path, nm0)
                 for path in spaths
                 for nm0 in os.listdir(path)
                 for nm in [nm0[:-4] if len(nm0) > 4 and nm0[-4:] == '.fmm'    else \
                            nm0[:-7] if len(nm0) > 7 and nm0[-7:] == '.fmm.gz' else \
                            None]
                 if nm is not None and nm == name),
                None)
            if fname is not None: break
        if fname is None: raise ValueError('Cannot find an FFM file with the name %s' % origname)
    # Okay, load the model...
    gz = True if fname[-3:] == '.gz' else False
    lines = None
    with (gzip.open(fname, 'rb') if gz else open(fname, 'r')) as f:
        lines = f.read().split('\n')
    if len(lines) < 3 or lines[0] != 'Flat Mesh Model Version: 1.0':
        raise ValueError('Given name does not correspond to a valid flat mesh model file')
    n = int(lines[1].split(':')[1].strip())
    m = int(lines[2].split(':')[1].strip())
    reg = lines[3].split(':')[1].strip()
    hemi = lines[4].split(':')[1].strip().upper()
    center = map(float, lines[5].split(':')[1].strip().split(','))
    onxaxis = map(float, lines[6].split(':')[1].strip().split(','))
    method = lines[7].split(':')[1].strip().lower()
    tx = np.asarray(
        [map(float, row.split(','))
         for row in lines[8].split(':')[1].strip(' \t[]').split(';')])
    crds = np.asarray([map(float, left.split(','))
                       for row in lines[9:(n+9)]
                       for (left,right) in [row.split(' :: ')]])
    vals = np.asarray([map(float, right.split(','))
                       for row in lines[9:(n+9)]
                       for (left,right) in [row.split(' :: ')]])
    tris = -1 + np.asarray(
        [map(int, row.split(','))
         for row in lines[(n+9):(n+m+9)]])
    mdl = RegisteredRetinotopyModel(
        RetinotopyMeshModel(tris, crds,
                            90 - 180/pi*vals[:,0], vals[:,1], vals[:,2],
                            transform=tx),
        registration=reg,
        center=center,
        center_right=onxaxis,
        method=method,
        radius=radius,
        sphere_radius=sphere_radius,
        chirality=hemi)
    __loaded_retinotopy_models[name] = mdl
    return mdl

# Tools for retinotopy registration:
def _retinotopy_vectors_to_float(ang, ecc, wgt, weight_cutoff=0):
    (ang, ecc, wgt) = np.asarray(
        [(a,e,w) if all(isinstance(x,Number) or np.issubdtype(type(x),np.float) for x in [a,e,w]) \
                    and w > weight_cutoff else (0,0,0)
         for (a,e,w) in zip(ang, ecc, wgt)]).T
    #wgt = np.clip((wgt - weight_cutoff) / (1.0 - weight_cutoff), 0, 1)
    wgt[wgt <= weight_cutoff] = 0
    return (ang, ecc, wgt)

def retinotopy_mesh_field(mesh, mdl,
                          polar_angle=None, eccentricity=None, weight=None,
                          weight_cutoff=0, scale=1, sigma=None, shape=2, suffix=None,
                          max_eccentricity=Ellipsis,
                          max_polar_angle=180,
                          angle_type='both',
                          exclusion_threshold=None):
    '''
    mesh_field_spec(mesh, model) yields a list that can be used with mesh_register as a potential
    term. This should generally be used in a similar fashion to retinotopy_anchors.

    Options:
      * polar_angle (default None) specifies that the given data should be used in place of the
        'polar_angle' or 'PRF_polar_angle'  property values. The given argument must be numeric and
        the same length as the the number of vertices in the mesh. If None is given, then the
        property value of the mesh is used; if a list is given and any element is None, then the
        weight for that vertex is treated as a zero. If the option is a string, then the property
        value with the same name isused as the polar_angle data.
      * eccentricity (default None) specifies that the given data should be used in places of the
        'eccentricity' or 'PRF_eccentricity' property values. The eccentricity option is handled 
        virtually identically to the polar_angle option.
      * weight (default None) specifies that the weight or scale of the data; this is handled
        generally like the polar_angle and eccentricity options, but may also be 1, indicating that
        all vertices with polar_angle and eccentricity values defined will be given a weight of 1.
        If weight is left as None, then the function will check for 'weight',
        'variance_explained', 'PRF_variance_explained', and 'retinotopy_weight' values and will use
        the first found (in that order). If none of these is found, then a value of 1 is assumed.
      * weight_cutoff (default 0) specifies that the weight must be higher than the given value inn
        order to be included in the fit; vertices with weights below this value have their weights
        truncated to 0.
      * scale (default 1) specifies a constant by which to multiply all weights for all anchors; the
        value None is interpreted as 1.
      * shape (default 2.0) specifies the exponent in the harmonic function.
      * sigma (default None) specifies, if given as a number, the sigma parameter of the Gaussian
        potential function; if sigma is None, however, the potential function is harmonic.
      * suffix (default None) specifies any additional arguments that should be appended to the 
        potential function description list that is produced by this function; i.e., the 
        retinotopy_anchors function produces a list, and the contents of suffix, if given and not
        None, are appended to that list (see mesh_register).
      * max_eccentricity (default Ellipsis) specifies how the eccentricity portion of the potential
        field should be normalized. Specifically, in order to ensure that polar angle and
        eccentricity contribute roughly equally to the potential, this should be approximately the
        max eccentricity appearing in the data on the mesh. If the argument is the default then the
        actual max eccentricity will be used.
      * max_polar_angle (default: 180) is used the same way as the max_eccentricity function, but if
        Ellipsis is given, the value 180 is always assumed regardless of measured data.
      * exclusion_threshold (default None) specifies that if the initial norm of a vertex's gradient
        is greater than exclusion_threshold * std + median (where std and median are calculated over
        the vertices with non-zero gradients) then its weight is set to 0 and it is not kept as part
        of the potential field.
      * angle_type (default: None) specifies that only one type of angle should be included in the
        mesh; this may be one of 'polar', 'eccen', 'eccentricity', 'angle', or 'polar_angle'. If
        None, then both polar angle and eccentricity are included.

    Example:
     # The retinotopy_anchors function is intended for use with mesh_register, as follows:
     # Define our Schira Model:
     model = neuropythy.retinotopy_model()
     # Make sure our mesh has polar angle, eccentricity, and weight data:
     mesh.prop('polar_angle',  polar_angle_vertex_data);
     mesh.prop('eccentricity', eccentricity_vertex_data);
     mesh.prop('weight',       variance_explained_vertex_data);
     # register the mesh using the retinotopy and model:
     registered_mesh = neuropythy.registration.mesh_register(
        mesh,
        ['mesh', retinotopy_mesh_field(mesh, model)],
        max_step_size=0.05,
        max_steps=2000)
    '''
    if isinstance(mdl, basestring):
        mdl = retinotopy_model(mdl)
    if not isinstance(mdl, RetinotopyMeshModel):
        if isinstance(mdl, RegisteredRetinotopyModel):
            mdl = mdl.model
        if not isinstance(mdl, RetinotopyMeshModel):
            raise RuntimeError('given model is not a RetinotopyMeshModel instance!')
    if not hasattr(mdl, 'data') or 'polar_angle' not in mdl.data or 'eccentricity' not in mdl.data:
        raise ValueError('Retinotopy model does not have polar angle and eccentricity data')
    if not isinstance(mesh, CorticalMesh):
        raise RuntimeError('given mesh is not a CorticalMesh object!')
    n = mesh.vertex_count
    X = mesh.coordinates.T
    if weight_cutoff is None: weight_cutoff = 0
    # make sure we have our polar angle/eccen/weight values:
    # (weight is odd because it might be a single number, so handle that first)
    (polar_angle, eccentricity, weight) = [
        extract_retinotopy_argument(mesh, name, arg, default='empirical')
        for (name, arg) in [
                ('polar_angle', polar_angle),
                ('eccentricity', eccentricity),
                ('weight', [weight for i in range(n)] \
                           if isinstance(weight, Number) or np.issubdtype(type(weight), np.float) \
                           else weight)]]
    # Make sure they contain no None/invalid values
    (polar_angle, eccentricity, weight) = _retinotopy_vectors_to_float(
        polar_angle, eccentricity, weight,
        weight_cutoff=weight_cutoff)
    idcs = [i for (i,w) in enumerate(weight) if w > 0]
    # Okay, let's get the model data ready
    mdl_1s = np.ones(mdl.forward.coordinates.shape[0])
    mdl_coords = np.dot(mdl.transform, np.vstack((mdl.forward.coordinates.T, mdl_1s)))[:2].T
    mdl_faces  = mdl.forward.triangles
    mdl_data   = np.asarray([mdl.data['polar_angle'], mdl.data['eccentricity']])
    # Get just the relevant weights and the scale
    wgts = weight[idcs] * (1 if scale is None else scale)
    # and the relevant polar angle/eccen data
    msh_data = np.asarray([polar_angle, eccentricity])[:,idcs]
    # format shape correctly
    shape = np.full((len(idcs)), float(shape), dtype=np.float32)
    # Last thing before constructing the field description: normalize both polar angle and eccen to
    # cover a range of 0-1:
    if max_eccentricity is Ellipsis: max_eccentricity = np.max(msh_data[1])
    if max_polar_angle  is Ellipsis: max_polar_angle  = 180
    if max_polar_angle is not None:
        msh_data[0] /= max_polar_angle
        mdl_data[0] /= max_polar_angle
    if max_eccentricity is not None:
        msh_data[1] /= max_eccentricity
        mdl_data[1] /= max_eccentricity
    # Check if we are making an eccentricity-only or a polar-angle-only field:
    if angle_type is not None:
        angle_type = angle_type.lower()
        if angle_type != 'both' and angle_type != 'all':
            convert = {'eccen':'eccen', 'eccentricity':'eccen', 'radius':'eccen',
                       'angle':'angle', 'polar_angle': 'angle', 'polar': 'angle'}
            angle_type = convert[angle_type]
            mdl_data = [mdl_data[0 if angle_type == 'angle' else 1]]
            msh_data = [msh_data[0 if angle_type == 'angle' else 1]]
    # okay, we've partially parsed the data that was given; now we can construct the final list of
    # instructions:
    if sigma is None:
        field_desc = ['mesh-field', 'harmonic', mdl_coords, mdl_faces, mdl_data, idcs, msh_data,
                      'scale', wgts, 'order', shape]
    else:
        if not hasattr(sigma, '__iter__'): sigma = [sigma for _ in wgts]
        field_desc = ['mesh-field', 'gaussian', mdl_coords, mdl_faces, mdl_data, idcs, msh_data,
                      'scale', wgts, 'order', shape, 'sigma', sigma]
    if suffix is not None: field_desc += suffix
    # now, if we want to exclude outliers, we do so here:
    if exclusion_threshold is not None:
        jpe = java_potential_term(mesh, field_desc)
        jcrds = to_java_doubles(mesh.coordinates)
        jgrad = to_java_doubles(np.zeros(mesh.coordinates.shape))
        jpe.calculate(jcrds,jgrad)
        gnorms = np.sum((np.asarray([[x for x in row] for row in jgrad])[:, idcs])**2, axis=0)
        gnorms_pos = gnorms[gnorms > 0]
        mdn = np.median(gnorms_pos)
        std = np.std(gnorms_pos)
        gn_idcs = np.where(gnorms > mdn + std*3.5)[0]
        for i in gn_idcs: wgts[i] = 0;
    return field_desc

        
def retinotopy_anchors(mesh, mdl,
                       polar_angle=None, eccentricity=None,
                       weight=None, weight_cutoff=0.1,
                       field_sign=None,
                       field_sign_weight=0,
                       model_field_sign=None,
                       model_hemi=Ellipsis,
                       scale=1,
                       shape='Gaussian', suffix=None,
                       sigma=[0.05, 1.0, 2.0],
                       select='close'):
    '''
    retinotopy_anchors(mesh, model) is intended for use with the mesh_register function and the
    retinotopy_model() function and/or the RetinotopyModel class; it yields a description of the
    anchor points that tie relevant vertices the given mesh to points predicted by the given model
    object. Any instance of the RetinotopyModel class should work as a model argument; this includes
    SchiraModel objects as well as RetinotopyMeshModel objects such as those returned by the
    retinotopy_model() function. If the model given is a string, then it is passed to the
    retinotopy_model() function first.

    Options:
      * polar_angle (default None) specifies that the given data should be used in place of the
        'polar_angle' or 'PRF_polar_angle'  property values. The given argument must be numeric and
        the same length as the the number of vertices in the mesh. If None is given, then the
        property value of the mesh is used; if a list is given and any element is None, then the
        weight for that vertex is treated as a zero. If the option is a string, then the property
        value with the same name isused as the polar_angle data.
      * eccentricity (default None) specifies that the given data should be used in places of the
        'eccentricity' or 'PRF_eccentricity' property values. The eccentricity option is handled 
        virtually identically to the polar_angle option.
      * weight (default None) specifies that the weight or scale of the data; this is handled
        generally like the polar_angle and eccentricity options, but may also be 1, indicating that
        all vertices with polar_angle and eccentricity values defined will be given a weight of 1.
        If weight is left as None, then the function will check for 'weight',
        'variance_explained', 'PRF_variance_explained', and 'retinotopy_weight' values and will use
        the first found (in that order). If none of these is found, then a value of 1 is assumed.
      * weight_cutoff (default 0) specifies that the weight must be higher than the given value inn
        order to be included in the fit; vertices with weights below this value have their weights
        truncated to 0.
      * scale (default 1) specifies a constant by which to multiply all weights for all anchors; the
        value None is interpreted as 1.
      * shape (default 'Gaussian') specifies the shape of the potential function (see mesh_register)
      * suffix (default None) specifies any additional arguments that should be appended to the 
        potential function description list that is produced by this function; i.e., the 
        retinotopy_anchors function produces a list, and the contents of suffix, if given and not
        None, are appended to that list (see mesh_register).
      * select (default 'close') specifies a function that will be called with two arguments for
        every vertex given an anchor; the arguments are the vertex label and the matrix of anchors.
        The function should return a list of anchors to use for the label (None is equivalent to
        lambda id,anc: anc). The parameter may alternately be specified using the string 'close':
        select=['close', [k]] indicates that any anchor more than k times the average edge-length in
        the mesh should be excluded; a value of just ['close', k] on the other hand indicates that
        any anchor more than k distance from the vertex should be exlcuded. The default value,
        'close', is equivalent to ['close', [40]].
      * sigma (default [0.05, 1.0, 2.0]) specifies how the sigma parameter should be handled; if
        None, then no sigma value is specified; if a single number, then all sigma values are
        assigned that value; if a list of three numbers, then the first is the minimum sigma value,
        the second is the fraction of the minimum distance between paired anchor points, and the 
        last is the maximum sigma --- the idea with this form of the argument is that the ideal
        sigma value in many cases is approximately 0.25 to 0.5 times the distance between anchors
        to which a single vertex is attracted; for any anchor a to which a vertex u is attracted,
        the sigma of a is the middle sigma-argument value times the minimum distance from a to all
        other anchors to which u is attracted (clipped by the min and max sigma).

    Example:
     # The retinotopy_anchors function is intended for use with mesh_register, as follows:
     # Define our Schira Model:
     model = neuropythy.registration.SchiraModel()
     # Make sure our mesh has polar angle, eccentricity, and weight data:
     mesh.prop('polar_angle',  polar_angle_vertex_data);
     mesh.prop('eccentricity', eccentricity_vertex_data);
     mesh.prop('weight',       variance_explained_vertex_data);
     # register the mesh using the retinotopy and model:
     registered_mesh = neuropythy.registration.mesh_register(
        mesh,
        ['mesh', retinotopy_anchors(mesh, model)],
        max_step_size=0.05,
        max_steps=2000)
    '''
    if isinstance(mdl, basestring):
        hemi = None
        if model_hemi is Ellipsis:
            md = mesh.meta_data
            sub = md.get('subject', None)
            hemi_obj = md.get('hemisphere', None)
            hemi = None               if sub      and sub.name == 'fsaverage_sym'  else \
                   hemi_obj.chirality if hemi_obj and isinstance(hemi, Hemisphere) else \
                   hemi_obj           if isinstance(hemi_obj, basestring)          else \
                   None
        elif model_hemi is None:
            hemi = None
        elif isinstance(model_hemi, basestring):
            model_hemi = model_hemi.upper()
            hemnames = {k:h
                        for (h,als) in [('LH', ['LH','L','LEFT','RHX','RX']),
                                        ('RH', ['RH','R','RIGHT','LHX','LX'])]
                        for k in als}
            if model_hemi in hemnames: hemi = hemnames[model_hemi]
            else: raise ValueError('Unrecognized hemisphere name: %s' % model_hemi)
        else:
            raise ValueError('model_hemi must be a string, Ellipsis, or None')
        mdl = retinotopy_model(mdl, hemi=hemi)
    if not isinstance(mdl, RetinotopyModel):
        raise RuntimeError('given model is not a RetinotopyModel instance!')
    if not isinstance(mesh, CorticalMesh):
        raise RuntimeError('given mesh is not a CorticalMesh object!')
    n = mesh.vertex_count
    X = mesh.coordinates.T
    if weight_cutoff is None: weight_cutoff = 0
    # make sure we have our polar angle/eccen/weight values:
    # (weight is odd because it might be a single number, so handle that first)
    (polar_angle, eccentricity, weight) = [
        extract_retinotopy_argument(mesh, name, arg, default='empirical')
        for (name, arg) in [
                ('polar_angle', polar_angle),
                ('eccentricity', eccentricity),
                ('weight', [weight for i in range(n)] \
                           if isinstance(weight, Number) or np.issubdtype(type(weight), np.float) \
                           else weight)]]
    # Make sure they contain no None/invalid values
    (polar_angle, eccentricity, weight) = _retinotopy_vectors_to_float(
        polar_angle, eccentricity, weight,
        weight_cutoff=weight_cutoff)
    idcs = [i for (i,w) in enumerate(weight) if w > 0]
    # Interpret the select arg if necessary (but don't apply it yet)
    select = ['close', [40]] if select == 'close'   else \
             ['close', [40]] if select == ['close'] else \
             select
    if select is None:
        select = lambda a,b: b
    elif isinstance(select, list) and len(select) == 2 and select[0] == 'close':
        d = np.mean(mesh.edge_lengths)*select[1][0] if isinstance(select[1], list) else select[1]
        select = lambda idx,ancs: [a for a in ancs if a[0] is not None if norm(X[idx] - a) < d]
    # Okay, apply the model:
    res = mdl.angle_to_cortex(polar_angle[idcs], eccentricity[idcs])
    # Organize the data; trim out those not selected
    data = [[[i for _ in r], r, [ksidx[tuple(a)] for a in r]]
            for (i,r0) in zip(idcs, res)
            if r0[0] is not None
            for ksidx in [{tuple(a):k for (k,a) in enumerate(r0)}]
            for r in [select(i, r0)]
            if len(r) > 0]
    # Flatten out the data into arguments for Java
    idcs = [int(i) for d in data for i in d[0]]
    ancs = np.asarray([pt for d in data for pt in d[1]]).T
    labs = np.asarray([ii for d in data for ii in d[2]]).T
    # Get just the relevant weights and the scale
    wgts = np.asarray(weight[idcs] * (1 if scale is None else scale))
    # add in the field-sign weights if requested here
    if not np.isclose(field_sign_weight, 0) and model_field_sign is not None:
        if field_sign is True or field_sign is Ellipsis or field_sign is None:
            field_sign = retinotopic_field_sign(mesh, retinotopy={'polar_angle':  polar_angle,
                                                                  'eccentricity': eccentricity})
        elif isinstance(field_sign, basestring): field_sign = mesh.prop(field_sign)
        field_sign = np.asarray(field_sign)
        fswgts = 1.0 - 0.25 * np.asarray([(fs - model_field_sign[l+1])
                                          for (l,fs) in zip(labs, field_sign[idcs])])**2
        wgts *= fswgts * field_sign_weight + (1 - field_sign_weight)
    # Figure out the sigma parameter:
    if sigma is None: sigs = None
    elif isinstance(sigma, Number) or np.issubdtype(type(sigma), np.float): sigs = sigma
    elif hasattr(sigma, '__iter__') and len(sigma) == 3:
        [minsig, mult, maxsig] = sigma
        sigs = np.clip(
            [mult*min([norm(a0 - a) for a in anchs if a is not a0]) if len(iii) > 1 else maxsig
             for (iii,anchs,_) in data
             for a0 in anchs],
            minsig, maxsig)
    else:
        raise ValueError('sigma must be a number or a list of 3 numbers')
    # okay, we've partially parsed the data that was given; now we can construct the final list of
    # instructions:
    tmp =  (['anchor', shape,
             np.asarray(idcs, dtype=np.int),
             np.asarray(ancs, dtype=np.float64),
             'scale', np.asarray(wgts, dtype=np.float64)]
            + ([] if sigs is None else ['sigma', sigs])
            + ([] if suffix is None else suffix))
    return tmp

def register_retinotopy_initialize(hemi,
                                   model='benson17', model_hemi=Ellipsis,
                                   polar_angle=None, eccentricity=None, weight=None,
                                   weight_cutoff=0.1,
                                   max_predicted_eccen=85,
                                   partial_voluming_correction=True,
                                   prior='retinotopy',
                                   resample=Ellipsis,
                                   max_area=None,
                                   max_eccentricity=None):
    '''
    register_retinotopy_initialize(hemi, model) yields an fsaverage or fsaverage_sym hemisphere that
    has been prepared for retinotopic registration with the data on the given hemisphere, hemi. The
    options polar_angle, eccentricity, weight, and weight_cutoff are accepted, as are the
    prior and resample options; all are documented in help(register_retinotopy).
    The return value of this function is actually a dictionary with the element 'map' giving the
    resulting map projection, and additional entries giving other meta-data calculated along the
    way. Note that the hemisphere will only be fsaverage_sym if the option model_hemi is set to
    None.
    '''
    # Step 0: Initialization of variables ##########################################################
    prop_names = ['polar_angle', 'eccentricity', 'weight']
    data = {}  # the map we build up in this function
    n = hemi.vertex_count
    # Step 1: get our properties straight ##########################################################
    (ang, ecc, wgt) = [
        extract_retinotopy_argument(hemi, name, arg, default='empirical')
        for (name, arg) in [
                ('polar_angle', polar_angle),
                ('eccentricity', eccentricity),
                ('weight', [weight for i in range(n)] \
                           if isinstance(weight, Number) or np.issubdtype(type(weight), np.float) \
                           else weight)]]
    # we also want to make sure weight is 0 where there are none values
    (ang, ecc, wgt) = _retinotopy_vectors_to_float(ang, ecc, wgt, weight_cutoff=weight_cutoff)
    # if there's a max eccentricity, apply that to the weights
    if max_eccentricity is not None:
        wgt = np.array(wgt)
        wgt[ecc > max_eccentricity] = 0
    # correct for partial voluming if necessary:
    if partial_voluming_correction is True: wgt *= (1.0 - np.asarray(hemi.partial_volume_factor()))
    # note these in the result dictionary:
    data['sub_polar_angle'] = ang
    data['sub_eccentricity'] = ecc
    data['sub_weight'] = wgt
    if hemi.has_property('curvature'):
        data['sub_curvature'] = hemi.prop('curvature')
    else:
        data['sub_curvature'] = np.zeros((len(ang),))
    # Step 2: do alignment, if required ############################################################
    if isinstance(model, basestring):
        h = hemi.name.lower() if model_hemi is Ellipsis else \
            None              if model_hemi is None     else \
            model_hemi
        model = retinotopy_model(model, hemi=h)
    if not isinstance(model, RegisteredRetinotopyModel):
        raise ValueError('model must be a RegisteredRetinotopyModel')
    data['model'] = model
    model_reg = model.projection_data['registration']
    model_reg = 'fsaverage_sym' if model_reg is None else model_reg
    model_chirality = model.projection_data['chirality']
    if model_reg == 'fsaverage_sym':
        proj_from_hemi = hemi if hemi.chirality == 'LH' else hemi.subject.RHX
    else:
        if model_chirality is not None and hemi.chirality != model_chirality:
            raise ValueError('Inverse-chirality hemisphere cannot be registered to model')
        proj_from_hemi = hemi
    # make sure we are registered to the model space
    if model_reg not in proj_from_hemi.topology.registrations:
        raise ValueError('Hemisphere is not registered to the model registration: %s' % model_reg)
    # give this hemisphere the correct data
    proj_from_hemi = proj_from_hemi.using(
        properties=proj_from_hemi.properties.using(
            polar_angle=ang,
            eccentricity=ecc,
            weight=wgt))
    data['project_from_hemi'] = proj_from_hemi
    # note the subject's registration to the model's registration:
    subreg = proj_from_hemi.topology.registrations[model_reg]
    ## if there's a prior, we should enforce it now:
    if prior is None:
        prior_hemi = None
        coords = subreg.coordinates
    else:
        if hemi.subject.id == model_reg or model_reg == 'native':
            prior_subject = proj_from_hemi.subject
            prior_hemi = proj_from_hemi
        else:
            prior_subject = freesurfer_subject(model_reg)
            prior_hemi = getattr(prior_subject, proj_from_hemi.chirality)
        if prior != 'native' and prior not in prior_hemi.topology.registrations:
            raise ValueError('Prior registration %s not found in prior subject %s' \
                             % (prior, model_reg))
        elif model_reg != 'native' and model_reg not in prior_hemi.topology.registrations:
            raise ValueError('Model registratio not found in prior subject: %s' % prior_subject)
        prior_reg0 = prior_hemi.topology.registrations[model_reg]
        prior_reg1 = prior_hemi.topology.registrations[prior]
        addr = prior_reg0.address(subreg.coordinates)
        data['address_in_prior'] = addr
        coords = prior_reg1.unaddress(addr)
    prior_reg = Registration(proj_from_hemi.topology, coords)
    data['prior_registration'] = prior_reg
    data['prior_hemisphere'] = prior_hemi
    # Step 3: resample, if need be
    if resample is Ellipsis:
        resample = 'fsaverage_sym' if model_hemi is None else 'fsaverage'
    data['resample'] = resample
    if resample is None:
        tohem = proj_from_hemi
        toreg = prior_reg
        data['initial_registration'] = prior_reg
        for p in prop_names:
            data['initial_' + p] = data['sub_' + p]
        data['initial_curvature'] = data['sub_curvature']
        data['unresample_function'] = lambda rr: rr
    else:
        if resample == 'fsaverage_sym':
            tohem = freesurfer_subject('fsaverage_sym').LH
            toreg = tohem.topology.registrations['fsaverage_sym']
        elif resample == 'fsaverage':
            tohem = getattr(freesurfer_subject('fsaverage'), model_chirality)
            toreg = tohem.topology.registrations['fsaverage']
        else:
            raise ValueError('resample argument must be fsaverage, fsaverage_sym, or None')
        data['resample_hemisphere'] = tohem
        resamp_addr = toreg.address(prior_reg.coordinates)
        data['resample_address'] = resamp_addr
        data['initial_registration'] = toreg
        for (p,v) in zip(prop_names,
                         _retinotopy_vectors_to_float(
                             *[toreg.interpolate_from(prior_reg, data['sub_' + p])
                               for p in prop_names])):
            data['initial_' + p] = v
        data['initial_curvature'] = toreg.interpolate_from(prior_reg, data['sub_curvature'])
        data['unresample_function'] = lambda rr: Registration(proj_from_hemi.topology,
                                                              rr.unaddress(resamp_addr))
    data['initial_mesh'] = tohem.registration_mesh(toreg)
    # Step 4: make the projection
    proj_data = model.projection_data
    if resample is None:
        proj_data = proj_from_hemi.projection_data(center=proj_data['center'],
                                                   center_right=proj_data['center_right'],
                                                   method=proj_data['method'],
                                                   registration=proj_data['registration'],
                                                   radius=proj_data['radius'])
    m = proj_data['forward_function'](data['initial_mesh'])
    for p in prop_names:
        m.prop(p, data['initial_' + p][m.vertex_labels])
    m.prop('curvature', data['initial_curvature'][m.vertex_labels])
    data['map'] = m
    # Step 5: Annotate how we get back
    def __postproc_fn(reg):
        d = data.copy()
        d['registered_coordinates'] = reg
        # First, unproject the map
        reg_map_3dx = d['map'].unproject(reg).T
        reg_3dx = np.array(d['initial_registration'].coordinates, copy=True)
        reg_3dx[d['map'].vertex_labels] = reg_map_3dx
        final_reg = Registration(tohem.topology, reg_3dx)
        d['finished_registration'] = final_reg
        # Now, if need be, unresample the points:
        d['registration'] = d['unresample_function'](final_reg)
        # now convert the sub points into retinotopy points
        rmesh = proj_from_hemi.registration_mesh(d['registration'])
        pred = np.asarray(
            [((p,e,l)
              if r != 0 and (max_area is None or r <= max_area) and e <= max_predicted_eccen else
              (0.0, 0.0, 0))
             for (p,e,l) in zip(*model.cortex_to_angle(rmesh))
             for r in [abs(round(l))]]).T
        pred = (np.asarray(pred[0], dtype=np.float32),
                np.asarray(pred[1], dtype=np.float32),
                np.asarray(pred[2], dtype=np.int32))
        for i in (0,1,2): pred[i].flags.writeable = False
        pred = make_dict({p:v for (p,v) in zip(['polar_angle','eccentricity','visual_area'], pred)})
        d['prediction'] = pred
        rmesh.prop(pred)
        d['registered_mesh'] = rmesh
        return make_dict(d)
    data['postprocess_function'] = __postproc_fn
    return data

def register_retinotopy(hemi,
                        model='benson17', model_hemi=Ellipsis,
                        polar_angle=None, eccentricity=None, weight=None, weight_cutoff=0.1,
                        max_eccentricity=None,
                        partial_voluming_correction=True,
                        edge_scale=1.0, angle_scale=1.0, functional_scale=1.0,
                        edge_max_compression=0.25, edge_max_stretch=3.0,
                        sigma=Ellipsis,
                        select='close',
                        prior='retinotopy',
                        resample=Ellipsis,
                        max_steps=2000, max_step_size=0.05, method='random',
                        max_predicted_eccen=90,
                        return_meta_data=False,
                        mutate_hemi=Ellipsis):
    '''
    register_retinotopy(hemi) registers the given hemisphere object, hemi, to a model of V1, V2,
      and V3 retinotopy, and yields a copy of hemi that is identical but additionally contains
      the registration 'retinotopy', whose coordinates are aligned with the model.

    Registration attempts to align the vertex positions of the hemisphere's spherical surface with a
    model of polar angle and eccentricity. This alignment proceeds through several steps and can
    be modified by several options. A description of these steps and options are provided here. For
    most cases, the default options should work relatively well.

    Method:
      (1) Prepare for registration by running neuropythy.vision.register_retinotopy_initialize. This
          function runs through a number of substeps:
            a. Extract the polar angle, eccentricity and weight data from the hemisphere. These
               data are usually properties on the mesh and can be modifies by the options
               polar_angle, eccentricity, and weight, which can be either property names or list
               of property values. By default (None), a property is chosen using the functions
               neuropythy.vision.extract_retinotopy_argument with the default option set to
               'empirical'.
            b. If partial voluming correction is enabled (via the option
               partial_voluming_correction), multiply the weight by (1 - p) where p is 
               hemi.partial_volume_factor().
            c. If there is a prior that is specified as a belief about the retinotopy, then a
               Registration is created for the hemisphere such that its vertices are arranged
               according to that prior (see also the prior option). Note that because hemi's
               coordinates must always be projected into the registration specified by the model,
               the prior must be the name of a registration to which the model's specified subject
               is also registered. This is clear in the case of an example. The default value for
               this is 'retinotopy'; assuming that our model is specified on the fsaverage_sym, 
               surface, the initial positions of the coordinates for the registration process would
               be the result of starting with hemi's fsaverage_sym-aligned coordinates then warping
               these coordinates in a way that is equivalent to the warping from fsaverage_sym's 
               native spherical coordinates to fsaverage_sym's retinotopy registration coordinates.
               Note that the retinotopy registration would usually be specified in a file in the
               fsaverage_sym subject's surf directory: surf/lh.retinotopy.sphere.reg.
               If no prior is specified (option value None), then the vertices that are used are
               those aligned with the registration of the model, which will usually be 'fsaverage'
               or 'fsaverage_sym'.
            d. If the option resample is not None, then the vertex coordinates are resampled onto
               either the fsaverage or fsaverage_sym's native sphere surface. (The value of resample
               should be either 'fsaverage' or 'fsaverage_sym'.) Resampling can prevent vertices
               that have been rearranged by alignment with the model's specified registration or by
               application of a prior from beginning the alignment with very high initial gradients
               and is recommended for subject alignments.
               If resample is None then no changes are made.
            e. A 2D projection of the (possibly aligned, prior-warped, and resampled) cortical
               surface is made according to the projection parameters of the model. This map is the
               mesh that is warped to eventually fit the model.
      (2) Perform the registration by running neuropythy.registration.mesh_register. This step
          consists of two major components.
            a. Create the potential function, which we will minimize. The potential function is a
               complex function whose inputs are the coordinates of all of the vertices and whose
               output is a potential value that increases both as the mesh is warped and as the
               vertices with retinotopy predictions get farther away from the positions in the model
               that their retinotopy values would predict they should lie. The balance of these
               two forces is best controlled by the option functional_scale. The potential function
               fundamentally consists of four terms; the first three describe mesh deformations and
               the last describes the model fit.
                - The edge deformation term is described for any vertices u and v that are connected
                  by an edge in the mesh; it's value is c/p (r(u,v) - r0(u,v))^2 where c is the
                  edge_scale, p is the number of edges in the mesh, r(a,b) is the distance between
                  vertices a and b, and r0(a,b) is the distance between a and b in the initial mesh.
                - The angle deformation term is described for any three vertices (u,v,w) that form
                  an angle in the mesh; its value is c/m h(t(u,v,w), t0(u,v,w)) where c is the
                  angle_scale argument, m is the number of angles in the mesh, t is the value of the
                  angle (u,v,w), t0 is the value of the angle in the initial mesh, and h(t,t0) is an
                  infinite-well function that asymptotes to positive infinity as t approaches both 0
                  and pi and is minimal when t = t0 (see the nben's 
                  nben.mesh.registration.InfiniteWell documentation for more details).
                - The perimeter term prevents the perimeter vertices form moving significantly;
                  this primarily prevents the mesh from wrapping in on itself during registration.
                  The form of this term is, for any vertex u on the mesh perimeter, 
                  (x(u) - x0(u))^2 where x and x0 are the position and initial position of the
                  vertex.
                - Finally, the functional term is minimized when the vertices best align with the
                  retinotopy model.
            b. Register the mesh vertices to the potential function using the nben Java library. The
               particular parameters of the registration are method, max_steps, and max_step_size.

    Options:
      * model specifies the instance of the retinotopy model to use; this must be an
        instance of the RegisteredRetinotopyModel class or a string that can be passed to the
        retinotopy_model() function (default: 'standard').
      * model_hemi specifies the hemisphere of the model; generally you shouldn't have to set this
        unless you are using an fsaverage_sym model, in which case it should be set to None; in all
        other cases, the default value (Ellipsis) instructs the function to auto-detect the
        hemisphere.
      * polar_angle, eccentricity, and weight specify the property names for the respective
        quantities; these may alternately be lists or numpy arrays of values. If weight is not given
        or found, then unity weight for all vertices is assumed. By default, each will check the
        hemisphere's properties for properties with compatible names; it will prefer the properties
        PRF_polar_angle, PRF_ecentricity, and PRF_variance_explained if possible.
      * weight_cutoff specifies the minimum value a vertex must have in the weight property in order
        to be considered as retinotopically relevant.
      * max_eccentricity (default: None) specifies that any vertex whose eccentricity is too high
        should be given a weight of 0 in the registration.
      * partial_voluming_correction (default: True), if True, specifies that the value
        (1 - hemi.partial_volume_factor()) should be applied to all weight values (i.e., weights
        should be down-weighted when likely to be affected by a partial voluming error).
      * sigma specifies the standard deviation of the Gaussian shape for the Schira model anchors;
        see retinotopy_anchors for more information.
      * edge_scale, angle_scale, and functional_scale all specify the relative strengths of the
        various components of the potential field (functional_scale refers to the strength of the
        retinotopy model).
      * select specifies the select option that should be passed to retinotopy_anchors.
      * max_steps (default 30,000) specifies the maximum number of registration steps to run.
      * max_step_size (default 0.05) specifies the maxmim distance a single vertex is allowed to
        move in a single step of the minimization.
      * edge_max_compression (default 0.25) specifies the minimum fraction of its length that an
        edge should be allowed to be compressed to.
      * edge_max_stretch (default 3.0) specifies the maximum fraction of its length that an edge
        should be allowed to be stretched to.
      * method (default 'random') is the method argument passed to mesh_register. This should be
        'random', 'pure', or 'nimble'. Generally, 'random' is recommended.
      * return_meta_data (default: False) specifies whether the return value should be the new
        Registration object or a dictionary of meta-data that was used during the registration
        calculations, in which the key 'registation' gives the registration object.
      * radius (default: pi/3) specifies the radius, in radians, of the included portion of the map
        projection (projected about the occipital pole).
      * sigma (default Ellipsis) specifies the sigma argument to be passed onto the 
        retinotopy_anchors function (see help(retinotopy_anchors)); the default value, Ellipsis,
        is interpreted as the default value of the retinotopy_anchors function's sigma option.
      * max_predicted_eccen (default: 85) specifies the maximum eccentricity that should appear in
        the predicted retinotopy values.
      * prior (default: 'retinotopy') specifies the prior that should be used, if found, in the 
        topology registrations for the subject associated with the retinotopy_model's registration.
      * resample (default: Ellipsis) specifies that the data should be resampled to one of
        the uniform meshes, 'fsaverage' or 'fsaverage_sym', prior to registration; if None then no
        resampling is performed; if Ellipsis, then auto-detect either fsaverage or fsaverage_sym
        based on the model_hemi option (if it is None, fsaverage_sym, else fsaverage).
    '''
    # Step 1: prep the map for registration--figure out what properties we're using...
    model = retinotopy_model()      if model is None                 else \
            retinotopy_model(model) if isinstance(model, basestring) else \
            model
    data = register_retinotopy_initialize(hemi,
                                          model=model,
                                          model_hemi=model_hemi,
                                          polar_angle=polar_angle,
                                          eccentricity=eccentricity,
                                          weight=weight,
                                          weight_cutoff=weight_cutoff,
                                          max_eccentricity=max_eccentricity,
                                          partial_voluming_correction=partial_voluming_correction,
                                          max_predicted_eccen=max_predicted_eccen,
                                          prior=prior, resample=resample)
    # Step 2: run the mesh registration
    if max_steps == 0:
        r = data['map'].coordinates
    else:
        elens = data['map'].edge_lengths
        if edge_max_compression is None and edge_max_stretch is None:
            edge_well_potential = []
        else: 
            emin = 0 if edge_max_compression is None else edge_max_compression * elens
            emax = (10**6) * elens if edge_max_stretch is None else edge_max_stretch * elens
            edge_well_potential = [['edge', 'infinite-well', 'min', emin, 'max', emax]]
        r = mesh_register(
            data['map'],
            #edge_well_potential + [
            [#['angle',     'infinite-well'],
             ['edge',      'harmonic-log', 'scale', edge_scale],
             ['angle',     'harmonic-log', 'scale', angle_scale],
             ['perimeter', 'harmonic'],
             retinotopy_anchors(data['map'], model,
                                polar_angle='polar_angle',
                                eccentricity='eccentricity',
                                weight='weight',
                                weight_cutoff=0, # taken care of above
                                scale=functional_scale,
                                select=select,
                                **({} if sigma is Ellipsis else {'sigma':sigma}))],
            method=method,
            max_steps=max_steps,
            max_step_size=max_step_size)
    # Step 3: run the post-processing function
    postproc = data['postprocess_function']
    ppr = postproc(r)
    return ppr if return_meta_data else ppr['registered_mesh']

# Tools for registration-free retinotopy prediction:
_retinotopy_templates = {}
def predict_retinotopy(sub, template='benson17'):
    '''
    predict_retinotopy(subject) yields a pair of dictionaries each with three keys: polar_angle,
    eccentricity, and v123roi; each of these keys maps to a numpy array with one entry per vertex.
    The first element of the yielded pair is the left hemisphere map and the second is the right
    hemisphere map. The values are obtained by resampling the Benson et al. 2014 anatomically
    defined template of retinotopy to the given subject.
    Note that the subject must have been registered to the fsaverage_sym subject prior to calling
    this function; this requires using the surfreg command (after the xhemireg command for the RH).
    Additionally, you must have the fsaverage_sym template files in your fsaverage_syn/surf
    directory; these files are sym.template_angle.mgz, sym.template_eccen.mgz, and 
    sym.template_areas.mgz.
    '''
    global __retinotopy_templates
    template = template.lower()
    if template not in _retinotopy_templates:
        # Find a sym template that has the right data:
        sym_path = next((os.path.join(path0, 'fsaverage_sym')
                         for path0 in (subject_paths() +
                                       [os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                     'lib', 'data')])
                         for path in [os.path.join(path0, 'fsaverage_sym', 'surf')]
                         if os.path.isfile(os.path.join(path, 'sym.%s_angle.mgz' % template)) 
                         if os.path.isfile(os.path.join(path, 'sym.%s_eccen.mgz' % template))
                         if os.path.isfile(os.path.join(path, 'sym.%s_varea.mgz' % template))),
                        None)
        if sym_path is None:
            raise ValueError('No fsaverage_sym subj found with surf/sym.%s_*.mgz files!' % template)
        sym = freesurfer_subject('fsaverage_sym').LH
        tmpl_path = os.path.join(sym_path, 'surf', 'sym.%s_' % template)
        # We need to load in the template data
        _retinotopy_templates[template] = {
            'angle': fsmgh.load(tmpl_path + 'angle.mgz').get_data().flatten(),
            'eccen': fsmgh.load(tmpl_path + 'eccen.mgz').get_data().flatten(),
            'varea': fsmgh.load(tmpl_path + 'varea.mgz').get_data().flatten()}
    # Okay, we just need to interpolate over to this subject
    tmpl = _retinotopy_templates[template]
    sym = freesurfer_subject('fsaverage_sym').LH
    return (
        {'polar_angle':  sub.LH.interpolate(sym,  tmpl['angle'], apply=False),
         'eccentricity': sub.LH.interpolate(sym,  tmpl['eccen'], apply=False),
         'visual_area':  sub.LH.interpolate(sym,  tmpl['varea'], apply=False, method='nearest')},
        {'polar_angle':  sub.RHX.interpolate(sym, tmpl['angle'], apply=False),
         'eccentricity': sub.RHX.interpolate(sym, tmpl['eccen'], apply=False),
         'visual_area':  sub.RHX.interpolate(sym, tmpl['varea'], apply=False, method='nearest')})
        

def clean_retinotopy(obj, retinotopy='empirical', output_style='visual', weight=Ellipsis,
                     equality_sigma=0.15, equality_scale=10.0,
                     smoothness_scale=0.04, orthogonality_scale=0,
                     yield_report=False):
    '''
    clean_retinotopy(mesh) attempts to cleanup the retinotopic maps on the given cortical mesh by
      minimizing an objective function that tracks the smoothness of the fields, the orthogonality
      of polar angle to eccentricity, and the deviation of the values from the measured values; the
      yielded result is the smoothed retinotopy, as would be returned by
      as_retinotopy(..., 'visual').
    clean_retinotopy(hemi) performs the identical operation on the hemisphere's white surface.
    
    The following options are accepted:
      * retinotopy ('empirical') specifies the retinotopy data; this should be understood by the
        mesh_retinotopy function or the as_retinotopy function.
      * output_style ('visual') specifies the style of the output data that should be returned;
        this should be a string understood by as_retinotopy.
      * yield_report (False) may be set to True, in which case a tuple (retino, report) is returned,
        where the report is the return value of the scipy.optimization.minimize function.
    '''
    from scipy.optimize import minimize
    from scipy.sparse import (lil_matrix, csr_matrix)
    if isinstance(obj, Hemisphere): obj = obj.white_surface
    # get the retinotopy first:
    if isinstance(retinotopy, basestring):
        retinotopy = mesh_retinotopy(obj, retinotopy.lower())
    (theta0, eccen0) = as_retinotopy(retinotopy, 'visual')
    # we want to scale eccen by a log-transform; this is the inverse of the cortical magnification
    # function in Horton & Hoyt 1991
    def _hh_ecc2cd(ecc):
        return 17.3 * (0.287682 + np.log(0.75 + ecc))
    def _hh_cd2ecc(d):
        return 0.75*(np.exp(0.0578035*d) - 1)
    rho_max = _hh_ecc2cd(90.0)
    rho0    = _hh_ecc2cd(eccen0) / rho_max # range from 0-1
    # We scale theta down to +/- pi
    theta0 *= np.pi/180.0

    # our x0 value is just a joining of theta with rho:
    x0 = np.concatenate((theta0, rho0))
    n = len(theta0)
    es = obj.indexed_edges
    fcs = obj.indexed_faces
    m = es.shape[1]
    p = fcs.shape[1]
    ninv = 1.0 / n
    minv = 1.0 / m

    # figure out the weights...
    if weight is Ellipsis:
        varexp_aliases = ['variance_explained', 'varexp', 'vexpl', 'weight']
        wgt = next((retinotopy[x] for x in varexp_aliases if x in retinotopy), ninv)
    elif weight is None:
        wgt = ninv
    elif isinstance(weight, basestring):
        wgt = obj.prop(weight)
    else:
        wgt = weight
    wgt = np.asarray(wgt / np.sum(wgt))
    ww  = wgt if wgt.shape is () else np.concatenate((wgt, wgt))

    # Next, setup the potential functions

    # PE1: equality; we use a Gaussian function so that patches of noise do not drive the potential
    # too strongly...
    (hpi, tau) = (0.5*np.pi, 2.0*np.pi)
    sig = equality_sigma if hasattr(equality_sigma, '__iter__') else (equality_sigma,equality_sigma)
    sig_tht = sig[0] * np.pi
    sig_rho = sig[1]
    f1_coef = ww
    d1_coef = ww / np.concatenate([np.full(n, s**2) for s in [sig_tht,sig_rho]])
    def _f_equal(x):
        theta = x[0:n]
        rho   = x[n:]
        # differences...
        dtht  = theta - theta0
        drho  = rho - rho0
        dtht2 = (dtht / sig_tht)**2
        drho2 = (drho / sig_rho)**2
        # okay, the equation itself
        fexp  = np.exp(-0.5 * np.concatenate((dtht2, drho2)))
        f     = np.sum(f1_coef * (1.0 - fexp))
        # and the derivative
        df    = d1_coef * fexp * np.concatenate((dtht, drho))
        # That's it:
        return (f, df)


    # PE2: smoothness; we want the change along any edge to be minimal
    # setup a fast edge-to-vertex summation:
    e2v = lil_matrix((n, m))
    for (k,(u,v)) in enumerate(es.T):
        e2v[u,k] = 1.0
        e2v[v,k] = -1.0
    e2v = csr_matrix(e2v)
    els = obj.edge_lengths
    elsuu = np.isclose(els, 0)
    els2inv = (1 + elsuu) / (els**2 + elsuu)
    def _f_smooth(x):
        theta = x[0:n]
        rho   = x[n:]
        # edge-values:
        etht1 = theta[es[0]]
        etht2 = theta[es[1]]
        erho1 = rho[es[0]]
        erho2 = rho[es[1]]
        # differences along edges:
        dtht  = (etht1 - etht2)
        drho  = (erho1 - erho2)
        dtht_r2 = dtht * els2inv
        drho_r2 = drho * els2inv
        # the potential is just the sum of squares of these
        f = 0.5 * minv * (np.sum(dtht_r2*dtht) + np.sum(drho_r2*drho))
        # for the derivative, we have to convert from edges back to vertices
        df = minv * np.concatenate((e2v.dot(dtht_r2), e2v.dot(drho_r2)))
        return (f, df)

    # PE3: orthogonality; we want eccentricity and polar angle to be orthogonal
    # at every triangle
    # We need to calculate some constants beforehand...
    fx = np.asarray([obj.coordinates[:,ii] for ii in fcs])
    ## side lengths:
    (s0_2,s1_2,s2_2) = [np.sum(dx**2, axis=0) for dx in (fx[2]-fx[1], fx[0]-fx[2], fx[1]-fx[0])]
    ## height of the triangle (from a point in side 12 to point 0
    (s0,s1,s2) = [np.sqrt(s) for s in (s0_2, s1_2, s2_2)]
    s0uu = np.isclose(s0_2, 0)
    inv_s0 = (1 - s0uu) / (s0 + s0uu)
    part12 = (s0_2 - s1_2 + s2_2) * (0.5 * inv_s0)
    height = np.sqrt(2*s0_2*(s1_2 + s2_2) - s0_2**2 - (s1_2 - s2_2)**2) * (0.5 * inv_s0)
    heightuu = np.isclose(height, 0)
    inv_h = (1 - heightuu) / (height + heightuu)
    ## convenience function for calculating gradients wrt the faces and such
    def _face_retino_grads(fs_tht, fs_rho):
        # We can use the height and fraction of side 1-2 to find gradient vectors relative to the
        # ad-hoc axes formed by traingle side 1-2 (x-axis) and the perpendicular to it (y-axis):
        (gtht, grho) = [np.asarray([dx, (z[0] - (z[1] + dx*part12))*inv_h])
                        for z  in [fs_tht, fs_rho]
                        for dx in [(z[2] - z[1])*inv_s0]]
        # find the norms of the gradients
        (ntht_2, nrho_2) = [np.sum(gr**2, axis=0) for gr  in (gtht, grho)]
        (ntht,   nrho)   = [np.sqrt(nz2)          for nz2 in (ntht_2, nrho_2)]
        # dot product vecotrs, u, can now be calculated:
        (utht, urho) = [gz * ((1 - uu)/(nz + uu))
                        for (gz,nz) in [(gtht,ntht), (grho,nrho)]
                        for uu in [np.isclose(nz, 0)]]
        return (gtht,utht,ntht,ntht_2, grho,urho,nrho,nrho_2)
    ## We need to know the initial gradient lengths
    (fs_tht0, fs_rho0) = [[z0[ii] for ii in fcs] for z0 in [theta0, rho0]]
    (_,_,ntht0,ntht0_2, _,_,nrho0,nrho0_2) = _face_retino_grads(fs_tht0, fs_rho0)
    fidcs = np.where(~np.isclose(ntht0_2 * nrho0_2, 0))[0]
    ## we are only interested in faces whose initial gradients are not near 0; this prevents
    ## discontinuities in the potential. Go ahead and filter these:
    (fcs, fs_tht0, fs_rho0)             = [np.asarray(z)[:,fidcs] for z in (fcs, fs_tht0, fs_rho0)]
    (s0, s1, s2, inv_h, inv_s0, part12, ntht0_2, nrho0_2) = [
        np.asarray(z)[fidcs]
        for z in (s0, s1, s2, inv_h, inv_s0, part12, ntht0_2, nrho0_2)]
    ## we now know the number of triangles and can calculate our normalization constants:
    p = len(fidcs)
    pinv = 1.0 / p
    invtot = ninv + minv + pinv
    (ninv, minv, pinv) = (ninv/invtot, minv/invtot, pinv/invtot)
    ## we can also pre-calculate a part of the jacobian:
    #jac_gr_z = [[height, 0], [height*(part12/s0 - 1), -1.0/s0], [-height*part12/s0, 1.0/s0]]
    jac_gr_z_T = [[0,       inv_h],
                  [-inv_s0, (part12 - s0)*inv_h*inv_s0],
                  [inv_s0,  -part12*inv_s0*inv_h]]
    ## We also need some data about how to get from faces to vertices
    f2vs = []
    for frow in fcs:
        lm = lil_matrix((n,p))
        for (f,u) in enumerate(frow):
            lm[u,f] = 1
        f2vs.append(csr_matrix(lm))
    def _f_ortho(x):
        # This calculation is a bit opaque; the actual value computed is the square of the dot
        # product of the normalized normal vector of the triangle for each field...
        # This can be found by decomposing the derivative of the dot product using the
        # multiplication rule:
        theta = x[0:n]
        rho   = x[n:]
        # separate out by triangle:
        fs_tht = np.asarray([theta[ii] for ii in fcs])
        fs_rho = np.asarray([rho[ii]   for ii in fcs])
        # get the face data:
        (gtht,utht,ntht,ntht_2, grho,urho,nrho,nrho_2) = _face_retino_grads(fs_tht, fs_rho)
        # the angle cosine is just this:
        cos_phi = np.sum(utht * urho, axis=0)
        # now, we consider the jacobian; first, we already calculated the jacobian of gtht and grho
        # above (jac_gr_z); we also need the jacobian of the normalized grads in terms of the grads:
        (ntht_3_inv, nrho_3_inv) = [(1 - uu) / (v + uu)
                                    for v  in [ntht*ntht_2, nrho*nrho_2]
                                    for uu in [np.isclose(v, 0)]]
        (jac_norm_tht, jac_norm_rho) = [
            np.asarray([[z[1]**2 * inz3,           -z01],
                        [          -z01, z[0]**2 * inz3]])
            for (z,inz3)  in [(gtht,ntht_3_inv), (grho,nrho_3_inv)]
            for z01           in [z[0]*z[1]*inz3]]
        # Okay, we can stick together the jacobians:
        (jac_tht, jac_rho) = [
            np.asarray([j0*u0 + j1*u1 for (j0,j1) in jac_gr_z_T])
            for (jac_gz, gw) in [(jac_norm_tht, urho), (jac_norm_rho, utht)]
            for (u0,u1)      in [(jac_gz[0,0]*gw[0] + jac_gz[0,1]*gw[1],
                                  jac_gz[1,0]*gw[0] + jac_gz[1,1]*gw[1])]]
        # last, we just need to move these over to vertices:
        (jac_tht, jac_rho) = [np.sum([m.dot(cos_phi * jz) for (m,jz) in zip(f2vs,jac_z)], axis=0)
                              for jac_z in [jac_tht, jac_rho]]
        # That's it, there is just dressing to put on the first part:
        f_ang  = 0.5 * pinv * np.sum(cos_phi**2)
        df_ang = pinv * np.concatenate((jac_tht, jac_rho))
        # The second part of the gradient is the part that prevents flat 0-gradients:
        # 1/2(log(1/2 |grad t|/|grad t0|)^2 + log(1/2 |grad r|/|grad r0|)^2)
        if np.isclose(ntht_2, 0).any() or np.isclose(nrho_2, 0).any():
            return (np.inf, 0)
        log_tht = np.log(ntht_2 / ntht0_2)
        log_rho = np.log(nrho_2 / nrho0_2)
        # potential is now easy...
        f_flt = 0.25 * pinv * (np.sum(log_tht**2) + np.sum(log_rho**2))
        # we need to calculate the gradient:
        (cc_tht, cc_rho) = [lgz / rz for (lgz,rz) in [(log_tht,ntht_2), (log_rho,nrho_2)]]
        (lg_tht, lg_rho) = [np.asarray([cc_z * (j0*uz[0] + j1*uz[1]) for (j0,j1) in jac_gr_z_T])
                            for (uz,cc_z) in [(utht,cc_tht), (urho,cc_rho)]]
        df_flt = pinv * np.concatenate([np.sum([m.dot(gzrow) for (gzrow,m) in zip(gz,f2vs)], axis=0)
                                        for gz in (lg_tht, lg_rho)])
        return (f_ang + f_flt, df_ang + df_flt)

    # Okay, mix these together!
    def _f(x):
        (fe, dfe) = _f_equal(x)  if equality_scale != 0      else (0,0)
        (fs, dfs) = _f_smooth(x) if smoothness_scale != 0    else (0,0)
        (fo, dfo) = _f_ortho(x)  if orthogonality_scale != 0 else (0,0)
        #print np.asarray([[equality_scale*fe, smoothness_scale*fs, orthogonality_scale*fo],
        #                  [equality_scale*np.sqrt(np.sum(dfe**2)),
        #                   smoothness_scale*np.sqrt(np.sum(dfs**2)),
        #                   orthogonality_scale*np.sqrt(np.sum(dfo**2))]])
        scales = [equality_scale, smoothness_scale, orthogonality_scale]
        if not np.isfinite([fe,fs,fo]).all():
            return (np.inf, np.full(len(x), np.inf))
        f  = equality_scale*fe + smoothness_scale*fs + orthogonality_scale*fo
        df = np.sum([d*s for (d,s) in zip([dfe,dfs,dfo],
                                          [equality_scale,smoothness_scale,orthogonality_scale])],
                    axis=0)
        return (f, df)

    # That's our potential; now we can do the minimization
    res = minimize(_f, x0, jac=True, method='L-BFGS-B')
    #return (x0, _f, (_f_equal, _f_smooth, _f_ortho))
    theta = res.x[0:n]
    rho = res.x[n:]
    # rescale rho
    eccen = _hh_cd2ecc(rho * rho_max)
    angle = theta*180.0/np.pi
    if yield_report is True:
        return (as_retinotopy({'polar_angle':angle, 'eccentricity':eccen}, output_style), res)
    else:
        return as_retinotopy({'polar_angle':angle, 'eccentricity':eccen}, output_style)
            
