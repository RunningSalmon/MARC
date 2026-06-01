from abc import ABC, abstractmethod
from typing import Optional

from Datatypes.Abstract_Object import AbstractObject


class ConditionParameter(ABC):
    pass

class Condition(ABC):
    @abstractmethod
    def __init__(self, parameter: Optional[ConditionParameter] = None):
        self.fixed_parameter = parameter

    @abstractmethod
    def applies_to(self, abstract_object: AbstractObject) -> bool:
        pass

    @abstractmethod
    def explains_grouping(self, affected_group: list[AbstractObject], unaffected_group: list[AbstractObject]) -> list['Condition']:
        pass

    def __repr__(self):
        return f"'{type(self).__name__}' with fixed parameter: {self.fixed_parameter}"
