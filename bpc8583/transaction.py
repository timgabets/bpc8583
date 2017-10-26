import struct
from datetime import datetime

from bpc8583.ISO8583 import ISO8583, currency_codes
from bpc8583.tools import get_date, get_datetime_with_year, get_datetime, get_stan, get_seconds_since_epoch, get_MMDD
from tracetools.tracetools import trace
from bpc8583.spec import IsoSpec, IsoSpec1987BPC
from pytlv.TLV import TLV

class Transaction():
    def __init__(self, type, card, term, icc_trxn=None, timeout=None):
        """
        """
        self.TLV = TLV()

        self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
        self.card = card
        self.term = term
        self.type = type.lower()
        self.description = ''
        self.account_from = '00'
        self.account_to = '00'
        self.expected_response_code = '000'
        self.expected_response_action = None
        self.currency = None
        self.PIN = None
        self._set_icc_trxn(icc_trxn)
        self.field48 = {}
        self.timeout = int(timeout) if timeout else 0

        if self.type in ['logon', 'echo']:
            """
            """
            self.IsoMessage.MTI("0800")

            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(24, 801)

        elif self.type == 'key change':
            """
            """
            self.IsoMessage.MTI("0800")

            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(24, 811)

        elif self.type == 'balance':
            """
            """
            self.IsoMessage.MTI("0100")
            
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(13, get_MMDD())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'purchase':
            """
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
            self.IsoMessage.MTI("0100")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'virtual purchase':
            """
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
            self.IsoMessage.MTI("0100")

            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)

        elif self.type == 'refund':
            """
            Refund
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
            self.IsoMessage.MTI("0100")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type in ['pin change', 'pin change reversal']:
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
            if self.type == 'pin change':
                self.IsoMessage.MTI("0100")
            elif self.type == 'pin change reversal':
                self.IsoMessage.MTI("0400")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'cash':
            """
            Cash
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
            self.IsoMessage.MTI("0100")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'dcc check':
            """
            DCC Availability check
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
            self.IsoMessage.MTI("0300")
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 301)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'create virtual card':
            """
            Create Virtual Card
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
            self.IsoMessage.MTI("0100")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        else:
            print('Unknown transaction type: {}'.format(type))
            return None
    
        # Common message fields:
        self.set_processing_code()
        self.IsoMessage.FieldData(7, get_seconds_since_epoch())
        self.IsoMessage.FieldData(11, get_stan())
        self.IsoMessage.FieldData(41, self.term.get_terminal_id())
        self.IsoMessage.FieldData(42, self.term.get_merchant_id())
        self.IsoMessage.FieldData(49, self.term.get_currency_code())

        if self.type in ['purchase', 'balance', 'cash'] and self.icc_trxn:
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
        if self.card:
            card_description = self.card.get_description()
        else:
            card_description = 'Cardless'

        if card_description:
            card_description += ' | '

        return card_description + self.description if self.description else card_description + self.type + ' ' + str(self.IsoMessage.FieldData(11))


    def set_PIN(self, PIN):
        """
        """
        if PIN:
            self.PIN = PIN
            encrypted_pinblock = self.term.get_encrypted_pin(PIN, self.card.get_card_number())
            if encrypted_pinblock:
                self.IsoMessage.FieldData(52, encrypted_pinblock)
                self.rebuild()


    def get_PIN(self):
        """
        """
        return self.PIN


    def set_STAN(self, STAN):
        """
        """
        if STAN and int(STAN) < 1000000 and int(STAN) > 0:
           self.IsoMessage.FieldData(11, int(STAN)) 
           self.rebuild()
        else:
            raise ValueError('Invalid STAN')


    def get_timeout(self):
        """
        """
        return self.timeout


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
            return True if int(actual_response_code) == 0 else False

        elif self.expected_response_action in ['DECLINED', 'DECLINE']:
            return True if int(actual_response_code) != 0 else False
            
        else:
            # no response action available, compare the response codes:
            if self.expected_response_code:
                return True if self.expected_response_code == actual_response_code else False
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


    def _set_icc_trxn(self, icc_trxn):
        """
        """
        try:
            if icc_trxn == None and self.card.get_service_code()[0] in ['2', '6']:
                self.icc_trxn = True
            elif icc_trxn == None and self.card.get_service_code()[0] not in ['2', '6']:
                self.icc_trxn = False
            elif icc_trxn.lower() == 'true':
                self.icc_trxn = True
            else:
                self.icc_trxn = False
        except AttributeError:
            # self.card is None for cardless transactions
            pass


    def set_currency(self, currency_id):
        """
        Set transaction currency code from given currency id, e.g. set 840 from 'USD'
        """
        try:
            self.currency = currency_codes[currency_id]
            self.IsoMessage.FieldData(49, self.currency)
            self.rebuild()
        except KeyError:
            self.currency = None


    def get_currency(self):
        """
        Currency getter
        """
        return self.currency


    def set_field48_tags(self, tag, tag_value):
        """
        """
        self.field48[tag] = tag_value
        self.build_field48()


    def build_field48(self):
        """
        """
        field48_data = ''
        for tag in self.field48:
            field48_data += tag + str(len(self.field48[tag])).zfill(3) + self.field48[tag]

        self.IsoMessage.FieldData(48, field48_data)
        self.rebuild()


    def set_field54(self, field_data):
        """
        """
        self.IsoMessage.FieldData(54, field_data)
        self.rebuild()


    def set_processing_code(self):
        """
        """
        if self.type in ['purchase', 'dcc check']:
            trxn_type_code = '00'
        elif self.type in ['cash']:
            trxn_type_code = '12'
        elif self.type in ['virtual purchase']:
            trxn_type_code = '15'
        elif self.type in ['refund']:
            trxn_type_code = '20'
        elif self.type in ['balance']:
            trxn_type_code = '31'
        elif self.type in ['pin change', 'pin change reversal']:
            trxn_type_code = '76'
        elif self.type in ['create virtual card']:
            trxn_type_code = '87'
        elif self.type in ['logon', 'echo', 'key change']:
            trxn_type_code = '99'
        else:
            trxn_type_code = None

        if trxn_type_code:
            self.processing_code = int(trxn_type_code + self.account_from + self.account_to )
        else:
            self.processing_code = None

        self.IsoMessage.FieldData(3, self.processing_code)
        self.rebuild()


    def set_account_from(self, account_type):
        """
        """
        self.account_from = account_type
        self.set_processing_code()


    def set_account_to(self, account_type):
        """
        """
        self.account_to = account_type
        self.set_processing_code()
        