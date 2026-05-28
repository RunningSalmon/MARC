from abc import ABC, abstractmethod

from Datatypes.Abstract_Object import AbstractObject


class ConditionParameter(ABC):
    pass

class Condition(ABC):
    @abstractmethod
    def applies_to(self, abstract_object: AbstractObject) -> bool:
        pass