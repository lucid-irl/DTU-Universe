import logging

from PyQt5.QtCore import QObject, pyqtSignal
from class_convertType import toQCheckBox
import json
from typing import Dict, List, Tuple

from PyQt5.QtWidgets import QCheckBox, QPushButton, QWidget

class ExceptionSettingNotFound(Exception):
    def __init__(self, setting: str) -> None:
        super().__init__('{0} setting is not found'.format(setting))

class ExceptionSettingFileNotExist(Exception):

    def __init__(self, filename:str) -> None:
        self.filename = filename
        super().__init__("{0} setting is not exist!".format(filename))

class ExceptionClusterNotExist(Exception):

    def __init__(self, key:str) -> None:
        self.key = key
        super().__init__("{0} cluster is not exist!".format(key))

class ExceptionIsNotRightFormat(Exception):

    def __init__(self) -> None:
        super().__init__("the Imported json is not right format")

class ClusterSetting:

    def __init__(self, settings):
        self.settings = settings

    def getSetting(self, setting: str):
        return self.settings[setting]

class Setting:

    """Class này đại diện cho một file setting JSON hai cấp."""

    def __init__(self, importFile):
        self.importFile = importFile
        self.defaultSetting = {
                "system":{
                    "saveChoicedSubject":True,
                    "autoImportSubjectFile":True
                },
                "appearance":{
                    "darkMode":True
                },
                "itemListWidget":{
                    "showInfoWhenHover":True,
                    "showTeacherNameBySide":True
                },
                "itemConflictListWidget":{
                    "showDayConflict":True
                },
                "buttonWeekContainer":{
                    "highlightConflictWeekButton":True
                }
            }
        try:
            with open(importFile, 'r') as f:
                self.userSetting = json.load(f)
        except:
            with open(importFile, 'w') as f:
                json.dump(self.defaultSetting, f)
                self.userSetting = self.defaultSetting

    def getUserSetting(self) -> Dict:
        return self.userSetting
    
    def getCluster(self, cluster):
        return ClusterSetting(self.getUserSetting()[cluster])

    def setValueForSetting(self, cluster, setting, value):
        if value != None:
            try:
                self.userSetting[cluster][setting] = value
            except Exception as e:
                raise e
        else:
            Exception('Value must be not None!')

    def setDefaultSetting(self):
        self.userSetting = self.defaultSetting

    def save(self):
        logging.debug('save setting')
        with open(self.importFile, 'w') as f:
            json.dump(self.userSetting, f, indent=4)

class ConnectSettingToWidget(QObject):
    signal_settingChange = pyqtSignal(bool)
    signal_settingSave = pyqtSignal(bool)
    SAVE = True

    """Class tiêu chuẩn để kết nối các setting trong JSON file tương ứng với các Widget trong PyQt5."""
    def __init__(self, setting: Setting):
        super().__init__()
        self.setting = setting
        self.settingVsWidget: List[Dict[Tuple[str],QWidget]] = []

    def connectSettingToWidget(self, cluster: str, setting:str, qWidget: QWidget):
        """Connect một setting với một QWidget."""
        connection = {(cluster, setting): qWidget}
        self.settingVsWidget.append(connection)

    def whichIsSaveButton(self, qPushButton: QPushButton):
        self.saveButton = qPushButton
        self.saveButton.clicked.connect(self.save)

    def whichIsDefaultSettingButton(self, qPushButton: QPushButton):
        self.defaultSettingButton = qPushButton
        self.defaultSettingButton.clicked.connect(self.setDefaultToWidget)

    def setDefaultToWidget(self):
        logging.info('default setting button is clicked')
        self.setting.setDefaultSetting()

        for connection in self.settingVsWidget:
            clusterSetting = list(connection.keys())[0]
            widget = list(connection.values())[0]
            if not ConnectSettingToWidget.SAVE:
                widget.setStyleSheet("""QCheckBox::indicator:checked {
                image: url(./resources/icon_tick_gray.svg);
                }""")
            value = self.setting.getCluster(clusterSetting[0]).getSetting(clusterSetting[1])
            if type(widget) is QCheckBox:
                self.settingToCheckBox(value, widget)

        self.signal_settingChange.emit(False)

    def settingToCheckBox(self, value: bool, checkBox: QCheckBox):
        logging.debug('Run setting to Check box --> {0}'.format(checkBox))
        checkBox.setChecked(value)
        checkBox.clicked.connect(lambda: self.checkBoxClickWhenNonSave(checkBox))

    def checkBoxClickWhenNonSave(self, checkBox: QCheckBox):
        logging.debug('change style checkbox')
        self.SAVE = False
        checkBox.setStyleSheet(
            """QCheckBox::indicator:checked {
            image: url(./resources/icon_tick_gray.svg);
            }"""
        )
        self.signal_settingChange.emit(False)


    def run(self):
        logging.debug('Run connect setting')
        logging.debug('Setting is {0}'.format(self.settingVsWidget))
        for connection in self.settingVsWidget:
            clusterSetting = list(connection.keys())[0]
            widget = list(connection.values())[0]
            widget.setStyleSheet("""QCheckBox::indicator:checked {
            image: url(./resources/icon_tick_black.svg);
            }""")
            logging.debug('widget --> {0}'.format(widget))
            logging.debug('type widget --> {0}'.format(type(widget)))
            value = self.setting.getCluster(clusterSetting[0]).getSetting(clusterSetting[1])

            logging.debug('Value --> {0}'.format(value))
            if type(widget) is QCheckBox:
                self.settingToCheckBox(value, widget)

    def save(self):
        for connection in self.settingVsWidget:
            clusterSetting = list(connection.keys())[0]
            widget = list(connection.values())[0]
            if type(widget) is QCheckBox:
                if toQCheckBox(widget).isChecked():
                    widget.setStyleSheet("""QCheckBox::indicator:checked {
                        image: url(./resources/icon_tick_black.svg);
                        }""")
                    self.setting.setValueForSetting(clusterSetting[0], clusterSetting[1], True)
                else:
                    self.setting.setValueForSetting(clusterSetting[0], clusterSetting[1], False)
        self.setting.save()
        self.SAVE = True
        self.signal_settingSave.emit(True)

    def isSaved(self):
        return ConnectSettingToWidget.SAVE

            
if __name__ == "__main__":
    cn = ConnectSettingToWidget()

