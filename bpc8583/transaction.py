import struct
from datetime import datetime

from bpc8583.ISO8583 import ISO8583
from bpc8583.tools import trace, get_date, get_datetime_with_year, get_datetime, get_stan
from bpc8583.spec import IsoSpec, IsoSpec1987BPC
from pytlv.TLV import TLV


class Transaction():
    def __init__(self, type, card, term):
        """
        """
        self.TLV = TLV()

        self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
        self.card = card
        self.term = term
        self.type = type.lower()
        self.description = ''
        self.expected_response_code = '000'
        self.expected_response_action = None

        if self.type in ['logon', 'echo']:
            """
            """
            self.IsoMessage.MTI("0800")

            self.IsoMessage.FieldData(3, 990000)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(24, 801)

        elif self.type == 'key change':
            """
            """
            self.IsoMessage.MTI("0800")

            self.IsoMessage.FieldData(3, 990000)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(24, 811)

        elif self.type == 'balance':
            """
            """
            self.IsoMessage.MTI("0100")
            
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(3, 310000)
            self.IsoMessage.FieldData(4, 0)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(13, 1216)
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'purchase':
            """
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
            self.IsoMessage.MTI("0200")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(3, 000000)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        else:
            print('Unknown transaction type: {}'.format(type))
            return None
    
        # Common message fields:
        self.IsoMessage.FieldData(7, get_datetime())
        self.IsoMessage.FieldData(11, get_stan())
        self.IsoMessage.FieldData(41, self.term.get_terminal_id())
        self.IsoMessage.FieldData(42, self.term.get_merchant_id())
        self.IsoMessage.FieldData(49, self.term.get_currency_code())

        if self.type in ['purchase', 'balance'] and card.get_service_code()[0] in ['2', '6']:
            self.IsoMessage.FieldData(55, self.build_emv_data())

        self.rebuild()


    def get_data(self):
        """
        """
        return struct.pack("!H", len(self.data)) + self.data


    def rebuild(self):
        """
        Rebuild IsoMessage (e.g. after field data change)
        """
        self.data = self.IsoMessage.BuildIso()


    def trace(self, header=None):
        """
        """
        self.IsoMessage.Print(header=header)


    def set_description(self, description):
        """
        """
        self.description = description


    def get_description(self):
        """
        Get transaction description (for logging purposes)
        """
        if self.description:
            return self.description
        else:
            return self.type + ' ' + str(self.IsoMessage.FieldData(11))


    def set_PIN(self, PIN):
        """
        """
        if PIN:
            encrypted_pinblock = self.term.get_encrypted_pin(PIN, self.card.get_card_number())
            if encrypted_pinblock:
                self.IsoMessage.FieldData(52, encrypted_pinblock)
                self.rebuild()


    def set_amount(self, amount):
        """
        Set transaction amount
        """
        if amount:
            try:
                self.IsoMessage.FieldData(4, int(amount))
            except ValueError:
                self.IsoMessage.FieldData(4, 0)
            self.rebuild()


    def set_expected_code(self, expected_response_code):
        """
        Expected response code of the transaction
        """
        self.expected_response_code = expected_response_code


    def set_expected_action(self, expected_response_action):
        """
        Expected outcome of the transaction ('APPROVED' or 'DECLINED')
        """
        if expected_response_action.upper() not in ['APPROVED', 'APPROVE', 'DECLINED', 'DECLINE']:
            return False

        self.expected_response_action = expected_response_action.upper()
        return True


    def is_response_expected(self, actual_response_code):
        """
        """
        if self.expected_response_action in ['APPROVED', 'APPROVE']:
            if int(actual_response_code) == 0:
                return True
            else:
                return False

        elif self.expected_response_action in ['DECLINED', 'DECLINE']:
            if int(actual_response_code) != 0:
                return True
            else:
                return False
        else:
            # no response action available, compare the response codes:
            if self.expected_response_code:
                if self.expected_response_code == actual_response_code:
                    return True
                else:
                    return False
            else:
                # neither response action, nor response code are set
                return None

        return True


    def _get_app_interchange_profile(self):
        """
        Contains the data objects (with tags and lengths) returned by the ICC in response to a command
        """
        #return '9A039505'
        return '0000'


    def build_emv_data(self):
        """
        TODO:
        95    TVR
        82    app_int_prof 
        """
        emv_data = ''
        emv_data += self.TLV.build({'82': self._get_app_interchange_profile()})
        emv_data += self.TLV.build({'9A': get_date()})
        emv_data += self.TLV.build({'95': self.term.get_tvr()})
        emv_data += self.TLV.build({'9F10': self.card.get_iss_application_data()})
        emv_data += self.TLV.build({'9F26': self.card.get_application_cryptogram()})
        emv_data += self.TLV.build({'9F36': self.card.get_transaction_counter()})
        emv_data += self.TLV.build({'9F37': self.term.get_unpredno()})
        emv_data += self.TLV.build({'9F1A': self.term.get_country_code()})


        return emv_data
