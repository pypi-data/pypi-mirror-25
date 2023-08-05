
import numpy as np
from os.path import dirname, exists, join, basename
from os import listdir
import glob
import gzip

from pyknotid.spacecurves import Knot

knots_folder = join(dirname(__file__), 'ideal_knots')

def _sort_func(filen):
    filen = filen.split('/')[-1]
    num_components = len(filen.split('#'))

    components = filen.split('#')[0].strip('_')

    values = components.split('_')

    crossings = int(values[0])
    number = int(values[1])

    return crossings + 1e-6 * number + 10000 * num_components

def available_ideal_knots():
    '''Returns a list of the knots whose conformations are available via
    :func:`ideal_knot`.
    '''

    filens = glob.glob(join(knots_folder, '*.txt.gz'))
    filens = [basename(filen)[:-7] for filen in filens]

    filens = sorted(filens, key=_sort_func)
    return filens

def ideal_knot(name):

    '''Returns a :class:`~pyknot2.spacecurves.knot.Knot` whose points form
    an approximation to the ideal (minimal ropelength) conformation of
    the given knot.

    These knots are the freely available tight knot conformations
    obtained by Jason Cantarella's Ridgerunner, see
    `http://www.jasoncantarella.com/wordpress/software/ridgerunner/`_
    for more information and the full data files.

    .. note:: Only prime_knots with up to 10 crossings are available,
              see :func:`available_ideal_knots`.

    Example::

        k = ideal_knot('6_3')

    Parameters
    ----------
    name : str
        The name of the knot in standard notation, e.g. 3_1, 4_1, ....
        Only knots with up to 10 crossings are available.

    '''

    filen = join(knots_folder, '{}.txt.gz'.format(name))
    if not exists(filen):
        raise ValueError(('Could not find filename {}.txt.gz for '
                          'the given knot name. Only knots with up '
                          'to 10 crossings are available.').format(name))

    points = []
    with gzip.open(filen, 'rb') as fileh:
        for line in fileh:
            line = line.decode('utf-8')
            numbers = line.split(' ')
            points.append([float(numbers[0]),
                           float(numbers[1]),
                           float(numbers[2])])

    return Knot(np.array(points))
                               
            
