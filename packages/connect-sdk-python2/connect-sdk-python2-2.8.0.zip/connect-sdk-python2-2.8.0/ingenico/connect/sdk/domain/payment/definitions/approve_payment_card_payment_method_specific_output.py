# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://epayments-api.developer-ingenico.com/s2sapi/v1/
#
from ingenico.connect.sdk.data_object import DataObject


class ApprovePaymentCardPaymentMethodSpecificOutput(DataObject):

    __void_response_id = None

    @property
    def void_response_id(self):
        """
        | Result of the authorization reversal request
        
        | Possible values are:
        
        * 00 - Successful reversal
        * 0, 8 or 11 - Reversal request submitted
        * 5 or 55 - Reversal request declined or referred
        * empty or 98 - The provider did not provide a response
        
        Type: str
        """
        return self.__void_response_id

    @void_response_id.setter
    def void_response_id(self, value):
        self.__void_response_id = value

    def to_dictionary(self):
        dictionary = super(ApprovePaymentCardPaymentMethodSpecificOutput, self).to_dictionary()
        self._add_to_dictionary(dictionary, 'voidResponseId', self.void_response_id)
        return dictionary

    def from_dictionary(self, dictionary):
        super(ApprovePaymentCardPaymentMethodSpecificOutput, self).from_dictionary(dictionary)
        if 'voidResponseId' in dictionary:
            self.void_response_id = dictionary['voidResponseId']
        return self
