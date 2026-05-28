from abc import ABC, abstractmethod
from typing import Optional

from Datatypes.Abstract_Object import AbstractObject


class ConditionParameter(ABC):
    pass

class Condition(ABC):
    @abstractmethod
    def applies_to(self, abstract_object: AbstractObject) -> bool:
        pass

    @abstractmethod
    def explains_grouping(self, affected_group: list[AbstractObject], unaffected_group: list[AbstractObject]) -> list['Condition']:
        pass