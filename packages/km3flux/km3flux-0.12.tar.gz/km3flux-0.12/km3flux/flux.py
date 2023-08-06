"""Assorted Fluxes, in  (m^2 sec sr GeV)^-1"""

import logging

import h5py
import numpy as np
from scipy.integrate import romberg, simps
from scipy.stats import describe        # noqa

from km3flux.data import (HONDAFILE, dm_gc_spectrum, dm_sun_spectrum,
                          DM_GC_FLAVORS, DM_GC_CHANNELS, DM_GC_MASSES,
                          DM_SUN_FLAVORS, DM_SUN_CHANNELS, DM_SUN_MASSES
                         )


class BaseFlux(object):
    """Base class for fluxes.

    Methods
    =======
    __call__(energy, zenith=None)
        Return the flux on energy, optionally on zenith.
    integrate(zenith=None, emin=1, emax=100, **integargs)
        Integrate the flux via romberg integration.
    integrate_samples(energy, zenith=None, emin=1, emax=100)
        Integrate the flux from given samples, via simpson integration.

    Example
    =======
    >>> zen = np.linspace(0, np.pi, 5)
    >>> ene = np.logspace(0, 2, 5)

    >>> from km3flux.flux import MyFlux
    >>> flux = MyFlux(flavor='nu_mu')

    >>> flux(ene)
    array([6.68440000e+01, 1.83370000e+01, 4.96390000e+00,
           1.61780000e+00, 5.05350000e-01,])
    >>> flux(ene, zen)
    array([2.29920000e-01, 2.34160000e-02, 2.99460000e-03,
           3.77690000e-04, 6.87310000e-05])
    """
    def __init__(self, **kwargs):
        pass

    def __call__(self, energy, zenith=None):
        if zenith is None:
            return self._averaged(energy)
        if len(zenith) != len(energy):
            raise ValueError("Zenith and energy need to have the same length.")
        return self._with_zenith(energy, zenith)

    def _averaged(self, energy):
        raise NotImplementedError

    def _with_zenith(self, energy, zenith):
        raise NotImplementedError

    def integrate(self, zenith=None, emin=1, emax=100, **integargs):
        return romberg(self, emin, emax, vec_func=True, **integargs)

    def integrate_samples(self, energy, zenith=None, emin=1, emax=100,
                          **integargs):
        energy = np.atleast_1d(energy)
        mask = (emin <= energy) & (energy <= emax)
        energy = energy[mask]
        if zenith:
            zenith = np.atleast_1d(zenith)
            zenith = zenith[mask]
        flux = self(energy, zenith=zenith)
        return simps(flux, energy, **integargs)


class PowerlawFlux(BaseFlux):
    """E^-gamma flux."""
    def __init__(self, gamma=2, scale=1e-4):
        self.gamma = gamma
        self.scale = scale

    def _averaged(self, energy):
        return self.scale * np.power(energy, -1 * self.gamma)

    def integrate(self, zenith=None, emin=1, emax=100, **integargs):
        """Compute analytic integral instead of numeric one."""
        if np.around(self.gamma, decimals=1) == 1.0:
            return np.log(emax) - np.log(emin)
        num = np.power(emax, 1 - self.gamma) - np.power(emin, 1 - self.gamma)
        den = 1.0 - self.gamma
        return self.scale * (num / den)


class Honda2015(BaseFlux):
    """
    Get Honda 2015 atmospheric neutrino fluxes.
    """
    def __init__(self, flavor='nu_mu'):
        self.table = None
        self.avtable = None
        filename = HONDAFILE
        if flavor not in ('nu_e', 'anu_e', 'nu_mu', 'anu_mu'):
            raise ValueError("Unsupported flux '{}'".format(flavor))
        with h5py.File(filename, 'r') as h5:
            self.energy_bins = h5['energy_binlims'][:]
            self.cos_zen_bins = h5['cos_zen_binlims'][:]
            self.table = h5[flavor][:]
            self.avtable = h5['averaged/' + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

    def _averaged(self, energy):
        fluxtable = self.avtable
        ene_bin = np.digitize(energy, self.energy_bins)
        ene_bin = ene_bin - 1
        return fluxtable[ene_bin]

    def _with_zenith(self, energy, zenith):
        fluxtable = self.table
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]


class HondaSarcevic(BaseFlux):
    """
    Get Honda + Sarcevic atmospheric neutrino fluxes.
    """
    def __init__(self, flavor='nu_mu'):
        self.table = None
        self.avtable = None
        filename = HONDAFILE
        if flavor not in ('nu_e', 'anu_e', 'nu_mu', 'anu_mu'):
            raise ValueError("Unsupported flux '{}'".format(flavor))
        with h5py.File(filename, 'r') as h5:
            self.energy_bins = h5['energy_binlims'][:]
            self.cos_zen_bins = h5['cos_zen_binlims'][:]
            self.table = h5['honda_sarcevic/' + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

    def _averaged(self, energy):
        raise NotImplementedError("Supports only zenith dependent flux!")

    def _with_zenith(self, energy, zenith):
        fluxtable = self.table
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]


class DarkMatterFlux(BaseFlux):
    """
    Get Dark Matter spectra (taken from M. Cirelli).

    >>> from km3flux import DarkMatterFlux
    >>> flux = DarkMatterFlux()

    >>> ene = np.logspace(0, 2, 11)

    >>> flux('anu_mu', ene)
    array([  6.68440000e+01,   1.83370000e+01,   4.96390000e+00,
         1.61780000e+00,   5.05350000e-01,   2.29920000e-01,
         2.34160000e-02,   2.99460000e-03,   3.77690000e-04,
         6.87310000e-05,   1.42550000e-05])

    """
    def __init__(self, source='gc', flavor='nu_mu', channel='w', mass=1000):
        self.flavor = flavor
        self.channel = channel
        self.mass = mass
        if source == 'sun':
            loader = dm_sun_spectrum
        else:
            loader = dm_gc_spectrum

        self.counts, self.lims = loader(flavor=flavor, channel=channel,
                                        mass=mass, full_lims=True)

    def _averaged(self, energy):
        energy = np.atleast_1d(energy)
        print(describe(energy))
        print(describe(self.lims))
        if np.any(energy > self.lims.max()):
            raise ValueError(
                "Some energies exceed parent mass '{}'!".format(self.mass))
        fluxtable = self.counts
        ene_bin = np.digitize(energy, self.lims)
        ene_bin = ene_bin - 1
        return fluxtable[ene_bin]

    def _with_zenith(self, energy, zenith):
        logging.warning('No zenith dependent flux implemented! '
                        'Falling back to averaged flux.'
                       )
        return self._averaged(self, energy)


def dmflux(energy, **kwargs):
    """Get the DM flux for your energies."""
    dmf = DarkMatterFlux(**kwargs)
    return dmf(energy)


def e2flux(energy, **kwargs):
    pf = PowerlawFlux(**kwargs)
    return pf(energy)


def all_dmfluxes(source='gc'):
    """Get all dark matter fluxes from all channels, masses, flavors."""
    fluxes = {}
    if source == 'sun':
        flavors = DM_SUN_FLAVORS
        channels = DM_SUN_CHANNELS
        masses = DM_SUN_MASSES
    else:
        flavors = DM_GC_FLAVORS
        channels = DM_GC_CHANNELS
        masses = DM_GC_MASSES
    for flav in flavors:
        for chan in channels:
            for mass in masses:
                mass = int(mass)
                fluxname = (flav, chan, mass)
                fluxes[fluxname] = DarkMatterFlux(source=source, flavor=flav,
                                                  channel=chan, mass=mass)
    return fluxes


def all_dmfluxes_sampled(energy, **kwargs):
    fluxes = all_dmfluxes(**kwargs)
    sampled_fluxes = {}
    for fluxname, flux in fluxes.items():
        sampled_fluxes[fluxname] = flux(energy)
    return fluxes
