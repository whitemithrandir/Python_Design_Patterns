import datetime as dt
from typing import Generator, List
import inspect



class DateMonth():
    
    def __init__(self, year:int, month:int) -> None:
        self.year = year
        self.month = month
    
    @staticmethod
    def from_str(datemonth: str) -> 'DateMonth':
        date = dt.datetime.strptime(datemonth, "%Y%m")
        return DateMonth(year=date.year, month=date.month)

    @staticmethod
    def from_date(date: dt.date) -> 'DateMonth':
        return DateMonth(year=date.year, month=date.month)
    
    def __str__(self) -> str:
        return str(self.year) + str(self.month).rjust(2, '0')
    
    def __repr__(self) -> str:
        return str(self)
    
    def first_date(self) -> dt.date:
        return dt.date(self.year, self.month, 1)
    
    def last_date(self) -> dt.date:
        date = dt.date(year=self.year, month=self.month, day=1)
        next_month_first_day = (date + dt.timedelta(days=32)).replace(day=1)
        return next_month_first_day - dt.timedelta(days=1)
    
    def next_month(self) -> 'DateMonth':
        year = self.year + ((self.month + 1) // 13)
        month = self.month + 1 if self.month < 12 else 1
        return DateMonth(year=year, month=month)

    @staticmethod
    def range(start_month: str, end_month:str) -> Generator['DateMonth', None, None]:
        currentmonth = DateMonth.from_str(start_month)
        while str(currentmonth) <= end_month:
            yield currentmonth
            currentmonth = currentmonth.next_month()
    
def get_subclasses(base_class, module) -> List[type]:
    subclasses = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, base_class) and obj != base_class:
            subclasses.append(obj)
    return subclasses


def get_model(model_name, module) -> type:
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and hasattr(obj, "name") and obj.name == model_name:
            return obj