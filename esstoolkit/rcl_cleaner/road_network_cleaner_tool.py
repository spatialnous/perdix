# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RoadNetworkCleaner
                                 A QGIS plugin
 This plugin clean a road centre line map.
                              -------------------
        begin                : 2016-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Space SyntaxLtd
        email                : i.kolovou@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import traceback
from PyQt4.QtCore import QThread, QSettings
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
import operator
import os
from PyQt4.QtCore import QPyNullVariant

from road_network_cleaner_dialog import RoadNetworkCleanerDialog
from sGraph.sGraph import * # better give these a name to make it explicit to which module the methods belong
from sGraph.utilityFunctions import *

# Import the debug library - required for the cleaning class in separate thread
# set is_debug to False in release version
is_debug = False
try:
    import pydevd_pycharm
    has_pydevd = True
except ImportError, e:
    has_pydevd = False
    is_debug = False

import sys
#sys.path.append("pydevd-pycharm.egg")

class NetworkCleanerTool(QObject):

    # initialise class with self and iface
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface=iface
        self.legend = self.iface.legendInterface()

        # load the dialog from the run method otherwise the objects gets created multiple times
        self.dlg = None

        # some globals
        self.cleaning = None
        self.thread = None

    def loadGUI(self):
        # create the dialog objects
        self.dlg = RoadNetworkCleanerDialog(self.getQGISDbs())

        # setup GUI signals
        self.dlg.closingPlugin.connect(self.unloadGUI)
        self.dlg.cleanButton.clicked.connect(self.startWorker)
        self.dlg.cancelButton.clicked.connect(self.killWorker)

        # add layers to dialog
        self.updateLayers()

        if self.dlg.getNetwork():
            self.dlg.outputCleaned.setText(self.dlg.inputCombo.currentText() + "_cl")
            self.dlg.dbsettings_dlg.nameLineEdit.setText(self.dlg.inputCombo.currentText() + "_cl")
        self.dlg.inputCombo.currentIndexChanged.connect(self.updateOutputName)

        # setup legend interface signals
        self.legend.itemAdded.connect(self.updateLayers)
        self.legend.itemRemoved.connect(self.updateLayers)

        self.settings = None

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

    def unloadGUI(self):
        if self.dlg:
            self.dlg.closingPlugin.disconnect(self.unloadGUI)
            self.dlg.cleanButton.clicked.disconnect(self.startWorker)
            self.dlg.cancelButton.clicked.disconnect(self.killWorker)
            self.settings = None
        self.legend.itemAdded.disconnect(self.updateLayers)
        self.legend.itemRemoved.disconnect(self.updateLayers)

        self.dlg = None

    def getQGISDbs(self):
        """Return all PostGIS connection settings stored in QGIS
        :return: connection dict() with name and other settings
        """
        settings = QSettings()
        settings.beginGroup('/PostgreSQL/connections')
        named_dbs = settings.childGroups()
        all_info = [i.split("/") + [unicode(settings.value(i))] for i in settings.allKeys() if
                    settings.value(i) != NULL and settings.value(i) != '']
        all_info = [i for i in all_info if
                    i[0] in named_dbs and i[2] != NULL and i[1] in ['name', 'host', 'service', 'password', 'username', 'database',
                                                                    'port']]
        dbs = dict(
            [k, dict([i[1:] for i in list(g)])] for k, g in itertools.groupby(sorted(all_info), operator.itemgetter(0)))
        QgsMessageLog.logMessage('dbs %s' % str(dbs), level=QgsMessageLog.CRITICAL)
        settings.endGroup()

        return dbs

    def getActiveLayers(self):
        layers_list = []
        for layer in self.iface.legendInterface().layers():
            if layer.isValid() and layer.type() == QgsMapLayer.VectorLayer:
                if layer.hasGeometryType() and (layer.geometryType() == 1):
                    layers_list.append(layer.name())
        return layers_list

    def updateLayers(self):
        layers = self.getActiveLayers()
        self.dlg.popActiveLayers(layers)

    # SOURCE: Network Segmenter https://github.com/OpenDigitalWorks/NetworkSegmenter
    # SOURCE: https://snorfalorpagus.net/blog/2013/12/07/multithreading-in-qgis-python-plugins/

    def updateOutputName(self):
        if self.dlg.memoryRadioButton.isChecked():
            self.dlg.outputCleaned.setText(self.dlg.inputCombo.currentText() + "_cl")
        else:
            self.dlg.outputCleaned.clear()
        self.dlg.dbsettings_dlg.nameLineEdit.setText(self.dlg.inputCombo.currentText() + "_cl")

    def giveMessage(self, message, level):
        # Gives warning according to message
        self.iface.messageBar().pushMessage("Road network cleaner: ", "%s" % (message), level, duration=5)

    def workerError(self, e, exception_string):
        # Gives error according to message
        QgsMessageLog.logMessage('Cleaning thread raised an exception: %s' % exception_string, level=QgsMessageLog.CRITICAL)
        self.dlg.close()

    def startWorker(self):
        self.dlg.cleaningProgress.reset()
        self.settings = self.dlg.get_settings()
        if self.settings['output_type'] == 'postgis':
            db_settings = self.dlg.get_dbsettings()
            self.settings.update(db_settings)

        if getLayerByName(self.settings['input']).crs().postgisSrid() == 4326:
            self.giveMessage('Re-project the layer. EPSG:4326 not allowed.', QgsMessageBar.INFO)
            return
        elif self.settings['output'] != '':

            cleaning = self.Worker(self.settings, self.iface)
            # start the cleaning in a new thread
            self.dlg.lockGUI(True)
            self.dlg.lockSettingsGUI(True)
            thread = QThread()
            cleaning.moveToThread(thread)
            cleaning.finished.connect(self.workerFinished)
            cleaning.error.connect(self.workerError)
            cleaning.warning.connect(self.giveMessage)
            cleaning.cl_progress.connect(self.dlg.cleaningProgress.setValue)

            thread.started.connect(cleaning.run)

            thread.start()

            self.thread = thread
            self.cleaning = cleaning

            if is_debug:
                print 'started'
        else:
            self.giveMessage('Missing user input!', QgsMessageBar.INFO)
            return

    def workerFinished(self, ret):
        if is_debug:
            print 'trying to finish'
        self.dlg.lockGUI(False)
        #TODO: only if edit default has been pressed before
        self.dlg.lockSettingsGUI(False)
        # get cleaning settings
        layer_name = self.settings['input']
        path, unlinks_path, errors_path  = self.settings['output'] # if postgis: connstring, schema, table_name

        output_type = self.settings['output_type']
        #  get settings from layer
        layer = getLayerByName(layer_name)

        if self.cleaning:
            # clean up the worker and thread
            self.cleaning.finished.disconnect(self.workerFinished)
            self.cleaning.error.disconnect(self.workerError)
            self.cleaning.warning.disconnect(self.giveMessage)
            self.cleaning.cl_progress.disconnect(self.dlg.cleaningProgress.setValue)

        # clean up the worker and thread
        self.thread.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()

        if ret:

            cleaned_features, errors_features, unlinks_features = ret

            print 'path', path
            if self.settings['errors']:
                if len(errors_features) > 0:
                    errors = to_layer(errors_features, layer.crs(), layer.dataProvider().encoding(), 'Point', output_type, errors_path)
                    errors.loadNamedStyle(os.path.dirname(__file__) + '/qgis_styles/errors.qml')
                    QgsMapLayerRegistry.instance().addMapLayer(errors)
                    self.iface.legendInterface().refreshLayerSymbology(errors)
                    QgsMessageLog.logMessage('layer name %s' % layer_name, level=QgsMessageLog.CRITICAL)
                else:
                    self.giveMessage('No errors detected!', QgsMessageBar.INFO)

            if self.settings['unlinks']:
                if len(unlinks_features) > 0:
                    unlinks = to_layer(unlinks_features, layer.crs(), layer.dataProvider().encoding(), 'Point', output_type, unlinks_path)
                    unlinks.loadNamedStyle(os.path.dirname(__file__) + '/qgis_styles/unlinks.qml')
                    QgsMapLayerRegistry.instance().addMapLayer(unlinks)
                    self.iface.legendInterface().refreshLayerSymbology(unlinks)
                else:
                    self.giveMessage('No unlinks detected!', QgsMessageBar.INFO)

            cleaned = to_layer(cleaned_features, layer.crs(), layer.dataProvider().encoding(), 'Linestring', output_type, path)
            cleaned.loadNamedStyle(os.path.dirname(__file__) + '/qgis_styles/cleaned.qml')
            QgsMapLayerRegistry.instance().addMapLayer(cleaned)
            self.iface.legendInterface().refreshLayerSymbology(cleaned)
            cleaned.updateExtents()

            self.giveMessage('Process ended successfully!', QgsMessageBar.INFO)
            self.dlg.cleaningProgress.setValue(100)

        else:
            # notify the user that sth went wrong
            self.giveMessage('Something went wrong! See the message log for more information', QgsMessageBar.CRITICAL)

        self.thread = None
        self.cleaning = None

        if self.dlg:
            self.dlg.cleaningProgress.reset()
            self.dlg.close()

    def killWorker(self):
        if is_debug: print 'trying to cancel'
        # add emit signal to breakTool or mergeTool only to stop the loop
        if self.cleaning:
            # Disconnect signals
            self.cleaning.finished.disconnect(self.workerFinished)
            self.cleaning.error.disconnect(self.workerError)
            self.cleaning.warning.disconnect(self.giveMessage)
            self.cleaning.cl_progress.disconnect(self.dlg.cleaningProgress.setValue)
            try: # it might not have been connected already
                self.cleaning.graph.progress.disconnect(self.dlg.cleaningProgress.setValue)
            except TypeError:
                pass
            # Clean up thread and analysis
            self.cleaning.kill()
            self.cleaning.graph.kill() #todo
            self.cleaning.deleteLater()
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()
            self.cleaning = None
            self.dlg.cleaningProgress.reset()
            self.dlg.close()
        else:
            self.dlg.close()


    # SOURCE: https://snorfalorpagus.net/blog/2013/12/07/multithreading-in-qgis-python-plugins/
    class Worker(QObject):

        # Setup signals
        finished = pyqtSignal(object)
        error = pyqtSignal(Exception, basestring)
        cl_progress = pyqtSignal(float)
        warning = pyqtSignal(str)
        cl_killed = pyqtSignal(bool)

        def __init__(self, settings, iface):
            QObject.__init__(self)
            self.settings = settings
            self.cl_killed = False
            self.iface = iface
            self.pseudo_graph = sGraph({}, {})
            self.graph = None

        def run(self):
            if has_pydevd and is_debug:
                pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True, suspend=False)
            ret = None
            #if self.settings:
            try:
                # cleaning settings
                layer_name = self.settings['input']
                layer = getLayerByName(layer_name)
                snap_threshold = self.settings['snap']
                break_at_vertices = self.settings['break']
                merge_type = self.settings['merge']
                collinear_threshold = self.settings['collinear_angle']
                angle_threshold = self.settings['simplification_threshold']
                fix_unlinks = self.settings['fix_unlinks']
                orphans = self.settings['orphans']
                getUnlinks = self.settings['unlinks']
                [load_range, cl1_range, cl2_range, cl3_range, break_range, merge_range, snap_range, unlinks_range, fix_range] = self.settings['progress_ranges']
                QgsMessageLog.logMessage('settings %s' % self.settings, level=QgsMessageLog.CRITICAL)

                self.cl_progress.emit(0)

                if break_at_vertices:

                    self.pseudo_graph.step = load_range / float(layer.featureCount())
                    self.pseudo_graph.progress.connect(self.cl_progress.emit)
                    self.graph = sGraph({}, {})
                    self.graph.total_progress = load_range
                    self.pseudo_graph.load_edges_w_o_topology(clean_features_iter(layer.getFeatures()))
                    QgsMessageLog.logMessage('pseudo_graph edges added %s' % load_range, level=QgsMessageLog.CRITICAL)
                    self.pseudo_graph.step = break_range / float(len(self.pseudo_graph.sEdges))
                    self.graph.load_edges(self.pseudo_graph.break_features_iter(getUnlinks, angle_threshold, fix_unlinks), angle_threshold)
                    QgsMessageLog.logMessage('pseudo_graph edges broken %s' % break_range, level=QgsMessageLog.CRITICAL)
                    self.pseudo_graph.progress.disconnect()
                    self.graph.progress.connect(self.cl_progress.emit)
                    self.graph.total_progress = self.pseudo_graph.total_progress

                else:
                    self.graph = sGraph({}, {})
                    self.graph.progress.connect(self.cl_progress.emit)
                    self.graph.step = load_range / float(layer.featureCount())
                    self.graph.load_edges(clean_features_iter(layer.getFeatures()), angle_threshold)
                    QgsMessageLog.logMessage('graph edges added %s' % load_range, level=QgsMessageLog.CRITICAL)

                self.graph.step = cl1_range / (float(len(self.graph.sEdges)) * 2.0)
                if orphans:
                    self.graph.clean(True, False, snap_threshold, True)
                else:
                    self.graph.clean(True, False, snap_threshold, False)
                QgsMessageLog.logMessage('graph clean parallel and closed pl %s' % cl1_range, level=QgsMessageLog.CRITICAL)

                if fix_unlinks:

                    self.graph.step = fix_range / float(len(self.graph.sEdges))
                    self.graph.fix_unlinks()
                    QgsMessageLog.logMessage('unlinks added  %s' % fix_range, level=QgsMessageLog.CRITICAL)

                # TODO clean iteratively until no error

                if snap_threshold != 0:

                    self.graph.step = snap_range / float(len(self.graph.sNodes))
                    self.graph.snap_endpoints(snap_threshold)
                    QgsMessageLog.logMessage('snap  %s' % snap_range, level=QgsMessageLog.CRITICAL)
                    self.graph.step = cl2_range / (float(len(self.graph.sEdges)) * 2.0)

                    if orphans:
                        self.graph.clean(True, False, snap_threshold, True)
                    else:
                        self.graph.clean(True, False, snap_threshold, False)
                    QgsMessageLog.logMessage('clean   %s' % cl2_range, level=QgsMessageLog.CRITICAL)

                if merge_type == 'intersections':

                    self.graph.step = merge_range / float(len(self.graph.sNodes))
                    self.graph.merge_b_intersections(angle_threshold)
                    QgsMessageLog.logMessage('merge %s %s angle_threshold ' % (merge_range, angle_threshold), level=QgsMessageLog.CRITICAL)

                elif merge_type == 'collinear':

                    self.graph.step = merge_range / float(len(self.graph.sEdges))
                    self.graph.merge_collinear(collinear_threshold, angle_threshold)
                    QgsMessageLog.logMessage('merge  %s' % merge_range, level=QgsMessageLog.CRITICAL)

                # cleaned multiparts so that unlinks are generated properly
                if orphans:
                    self.graph.step = cl3_range / (float(len(self.graph.sEdges)) * 2.0)
                    self.graph.clean(True, orphans, snap_threshold, False, True)
                    QgsMessageLog.logMessage('clean  %s' % cl3_range, level=QgsMessageLog.CRITICAL)
                else:
                    self.graph.step = cl3_range / (float(len(self.graph.sEdges)) * 2.0)
                    self.graph.clean(True, False, snap_threshold, False, True)
                    QgsMessageLog.logMessage('clean %s' % cl3_range, level=QgsMessageLog.CRITICAL)

                if getUnlinks:

                    self.graph.step = unlinks_range / float(len(self.graph.sEdges))
                    self.graph.generate_unlinks()
                    QgsMessageLog.logMessage('unlinks generated %s' % unlinks_range, level=QgsMessageLog.CRITICAL)
                    unlinks = self.graph.unlinks
                else:
                    unlinks = []

                cleaned_features = map(lambda e: e.feature, self.graph.sEdges.values())
                # add to errors multiparts and points
                self.graph.errors += multiparts
                self.graph.errors += points

                if is_debug: print "survived!"
                self.graph.progress.disconnect()
                self.cl_progress.emit(95)
                # return cleaned data, errors and unlinks
                ret = cleaned_features, self.graph.errors, unlinks

            except Exception, e:
                # forward the exception upstream
                self.error.emit(e, traceback.format_exc())

            self.finished.emit(ret)

        def kill(self):
            self.cl_killed = True
