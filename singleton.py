
import model_utils

class SettingManager:
    __instance = None
    __dates_dict = {}

    @staticmethod
    def get_instance():
        if SettingManager.__instance is None:
            SettingManager.__instance == SettingManager()
        return SettingManager.__instance
    
    def __init__(self) -> None:
        if SettingManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SettingManager.__instance = self

    def set_number(self, key, value):
        self.__dates_dict[key] = value

    def get_number(self, key):
        return self.__dates_dict.get(key, None)


result = model_utils.get_next_12_months()

test_manager = SettingManager.get_instance()

for i,j in zip(result, range(len(result))):
    key = result[j]
    value = model_utils.calculate_years(i, [2020])
    test_manager.set_number(key,value)

for j in result:
    print(test_manager.get_number(j))


# Yeni bir örnek oluşturulamaz
yeni_settings_manager = SettingManager()  
