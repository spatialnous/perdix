# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2020 Space Syntax Ltd
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

import unittest

from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsFeature,
    QgsLineString,
    QgsPoint,
    QgsMultiLineString,
)

from perdix.gate_transformer import TransformerAnalysis
from perdix.utilities.exceptions import BadInputError

qgs = QgsApplication([], False)
qgs.initQgis()


class TestGateTransformer(unittest.TestCase):
    @staticmethod
    def make_single_feature_layer(layertype: str, geometry):
        vl = QgsVectorLayer(layertype, "temp", "memory")
        pr = vl.dataProvider()
        f = QgsFeature()
        f.setGeometry(geometry)
        pr.addFeature(f)
        vl.updateExtents()
        return vl

    def test_rotate(self):
        vl = TestGateTransformer.make_single_feature_layer(
            "LineString", QgsLineString([QgsPoint(210, 41), QgsPoint(301, 55)])
        )
        self.assertEqual(vl.featureCount(), 1)
        TransformerAnalysis.GateTransformer.rotate_line(vl, 90)
        rot_feat = next(vl.getFeatures()).geometry().asPolyline()
        self.assertAlmostEqual(rot_feat[0][0], 248.5, places=3)
        self.assertAlmostEqual(rot_feat[0][1], 93.5, places=3)
        self.assertAlmostEqual(rot_feat[1][0], 262.5, places=3)
        self.assertAlmostEqual(rot_feat[1][1], 2.5, places=3)

    def test_resize(self):
        vl = TestGateTransformer.make_single_feature_layer(
            "LineString", QgsLineString([QgsPoint(210, 41), QgsPoint(301, 55)])
        )
        self.assertEqual(vl.featureCount(), 1)
        TransformerAnalysis.GateTransformer.resize_line(vl, 0.5)
        rot_feat = next(vl.getFeatures()).geometry().asPolyline()
        self.assertAlmostEqual(rot_feat[0][0], 255.7470, places=3)
        self.assertAlmostEqual(rot_feat[0][1], 48.0380, places=3)
        self.assertAlmostEqual(rot_feat[1][0], 255.2529, places=3)
        self.assertAlmostEqual(rot_feat[1][1], 47.9619, places=3)

    def test_rescale(self):
        vl = TestGateTransformer.make_single_feature_layer(
            "LineString", QgsLineString([QgsPoint(210, 41), QgsPoint(301, 55)])
        )
        self.assertEqual(vl.featureCount(), 1)
        TransformerAnalysis.GateTransformer.rescale_line(vl, 15)
        rot_feat = next(vl.getFeatures()).geometry().asPolyline()
        self.assertAlmostEqual(rot_feat[0][0], 938.0, places=3)
        self.assertAlmostEqual(rot_feat[0][1], 153.0, places=3)
        self.assertAlmostEqual(rot_feat[1][0], -427.0, places=3)
        self.assertAlmostEqual(rot_feat[1][1], -56.9999, places=3)

    def test_except_check_singlepart_lines_not_lines(self):
        vl = TestGateTransformer.make_single_feature_layer("Point", QgsPoint(210, 41))
        with self.assertRaises(BadInputError) as e:
            TransformerAnalysis.GateTransformer.check_singlepart_lines(vl)
        self.assertEqual(str(e.exception), "Only line layers can be resized")

    def test_except_check_singlepart_lines_no_parts(self):
        mls = QgsMultiLineString()

        vl = TestGateTransformer.make_single_feature_layer("MultiLineString", mls)
        with self.assertRaises(BadInputError) as e:
            TransformerAnalysis.GateTransformer.check_singlepart_lines(vl)
        self.assertEqual(
            str(e.exception), "Feature with id 1 has no line geometry, please correct"
        )

    def test_except_check_singlepart_lines_more_parts(self):
        mls = QgsMultiLineString()
        mls.addGeometry(QgsLineString([QgsPoint(210, 41), QgsPoint(301, 55)]))
        mls.addGeometry(QgsLineString([QgsPoint(210, 55), QgsPoint(301, 41)]))

        vl = TestGateTransformer.make_single_feature_layer("MultiLineString", mls)
        with self.assertRaises(BadInputError) as e:
            TransformerAnalysis.GateTransformer.check_singlepart_lines(vl)
        self.assertEqual(
            str(e.exception),
            "Feature with id 1 contains more than 1 line, please correct",
        )

    def test_except_check_singlepart_lines_no_vertices(self):
        vl = TestGateTransformer.make_single_feature_layer(
            "LineString", QgsLineString([])
        )
        with self.assertRaises(BadInputError) as e:
            TransformerAnalysis.GateTransformer.check_singlepart_lines(vl)
        self.assertEqual(
            str(e.exception), "Line with id 1 has fewer than 2 vertices, please correct"
        )

    def test_except_check_singlepart_lines_one_vertex(self):
        vl = TestGateTransformer.make_single_feature_layer(
            "LineString", QgsLineString([QgsPoint(210, 41)])
        )
        with self.assertRaises(BadInputError) as e:
            TransformerAnalysis.GateTransformer.check_singlepart_lines(vl)
        self.assertEqual(
            str(e.exception), "Line with id 1 has fewer than 2 vertices, please correct"
        )

    def test_except_check_singlepart_lines_more_vertices(self):
        vl = TestGateTransformer.make_single_feature_layer(
            "LineString",
            QgsLineString([QgsPoint(210, 41), QgsPoint(301, 55), QgsPoint(107, 115)]),
        )
        with self.assertRaises(BadInputError) as e:
            TransformerAnalysis.GateTransformer.check_singlepart_lines(vl)
        self.assertEqual(
            str(e.exception), "Line with id 1 has more than 2 vertices, please correct"
        )


if __name__ == "__main__":
    unittest.main()

qgs.exitQgis()
