# -*- coding:utf-8 -*-
#
# Created by Douglas Thor, Dec. 2014.
# Modified from Pierre Raybaut's p_pylint.py, © 2009-2011
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""Coverage Code Analysis Plugin"""

# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=R0911
# pylint: disable=R0201

from spyderlib.qt.QtGui import QInputDialog, QVBoxLayout, QGroupBox, QLabel
from spyderlib.qt.QtCore import SIGNAL, Qt

# Local imports
from spyderlib.baseconfig import get_translation
_ = get_translation("p_coverage", dirname="spyderplugins")
from spyderlib.utils.qthelpers import get_icon, create_action
from spyderlib.plugins import SpyderPluginMixin, PluginConfigPage

from spyderplugins.widgets.coveragegui import CoverageWidget, COVERAGE_PATH


class CoverageConfigPage(PluginConfigPage):
    def setup_page(self):
        """
        Create the Spyder Config page for this plugin.

        As of Dec 2014, there are no options available to set, so we only
        display the data path.
        """
        results_group = QGroupBox(_("Results"))
        results_label1 = QLabel(_("Results are stored here:"))
        results_label1.setWordWrap(True)

        # Warning: do not try to regroup the following QLabel contents with
        # widgets above -- this string was isolated here in a single QLabel
        # on purpose: to fix Issue 863
        results_label2 = QLabel(CoverageWidget.DATAPATH)

        results_label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        results_label2.setWordWrap(True)

        results_layout = QVBoxLayout()
        results_layout.addWidget(results_label1)
        results_layout.addWidget(results_label2)
        results_group.setLayout(results_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(results_group)
        vlayout.addStretch(1)
        self.setLayout(vlayout)


class Coverage(CoverageWidget, SpyderPluginMixin):
    """Python source code analysis based on pylint"""
    CONF_SECTION = 'coverage'
    CONFIGWIDGET_CLASS = CoverageConfigPage

    def __init__(self, parent=None):
        CoverageWidget.__init__(self, parent=parent,
                                max_entries=self.get_option('max_entries', 50))
        SpyderPluginMixin.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()

    #------ SpyderPluginWidget API --------------------------------------------
    def get_plugin_title(self):
        """Return widget title"""
        return _("Coverage")

    def get_plugin_icon(self):
        """Return widget icon"""
        return get_icon('pylint.png')

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.resultswidget

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        # Font
#        history_action = create_action(self, _("History..."),
#                                       None, 'history.png',
#                                       _("Set history maximum entries"),
#                                       triggered=self.change_history_depth)
#        self.resultswidget.common_actions += (None, history_action)
        return []

    def on_first_registration(self):
        """Action to be performed on first plugin registration"""
        self.main.tabify_plugins(self.main.inspector, self)
        self.dockwidget.hide()

    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        self.connect(self, SIGNAL("edit_goto(QString,int,QString)"),
                     self.main.editor.load)
        self.connect(self, SIGNAL('redirect_stdio(bool)'),
                     self.main.redirect_internalshell_stdio)
        self.main.add_dockwidget(self)

        coverage_act = create_action(self,
                                     _("Run code_coverage analysis"),
                                     triggered=self.run_coverage)
        coverage_act.setEnabled(COVERAGE_PATH is not None)
        self.register_shortcut(coverage_act, context="coverage",
                               name="run analysis",
                               default="Alt+F11")

        self.main.source_menu_actions += [None, coverage_act]
        self.main.editor.pythonfile_dependent_actions += [coverage_act]

    def refresh_plugin(self):
        """Refresh coverage widget"""
        self.remove_obsolete_items()

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True

    def apply_plugin_settings(self, options):
        """Apply configuration file's plugin settings"""
        # The history depth option will be applied at
        # next Spyder startup, which is soon enough
        pass

    #------ Public API --------------------------------------------------------
    # TODO: Get rid of this superfluous code
    def change_history_depth(self):
        "Change history max entries"""
        depth, valid = QInputDialog.getInteger(self, _('History'),
                                               _('Maximum entries'),
                                               self.get_option('max_entries'),
                                               10,
                                               10000)
        if valid:
            self.set_option('max_entries', depth)

    def run_coverage(self):
        """Run coverage code analysis"""
        if self.get_option('save_before', True)\
           and not self.main.editor.save():
            return
        self.analyze(self.main.editor.get_current_filename())

    def analyze(self, filename):
        """Reimplement analyze method"""
        if self.dockwidget and not self.ismaximized:
            self.dockwidget.setVisible(True)
            self.dockwidget.setFocus()
            self.dockwidget.raise_()
        CoverageWidget.analyze(self, filename)


#==============================================================================
# The following statements are required to register this 3rd party plugin:
#==============================================================================
PLUGIN_CLASS = Coverage
