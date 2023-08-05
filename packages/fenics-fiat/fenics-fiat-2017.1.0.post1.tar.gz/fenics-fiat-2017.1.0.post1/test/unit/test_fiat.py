# Copyright (C) 2015-2016 Jan Blechta
#
# This file is part of FIAT.
#
# FIAT is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FIAT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with FIAT. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, print_function, division

import random
import numpy as np
import pytest

from FIAT.reference_element import LINE, ReferenceElement
from FIAT.reference_element import UFCInterval, UFCTriangle, UFCTetrahedron
from FIAT.lagrange import Lagrange
from FIAT.discontinuous_lagrange import DiscontinuousLagrange   # noqa: F401
from FIAT.discontinuous_taylor import DiscontinuousTaylor       # noqa: F401
from FIAT.P0 import P0                                          # noqa: F401
from FIAT.crouzeix_raviart import CrouzeixRaviart               # noqa: F401
from FIAT.raviart_thomas import RaviartThomas                   # noqa: F401
from FIAT.discontinuous_raviart_thomas import DiscontinuousRaviartThomas  # noqa: F401
from FIAT.brezzi_douglas_marini import BrezziDouglasMarini      # noqa: F401
from FIAT.nedelec import Nedelec                                # noqa: F401
from FIAT.nedelec_second_kind import NedelecSecondKind          # noqa: F401
from FIAT.regge import Regge                                    # noqa: F401
from FIAT.hdiv_trace import HDivTrace                           # noqa: F401
from FIAT.hellan_herrmann_johnson import HellanHerrmannJohnson  # noqa: F401
from FIAT.brezzi_douglas_fortin_marini import BrezziDouglasFortinMarini  # noqa: F401
from FIAT.gauss_legendre import GaussLegendre                   # noqa: F401
from FIAT.gauss_lobatto_legendre import GaussLobattoLegendre    # noqa: F401
from FIAT.restricted import RestrictedElement                   # noqa: F401
from FIAT.tensor_product import TensorProductElement            # noqa: F401
from FIAT.hdivcurl import Hdiv, Hcurl                           # noqa: F401
from FIAT.argyris import Argyris, QuinticArgyris                # noqa: F401
from FIAT.hermite import CubicHermite                           # noqa: F401
from FIAT.morley import Morley                                  # noqa: F401
from FIAT.bubble import Bubble
from FIAT.enriched import EnrichedElement                       # noqa: F401
from FIAT.nodal_enriched import NodalEnrichedElement


I = UFCInterval()
T = UFCTriangle()
S = UFCTetrahedron()


def test_basis_derivatives_scaling():
    "Regression test for issue #9"
    class Interval(ReferenceElement):

        def __init__(self, a, b):
            verts = ((a,), (b,))
            edges = {0: (0, 1)}
            topology = {0: {0: (0,), 1: (1,)},
                        1: edges}
            super(Interval, self).__init__(LINE, verts, topology)

    random.seed(42)
    for i in range(26):
        a = 1000.0*(random.random() - 0.5)
        b = 1000.0*(random.random() - 0.5)
        a, b = min(a, b), max(a, b)

        interval = Interval(a, b)
        element = Lagrange(interval, 1)

        points = [(a,), (0.5*(a+b),), (b,)]
        tab = element.get_nodal_basis().tabulate(points, 2)

        # first basis function
        assert np.isclose(tab[(0,)][0][0], 1.0)
        assert np.isclose(tab[(0,)][0][1], 0.5)
        assert np.isclose(tab[(0,)][0][2], 0.0)
        # second basis function
        assert np.isclose(tab[(0,)][1][0], 0.0)
        assert np.isclose(tab[(0,)][1][1], 0.5)
        assert np.isclose(tab[(0,)][1][2], 1.0)

        # first and second derivatives
        D = 1.0 / (b - a)
        for p in range(len(points)):
            assert np.isclose(tab[(1,)][0][p], -D)
            assert np.isclose(tab[(1,)][1][p], +D)
            assert np.isclose(tab[(2,)][0][p], 0.0)
            assert np.isclose(tab[(2,)][1][p], 0.0)


xfail_impl = pytest.mark.xfail(strict=True, raises=NotImplementedError)
xfail_key = pytest.mark.xfail(strict=True, raises=KeyError)
elements = [
    "Lagrange(I, 1)",
    "Lagrange(I, 2)",
    "Lagrange(I, 3)",
    "Lagrange(T, 1)",
    "Lagrange(T, 2)",
    "Lagrange(T, 3)",
    "Lagrange(S, 1)",
    "Lagrange(S, 2)",
    "Lagrange(S, 3)",
    "P0(I)",
    "P0(T)",
    "P0(S)",
    "DiscontinuousLagrange(I, 0)",
    "DiscontinuousLagrange(I, 1)",
    "DiscontinuousLagrange(I, 2)",
    "DiscontinuousLagrange(T, 0)",
    "DiscontinuousLagrange(T, 1)",
    "DiscontinuousLagrange(T, 2)",
    "DiscontinuousLagrange(S, 0)",
    "DiscontinuousLagrange(S, 1)",
    "DiscontinuousLagrange(S, 2)",
    "DiscontinuousTaylor(I, 0)",
    "DiscontinuousTaylor(I, 1)",
    "DiscontinuousTaylor(I, 2)",
    "DiscontinuousTaylor(T, 0)",
    "DiscontinuousTaylor(T, 1)",
    "DiscontinuousTaylor(T, 2)",
    "DiscontinuousTaylor(S, 0)",
    "DiscontinuousTaylor(S, 1)",
    "DiscontinuousTaylor(S, 2)",
    "CrouzeixRaviart(I, 1)",
    "CrouzeixRaviart(T, 1)",
    "CrouzeixRaviart(S, 1)",
    "RaviartThomas(T, 1)",
    "RaviartThomas(T, 2)",
    "RaviartThomas(T, 3)",
    "RaviartThomas(S, 1)",
    "RaviartThomas(S, 2)",
    "RaviartThomas(S, 3)",
    "DiscontinuousRaviartThomas(T, 1)",
    "DiscontinuousRaviartThomas(T, 2)",
    "DiscontinuousRaviartThomas(T, 3)",
    "DiscontinuousRaviartThomas(S, 1)",
    "DiscontinuousRaviartThomas(S, 2)",
    "DiscontinuousRaviartThomas(S, 3)",
    "BrezziDouglasMarini(T, 1)",
    "BrezziDouglasMarini(T, 2)",
    "BrezziDouglasMarini(T, 3)",
    "BrezziDouglasMarini(S, 1)",
    "BrezziDouglasMarini(S, 2)",
    "BrezziDouglasMarini(S, 3)",
    "Nedelec(T, 1)",
    "Nedelec(T, 2)",
    "Nedelec(T, 3)",
    "Nedelec(S, 1)",
    "Nedelec(S, 2)",
    "Nedelec(S, 3)",
    "NedelecSecondKind(T, 1)",
    "NedelecSecondKind(T, 2)",
    "NedelecSecondKind(T, 3)",
    "NedelecSecondKind(S, 1)",
    "NedelecSecondKind(S, 2)",
    "NedelecSecondKind(S, 3)",
    "Regge(T, 0)",
    "Regge(T, 1)",
    "Regge(T, 2)",
    "Regge(S, 0)",
    "Regge(S, 1)",
    "Regge(S, 2)",
    "HellanHerrmannJohnson(T, 0)",
    "HellanHerrmannJohnson(T, 1)",
    "HellanHerrmannJohnson(T, 2)",
    "BrezziDouglasFortinMarini(T, 2)",
    "GaussLegendre(I, 0)",
    "GaussLegendre(I, 1)",
    "GaussLegendre(I, 2)",
    "GaussLobattoLegendre(I, 1)",
    "GaussLobattoLegendre(I, 2)",
    "GaussLobattoLegendre(I, 3)",
    "Bubble(I, 2)",
    "Bubble(T, 3)",
    "Bubble(S, 4)",
    "RestrictedElement(Lagrange(I, 2), restriction_domain='facet')",
    "RestrictedElement(Lagrange(T, 2), restriction_domain='vertex')",
    "RestrictedElement(Lagrange(T, 3), restriction_domain='facet')",
    "NodalEnrichedElement(Lagrange(I, 1), Bubble(I, 2))",
    "NodalEnrichedElement(Lagrange(T, 1), Bubble(T, 3))",
    "NodalEnrichedElement(Lagrange(S, 1), Bubble(S, 4))",
    "NodalEnrichedElement("
    "    RaviartThomas(T, 1),"
    "    RestrictedElement(RaviartThomas(T, 2), restriction_domain='interior')"
    ")",
    "NodalEnrichedElement("
    "    Regge(S, 1),"
    "    RestrictedElement(Regge(S, 2), restriction_domain='interior')"
    ")",

    # Following element do not bother implementing get_nodal_basis
    # so the test would need to be rewritten using tabulate
    xfail_impl("TensorProductElement(DiscontinuousLagrange(I, 1), Lagrange(I, 2))"),
    xfail_impl("Hdiv(TensorProductElement(DiscontinuousLagrange(I, 1), Lagrange(I, 2)))"),
    xfail_impl("Hcurl(TensorProductElement(DiscontinuousLagrange(I, 1), Lagrange(I, 2)))"),
    xfail_impl("HDivTrace(T, 1)"),
    xfail_impl("EnrichedElement("
               "Hdiv(TensorProductElement(Lagrange(I, 1), DiscontinuousLagrange(I, 0))), "
               "Hdiv(TensorProductElement(DiscontinuousLagrange(I, 0), Lagrange(I, 1)))"
               ")"),
    xfail_impl("EnrichedElement("
               "Hcurl(TensorProductElement(Lagrange(I, 1), DiscontinuousLagrange(I, 0))), "
               "Hcurl(TensorProductElement(DiscontinuousLagrange(I, 0), Lagrange(I, 1)))"
               ")"),

    # These elements have broken constructor
    xfail_key("Argyris(T, 1)",),
    xfail_key("QuinticArgyris(T)",),
    xfail_key("CubicHermite(I)",),
    xfail_key("CubicHermite(T)",),
    xfail_key("CubicHermite(S)",),
    xfail_key("Morley(T)",),
]


@pytest.mark.parametrize('element', elements)
def test_nodality(element):
    """Check that generated elements are nodal, i.e. nodes evaluated
    on basis functions give Kronecker delta
    """
    # Instantiate element lazily
    element = eval(element)

    # Fetch primal and dual basis
    poly_set = element.get_nodal_basis()
    dual_set = element.get_dual_set()
    assert poly_set.get_reference_element() == dual_set.get_reference_element()

    # Get coeffs of primal and dual bases w.r.t. expansion set
    coeffs_poly = poly_set.get_coeffs()
    coeffs_dual = dual_set.to_riesz(poly_set)
    assert coeffs_poly.shape == coeffs_dual.shape

    # Check nodality
    for i in range(coeffs_dual.shape[0]):
        for j in range(coeffs_poly.shape[0]):
            assert np.isclose(
                coeffs_dual[i].flatten().dot(coeffs_poly[j].flatten()),
                1.0 if i == j else 0.0
            )


@pytest.mark.parametrize('elements', [
    (Lagrange(I, 2), Bubble(I, 2)),
    (Lagrange(T, 3), Bubble(T, 3)),
    (Lagrange(S, 4), Bubble(S, 4)),
    (Lagrange(I, 1), Lagrange(I, 1)),
    (Lagrange(I, 1), Bubble(I, 2), Bubble(I, 2)),
])
def test_illposed_nodal_enriched(elements):
    """Check that nodal enriched element fails on ill-posed
    (non-unisolvent) case
    """
    with pytest.raises(np.linalg.LinAlgError):
        NodalEnrichedElement(*elements)


def test_empty_bubble():
    "Check that bubble of too low degree fails"
    with pytest.raises(RuntimeError):
        Bubble(I, 1)
    with pytest.raises(RuntimeError):
        Bubble(T, 2)
    with pytest.raises(RuntimeError):
        Bubble(S, 3)


def test_nodal_enriched_implementation():
    """Following element pair should be the same.
    This might be fragile to dof reordering but works now.
    """

    e0 = RaviartThomas(T, 2)

    e1 = NodalEnrichedElement(
        RestrictedElement(RaviartThomas(T, 2), restriction_domain='facet'),
        RestrictedElement(RaviartThomas(T, 2), restriction_domain='interior')
    )

    for attr in ["degree",
                 "get_reference_element",
                 "entity_dofs",
                 "entity_closure_dofs",
                 "get_formdegree",
                 "mapping",
                 "num_sub_elements",
                 "space_dimension",
                 "value_shape",
                 "is_nodal",
                 ]:
        assert getattr(e0, attr)() == getattr(e1, attr)()
    assert np.allclose(e0.get_coeffs(), e1.get_coeffs())
    assert np.allclose(e0.dmats(), e1.dmats())
    assert np.allclose(e0.get_dual_set().to_riesz(e0.get_nodal_basis()),
                       e1.get_dual_set().to_riesz(e1.get_nodal_basis()))


if __name__ == '__main__':
    import os
    pytest.main(os.path.abspath(__file__))
