import json
from typing import Dict

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


class Setting:

    """Class này đại diện cho một file setting JSON hai cấp."""

    def __init__(self, importFile):
        self.importFile = importFile
        self.defaultSetting = {
                "system":{
                    "saveChoicedSubject":1,
                    "autoImportSubjectFile":1
                },
                "appearance":{
                    "darkMode":1
                },
                "itemListWidget":{
                    "showInfoWhenHover":1,
                    "showTeacherNameBySide":1
                },
                "itemConflictListWidget":{
                    "showDayConflict":1
                },
                "buttonWeekContainer":{
                    "highlightConflictWeekButton":1
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
    
    def getClusterSettings(self):
        try:
            clusters = []
            for key, _ in self.getUserSetting().items():
                clusters.append(key)
            return clusters
        except Exception as e:
            raise e

    def setValueForSetting(self, cluster, setting, value):
        if value != None:
            try:
                self.userSetting[cluster][setting] = value
            except Exception as e:
                raise e
        else:
            Exception('Value must be not None!')

    def save(self):
        with open(self.importFile, 'w') as f:
            json.dump(self.userSetting, f, indent=4)


            
if __name__ == "__main__":
    st = Setting('cs4rsa_settings.json')
    print(st.getClusterSettings())

