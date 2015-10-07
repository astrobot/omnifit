# Licensed under a 3-clause BSD style license - see LICENSE.rst
from astropy.tests.helper import pytest
import numpy as np
import os
from ... import spectrum
from ... import utils
from ...tests import helpers
from astropy import units as u

class TestKKrelation_supportfuncs:
  def test_transrefcoefficients(self):
    """
    Make sure that the calculations for the transmission and
    reflection coefficients work as expected
    """

    testspec = helpers.generate_cdespectrum()
    testn = testspec.n
    testk = testspec.k
    testm1 = testspec.n + testspec.k * 1j
    testm0 = 1.0+0.0j
    testm2 = 1.3+1.3j

    t01,t02,t12,r01,r02,r12 = utils.complex_transmission_reflection(testm0,testm1,testm2)

    #these are the functions which are supposed to work
    complex_transmission = lambda m1,m2: (2.*m1.real)/(m1+m2)
    complex_reflection = lambda m1,m2: (m1-m2)/(m1+m2)

    assert np.all(t01 == complex_transmission(testm0,testm1))
    assert np.all(t02 == complex_transmission(testm0,testm2))
    assert np.all(t12 == complex_transmission(testm1,testm2))

    assert np.all(r01 == complex_reflection(testm0,testm1))
    assert np.all(r02 == complex_reflection(testm0,testm2))
    assert np.all(r12 == complex_reflection(testm1,testm2))

class TestKKIter:
  def test_kkiterbasic(self):
    """
    Test basic functionality of KK iteration.
    Not going for a full iteration; just making sure it doesn't crash
    and that it returns an array of what looks like the right shape
    """
    testspec = helpers.generate_absspectrum()
    assert testspec.x.unit == u.kayser
    assert testspec.y.unit == utils.unit_od
    testspec.subspectrum(2200.,3900.)
    freq = testspec.x
    transmittance = testspec.y.to(utils.unit_transmittance,equivalencies=utils.equivalencies_absorption)
    m_substrate = 1.74+0.0j #CsI window, like in the original Hudgins paper
    d_substrate = 0.2*u.micron
    n0 = 1.3
    m_ice = utils.kramers_kronig(freq,transmittance,m_substrate,d_substrate,n0,maxiter=2)
    assert m_ice.shape == freq.shape

  def test_kkitertocde(self):
    """
    Check the sanity of CDE spectra generated from KK iteration results
    """
    testspec = helpers.generate_absspectrum()
    assert testspec.x.unit == u.kayser
    assert testspec.y.unit == utils.unit_od
    testspec.subspectrum(2000.,4500.)
    freq = testspec.x
    transmittance = testspec.y.to(utils.unit_transmittance,equivalencies=utils.equivalencies_absorption)
    m_substrate = 1.74+0.0j #CsI window, like in the original Hudgins paper
    d_substrate = 0.5*u.micron #not probably true, but good enough for testing
    n0 = 1.3
    m_ice = utils.kramers_kronig(freq,transmittance,m_substrate,d_substrate,n0)
    assert m_ice.shape == freq.shape