# PSF Generator

GLAO_PSF is an Ground-Layer Adaptive Optics Structure Function and average Point Spread Function calculator.
Calculating the AO-corrected and uncorrected PSFs will allow comparisons of instrument sensitivity
improvements expected with AO correction under various conditions.

This code was created in support of GLAO design studies for

* Thirty Meter Telescope
* Keck Telescopes

## Getting the code

### Prerequisite: make sure you have hdf5 library installed
You will need the hdf5 library installed on your system. Use your system installer to get
HDF5 1.8.4 or newer, shared library version with development headers (libhdf5-dev or similar). From a mac
this can be done with port or homebrew, and from Ubuntu with apt-get. For example (mac):

```
port install hdf5
```
see http://docs.h5py.org/en/latest/build.html#source-installation for more information about hdf5 install.

### Installing the GLAO_PSF code
GLAO_PSF is available from the Python Package Index (PyPI):

```
pip install glao_psf
```

## Running the code example

The code starts by reading parameters from a configuration file that define the atmospheric seeing conditions,
AO configuration (# of guidestars etc.), and image parameters (such as wavelength). Then it calculates both
the AO-corrected PSF and the open-atmosphere (not AO correced) PSF. Finally, it writes these PSFs to
FITS files.

An example config file is provided with the package (example.cfg). The code will use this config file
by default if no other arguments are given.

From within python:

```
>>> from glao_psf import psf_fe
>>> db = psf_fe.run('example.cfg')
```

Later on, you will want to write your own config file. Look for 'keck.cfg' and 'tmt.cfg' in the code distribution
(or download from this bitbucket repository). Edit a copy of one of these and put it in the directory from which you are running
python.

## Looking at results

The results are saved in two FITS files (nominally psf.fits, and psf0.fits, but these file names
can be overridden in the `[output]` section of the config file).

The return value `db` is a Pandas dataFrame containing a summary of results. This
is mostly useful for multi-runs (see the section on multi-runs below)

To get a quick view of the guidestar constellation:

```
>>> psf_fe.a.constellation.graph()
```

To view cross sections of the PSFs:

```
>>> psf_fe.a.PSF.graph()
>>> psf_fe.a.PSF_seeing.graph(oplot=True)
```

Note: PSFs are normalized so as to integrate to 1, that is $/int PSF(\theta) d^2 \theta = 1$.

Equivalent Noise Area (ENA) is calculated for both PSFs. ENA has units of square arcseconds.
There is also a notion of ENA radius, defined as the
radius of the circle that has area equal to ENA, having units of arcseconds. ENA radius of a
seeing PSF is very close to the full-width-half-max. ENA and ENA_R are keywords in the FITS headers
of the PSF files. They can also be viewed using python:

```
>>> psf_fe.a.PSF.ena
>>> psf_fe.a.PSF.ena_r
>>> psf_fe.a.PSF_seeing.ena
>>> psf_fe.a.PSF_seeing.ena_r
```

Finally, to view the entire PSF as an image:

```
>>> psf_fe.a.PSF.show()
>>> psf_fe.a.PSF_seeing.show()
```
To get all the above graphs and ENA summary with a single command:

```
>>> psf_fe.summary()
```

## Setting up a configuration file

Edit a new config file (using example.cfg as a guide). There are 5 sections
in the config file:

* constellation
* atmosphere
* AO
* image
* output

The format of the config file is

```
[section_name]
parameter= value
parameter= value
...
```

Lines that begin with # are comments.

Do not put quotes around any of the values. Some
parameters are numerical values followed by optional
units; some parameters are just strings. One parameter
image/field_point is an XY pair surrounded by parentheses.

### Multi-run specification

Starting with version 2, parameters can have multiple values,
separated by commas, as in

```
parameter= value1, value2, value3
```

The code will collect all the multi-value specifications and from them
define a set of runs, one run for each combinations of the multiple
parameters. For example if one parameter has 3 values and another 4 values, then
3x4 or 12 runs will happen, each generating a PSF with a different
combination of the parameters.

The multi-run creates a database (Python Pandas dataFrame), which is returned
by the call to `psf_fe.run(configFile)`. This dataFrame has the parameter settings
and certain of the results such as ENA (equivalent noise area of the PSF),
EE_50 (50% encircled energy radius), EE_80, etc. Within Python, the dataFrame
can be queried or saved to disk.

The GLAO PSFs and the corresponding seeing-limited PSFs under the same parameters
will be stored as fits files in a data directory
(the directory's name is specified by the `run_name` parameter). Each fits file has header
information that defines the conditions of the run. All the fits file headers
are summarized in a spreadsheet file `log.csv' in that same directory.

### Entries in the configuration file

### [constellation] Define a guide star constellation

#### geom

Constellations are "circle" or "wheel." A circle has all the guide stars at the radius, equally spaced in angle.
A wheel is a circle with one additional guide star at the center.

#### radius

The radius is in arcsminutes from the center of the field.

#### ngs

Set ngs to the number of guide stars.

#### rot

Ordinarily, the constellation geometry has the
first guidestar at 0 degrees position angle and the remaining stars
positioned around the circle equally spaced in angle.
Use rot to rotate the entire constellation on the
sky by this amount in degrees.

### [atmosphere] Define the seeing conditions

#### profile

Chose from a number of built-in Cn2 profiles. These
include statistical average profiles measured for the
TMT site survey and the Gemini GLAO survey.
For TMT use

```
profile= Maunakea 13N median
```

Manueakea 13N 25% and Maunakea 13N 75% profiles are
also available.

For Keck use
```
profile= MK2009 50%
```
25% and 75% are also available.

#### outer_scale

The outer scale of turbulence (known as L0). This is the distance
at which the structure function flattens out, rather than continuing
up on a r^5/3 power law. Lore says that at Maunakea
L0 ~ 30 meters, but there is little direct measurement evidence.
The often observed open seeing at Maunakea, about
1/3 arcsec when r0 = 20 cm, does seem consistent with
this value of L0 (seeing would be about 1/2 arcsec at infinite outer scale).

Also, L0 has a mixed meaning when
taking into about Cn2 altitude profiles.
Recall that the argument for
an outer scale is based on surface topography.
So does L0 = 30 meters mean
only at the ground layer, while at
upper altitude layers well above the ground it is much larger?
For simplicity, our code models the outer scale the same at all layers,
although a future version of the code may allow for specifying a separate
L0 for each layer.

Specify the outer scale as a positive number, the
distance in meters. For an infinite outer scale
(Kolmogorov r^(5/3) turbulence for all r)
use Infinity as the value:

```
outer_scale= Infinity
```

#### r0

Fried seeing parameter. Specifying this parameter
*scales the Cn2 profile*, so don't use it if you
want to use the standard measured profile, which
has its r0 implicit.

### [AO] Adaptive optics system information

#### dm_conjugate

The deformable mirror (DM) conjugate altitude. This is
the (optical conjugate) altitude at which the wavefront
is corrected. Both the Keck telescope and the
present design for TMT are Richey-Cretien,
where the secondary mirror conjugate is at
a negative altitude. If the GLAO correction is to be
done with an adaptive secondary, use these values:

* TMT: dm_conjugate= -280 meters
* Keck: dm_conjugate= -126 meters

#### actuator_spacing

A deformable mirror only has a finite number of
actuators on the back in order to affect wavefront
correction. We model this as a spatial-frequency
cutoff to the correction. Actuator spacing is defined
across the pupil (not across the secondary mirror),
i.e. it is a sampling on the incoming beam to the
telescope. Setting the actuator_spacing to
zero is allowed, which means the model assumes
correction across all spatial frequencies.

### [image] Imaging properties

The PSF is the image of a point source at
a given wavelength. We have not modeled a sky
background, however the analysis by King shows
that Equivalent Noise Area (ENA) can be calculated
from just the PSF and will profide a factor that
can be used to calculate the signal-to-noise given
the sky background.

#### wavelength

The wavelength at which the PSFs are calculated,
in microns.

#### field_points

This is a list (comma delimited) of positions in
the field at which the AO corrected PSF is calculated.
Each point is defined by an XY pair of numbers separated by
a comma and surrounded by parentheses, as in (0.,0.),(1.,0.),...
The values are distances from the center (0.,0.)
of the guide star constellation, in arcminutes. Typically the field_points
are located within the constellation radius, but don't
have to be. The calculation will be inaccurate
beyond two constellation radii, but generally there
is very little GLAO correction there, and
the corrected PSF is essentially the same as the uncorrected PSF.

### [output] Set the file names for storing the calculated PSFs

**NOTE** None of the `[output]` parameters are allowed to be multi-parameters.

#### run_name

The name for the run. The results will be stored in a directory
with this name.

#### filename

The prefix name for the fits files with AO-corrected PSFs. For example
filename "psf" will generate files psf_0000.fits, psf_0001.fits etc.
one for each case defined by the configuration file.

#### seeing_psf_filename

The prefix name for the files with the open-seeing PSF.

## Code source, modifications and suggestions

Code source is maintained in a Bitbucket repository:
https://bitbucket.org/donald_gavel/glao_psf/src

Feel free to modify your local copy to suit your needs. The code
psf_fe.py (psf "front end") drives psf.py. I would
appreciate a note from you telling me about the changes you made so they can be possibly
included in future release. Also, I'm happy to entertain suggestions for new features.

Code documentation is coming soon.

## References

Gavel, Donald. "Point Spread Function for Ground Layer Adaptive Optics." [arXiv preprint arXiv:1706.00041  (2017)](https://arxiv.org/abs/1706.00041).

Chun, M., Wilson, R., Avila, R., Butterley, T., Aviles, J. L., Wier, D., & Benigni, S. (2009).
Mauna Kea ground-layer characterization campaign. Monthly Notices of the Royal Astronomical Society,
394(3), 1121–1130. http://doi.org/10.1111/j.1365-2966.2008.14346.x

I. R. King, "Accuracy of Measurement of Star Images on a Pixel Array," Publications of the
Astronomical Society of the Pacific 95(February), pp. 163-168, 1983.

G. Z. Angeli, B.-j. Seo, C. Nissly, and M. Troy, "A convenient telescope performance metric
for imaging through turbulence," Proc. of SPIE 8127, pp. 1-11, 2011.

