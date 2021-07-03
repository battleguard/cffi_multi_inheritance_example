#******************************************************************************
# CUI
#
# The Advanced Framework for Simulation, Integration, and Modeling (AFSIM)
#
# This is a US Government Work not subject to copyright protection in the US.
#
# The use, dissemination or disclosure of data in this file is subject to
# limitation or restriction. See accompanying README and LICENSE for details.
#******************************************************************************
#
#******************************************************************************

from afsim.afsim_interface import AfsimFFI

__all__ = ['Object']


class Object(AfsimFFI):
    def __init__(self):
        AfsimFFI.__init__(self)
        self._ptr = None

    def get_name(self) -> str:
        """
        Get the name of the object.

        Returns
        -------
        str
            Returns a string containing the name of the object.
        """
        return AfsimFFI.to_str(AfsimFFI.LIB.Object_GetName(self._ptr))

    def get_name_id(self) -> str:
        """
        Get the string ID of the name of the object.

        Returns
        -------
        Returns a string containing the string ID of the name of the object.
        """
        return AfsimFFI.to_str(AfsimFFI.LIB.Object_GetNameId(self._ptr))

    def set_name(self, name: str) -> None:
        """
        Get the name of the object.

        Parameters
        ----------
        name : str
            The name of the object
        """
        AfsimFFI.LIB.Object_SetName(AfsimFFI._ptr, name.encode())

    def get_type(self) -> str:
        """
        Get the 'type' of the object.

        Returns
        -------
        str
            Returns a string containing the 'type' of the object.
        """
        return AfsimFFI.to_str(AfsimFFI.LIB.Object_GetType(self._ptr))

    def get_type_id(self) -> str:
        """
        Get the string ID of the 'type' of the object.

        Returns
        -------
        str
            Returns the string ID of the type of object
        """
        return AfsimFFI.to_str(AfsimFFI.LIB.Object_GetTypeId(self._ptr))

    def set_type(self, type_: str) -> None:
        """
        Set the 'type' of the object.
        Parameters
        ----------
        type_ : str
            The type to be assigned to the object.
        """
        AfsimFFI.LIB.Object_SetType(self._ptr, type_.encode())

    def get_base_type(self) -> str:
        """
        Get the 'base type' of the object

        Returns
        -------
        str
            Returns the base type
        """
        return AfsimFFI.to_str(AfsimFFI.LIB.Object_GetBaseType(self._ptr))

    def get_base_type_id(self) -> str:
        """
        Get the string ID of the object from which this object derives.

        Returns
        -------
        str
            Returns the string Id of the base type
        """
        return AfsimFFI.to_str(AfsimFFI.LIB.Object_GetBaseTypeId(self._ptr))

    def is_a_typeof(self, type_: str) -> bool:
        """
        Check if is type

        Parameters
        ----------
        type_ str
          Type to be checked

        Returns
        -------
        bool
            Returns true if it is a type
        """
        return bool(AfsimFFI.LIB.Object_IsA_TypeOf(self._ptr, type_.encode()))
