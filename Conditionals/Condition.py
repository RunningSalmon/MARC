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
        """
            Returns true if the condition applies to the given abstract object
        """
        pass

    @abstractmethod
    def explains_grouping(self, affected_group: list[AbstractObject], unaffected_group: list[AbstractObject]) -> list[
        'Condition']:
        """
            Returns a list of conditions that separates the two groups of abstract objects
            :arg affected_group: The group that is affected by the condition
            :arg unaffected_group: The group that is not affected by the condition
        """
        pass

    def __repr__(self):
        return f"'{type(self).__name__}' with fixed parameter: {self.fixed_parameter}"
