from .ISO8583 import ISO8583, DT, LT, SpecError
     
class IsoSpec(object):
    __ValidContentTypes = ('a', 'n', 's', 'an', 'as', 'ns', 'ans', 'b', 'z')
    
    Descriptions = {}
    ContentTypes = {}
    DataTypes = {}
    
    def __init__(self):
        self.SetContentTypes()
        self.SetDataTypes()
    
    def SetContentTypes(self):
        pass
    def SetDataTypes(self):
        pass
         
    def Description(self, field):
        try:
            return self.ContentTypes[field]['Description']
        except KeyError:
            return ''


    def DataType(self, field, DataType = None):
        if DataType == None:
            return self.DataTypes[field]['Data']
        else:
            if DataType not in DT:
                raise SpecError("Cannot set data type '{0}' for F{1}: Invalid data type".format(DataType, field))
            if field not in self.DataTypes.keys():
                self.DataTypes[field] = {}
            self.DataTypes[field]['Data'] = DataType

    
    def ContentType(self, field, ContentType = None):
        if ContentType == None:
            return self.ContentTypes[field]['ContentType']
        else:
            if ContentType not in self.__ValidContentTypes:
                raise SpecError("Cannot set Content type '{0}' for F{1}: Invalid content type".format(ContentType, field))
            self.ContentTypes[field]['ContentType'] = ContentType

            
    def MaxLength(self, field, MaxLength = None):
        if MaxLength:
            self.ContentTypes[field]['MaxLen'] = MaxLength
        else:
            return self.ContentTypes[field]['MaxLen']
    

    def LengthType(self, field, LengthType = None):
        if LengthType == None:
            return self.ContentTypes[field]['LenType']
        else:
            if LengthType not in self.__ValidContentTypes:
                raise SpecError("Cannot set Length type '{0}' for F{1}: Invalid length type".format(LengthType, field))
            self.ContentTypes[field]['LenType'] = LengthType

    
    def LengthDataType(self, field, LengthDataType = None):
        if LengthDataType == None:
            return self.DataTypes[field]['Length']
        else:
            if LengthDataType not in DT:
                raise SpecError("Cannot set data type '{0}' for F{1}: Invalid data type".format(LengthDataType, field))
            if field not in self.DataTypes.keys():
                self.DataTypes[field] = {}
            self.DataTypes[field]['Length'] = LengthDataType
    
    
    
class IsoSpec1987(IsoSpec):
    def SetContentTypes(self):
        self.ContentTypes = ContentTypes['1987']

        
class IsoSpec1987ASCII(IsoSpec1987):
    def SetDataTypes(self):
        self.DataType('MTI', DT.ASCII)
        self.DataType(1, DT.ASCII) # bitmap
        
        for field in self.ContentTypes.keys():
            self.DataType(field, DT.ASCII)
            if self.LengthType(field) != LT.FIXED:
                self.LengthDataType(field, DT.ASCII)


class IsoSpec1987BPC(IsoSpec1987):
    '''
    A BPC's flavour of ISO8583 

    MTI is ASCII
    Bitmap is BCD
    DataFields are also ASCII
    '''
    RespCodeDescriptions = {
        '00': 'APPROVED',
        '000': 'APPROVED',
        '001': 'HONR W/ID:',
        '005': 'UNABLE TO PROCESS',
        '020': 'BALANCE IS NEGATIVE',
        '100': 'CARD DECLINED',
        '101': 'EXPIRED CARD',
        '103': 'CALL ISSUER',
        '104': 'CAPTURE CARD SPEC',
        '106': 'PIN-TRIES EXCEED',
        '107': 'CALL ISSUER',
        '109': 'INVALID TERMINAL OR MERCHANT',
        '110': 'INVALID AMOUNT',
        '111': 'INVALID CARD',
        '116': 'INSUFFICIENT FUNDS',
        '117': 'INCORRECT PIN',
        '119': 'SECURITY VIOLATION',
        '120': 'SECURITY VIOLATION',
        '121': 'EXCDS WDRWL LIMT',
        '123': 'EXCDS WDRWL LIMT',
        '125': 'INVALID CARD',
        '202': 'INVALID CARD',
        '203': 'PICK-UP CARD',
        '204': 'PICK-UP CARD',
        '208': 'PICK-UP CARD',
        '209': 'PICK-UP CARD',
        '902': 'INVALID TRANS',
        '903': 'RE-ENTER TRANS',
        '904': 'FORMAT ERROR',
        '907': 'HOST NOT AVAIL.',
        '909': 'INVALID TRANS',
        '910': 'HOST NOT AVAIL.',
        '913': 'INVALID TRANS',
        '914': 'ORIG TRANS NOT FOUND',
        '920': 'PIN ERROR',
        '940': 'CAPTURE CARD SPEC',
    }

    def SetDataTypes(self):
        '''
        '''
        self.DataType('MTI', DT.ASCII)
        for field in self.ContentTypes.keys():
            self.DataType(field, DT.ASCII)
            if self.LengthType(field) != LT.FIXED:
                self.LengthDataType(field, DT.ASCII)

        self.DataType(1, DT.BIN) # bitmap
        self.DataType(52, DT.BIN) # pin block
        self.DataType(53, DT.BIN) # security related control information
        self.DataType(55, DT.BIN) # ICC data


    def RespCodeDescription(self, response_code):
        '''
        '''
        try:
            return self.RespCodeDescriptions[response_code ]
        except KeyError:
            return ''


class IsoSpec1987CUP(IsoSpec1987):
    '''
    A CUP's flavour of ISO8583 

    MTI is ASCII
    Bitmap is BCD
    DataFields are also ASCII
    '''
    RespCodeDescriptions = {
        '00': 'APPROVED',
        '000': 'APPROVED',
        '001': 'HONR W/ID:',
        '005': 'UNABLE TO PROCESS',
        '020': 'BALANCE IS NEGATIVE',
        '100': 'CARD DECLINED',
        '101': 'EXPIRED CARD',
        '103': 'CALL ISSUER',
        '104': 'CAPTURE CARD SPEC',
        '106': 'PIN-TRIES EXCEED',
        '107': 'CALL ISSUER',
        '109': 'INVALID TERMINAL OR MERCHANT',
        '110': 'INVALID AMOUNT',
        '111': 'INVALID CARD',
        '116': 'INSUFFICIENT FUNDS',
        '117': 'INCORRECT PIN',
        '119': 'SECURITY VIOLATION',
        '120': 'SECURITY VIOLATION',
        '121': 'EXCDS WDRWL LIMT',
        '123': 'EXCDS WDRWL LIMT',
        '125': 'INVALID CARD',
        '202': 'INVALID CARD',
        '203': 'PICK-UP CARD',
        '204': 'PICK-UP CARD',
        '208': 'PICK-UP CARD',
        '209': 'PICK-UP CARD',
        '902': 'INVALID TRANS',
        '903': 'RE-ENTER TRANS',
        '904': 'FORMAT ERROR',
        '907': 'HOST NOT AVAIL.',
        '909': 'INVALID TRANS',
        '910': 'HOST NOT AVAIL.',
        '913': 'INVALID TRANS',
        '914': 'ORIG TRANS NOT FOUND',
        '920': 'PIN ERROR',
        '940': 'CAPTURE CARD SPEC',
    }
    def SetDataTypes(self):
        '''
        '''
        self.ContentTypes = ContentTypes['CUP']
        self.DataType('MTI', DT.ASCII)
        for field in self.ContentTypes.keys():
            self.DataType(field, DT.ASCII)
            if self.LengthType(field) != LT.FIXED:
                self.LengthDataType(field, DT.ASCII)

        self.DataType(1, DT.BIN) # bitmap
        self.DataType(52, DT.BIN) # pin block
        #self.DataType(53, DT.BIN) # security related control information
        self.DataType(55, DT.BIN) # ICC data


    def RespCodeDescription(self, response_code):
        '''
        '''
        try:
            return self.RespCodeDescriptions[response_code ]
        except KeyError:
            return 'UNKNOWN RESPONSE'


class IsoSpec1987BCD(IsoSpec1987):
    def SetDataTypes(self):
        self.DataType('MTI', DT.BCD)
        self.DataType(1, DT.BIN) # bitmap
        
        # Most popular BCD implementations use the reserved/private fields
        # as binary, so we have to set them as such in contrast to the ISO spec
        for field in self.ContentTypes.keys():
            if self.MaxLength(field) == 999:
                self.ContentType(field, 'b')
        
        
        for field in self.ContentTypes.keys():
            
            ContentType = self.ContentType(field)
            
            if 'a' in ContentType or 's' in ContentType:
                self.DataType(field, DT.ASCII)
            elif ContentType == 'b':
                self.DataType(field, DT.BIN)
            else:
                self.DataType(field, DT.BCD)

            if self.LengthType(field) != LT.FIXED:
                self.LengthDataType(field, DT.BCD)


class IsoSpecPostBridge(IsoSpec1987):
    '''
    A PostBridge's flavour of ISO8583 

    MTI is ASCII
    Bitmap is BCD
    DataFields are also ASCII
    '''
    RespCodeDescriptions = {
        '00': 'APPROVED',
        '000': 'APPROVED',
        '001': 'HONR W/ID:',
        '005': 'UNABLE TO PROCESS',
        '020': 'BALANCE IS NEGATIVE',
        '100': 'CARD DECLINED',
        '101': 'EXPIRED CARD',
        '103': 'CALL ISSUER',
        '104': 'CAPTURE CARD SPEC',
        '106': 'PIN-TRIES EXCEED',
        '107': 'CALL ISSUER',
        '109': 'INVALID TERMINAL OR MERCHANT',
        '110': 'INVALID AMOUNT',
        '111': 'INVALID CARD',
        '116': 'INSUFFICIENT FUNDS',
        '117': 'INCORRECT PIN',
        '119': 'SECURITY VIOLATION',
        '120': 'SECURITY VIOLATION',
        '121': 'EXCDS WDRWL LIMT',
        '123': 'EXCDS WDRWL LIMT',
        '125': 'INVALID CARD',
        '202': 'INVALID CARD',
        '203': 'PICK-UP CARD',
        '204': 'PICK-UP CARD',
        '208': 'PICK-UP CARD',
        '209': 'PICK-UP CARD',
        '902': 'INVALID TRANS',
        '903': 'RE-ENTER TRANS',
        '904': 'FORMAT ERROR',
        '907': 'HOST NOT AVAIL.',
        '909': 'INVALID TRANS',
        '910': 'HOST NOT AVAIL.',
        '913': 'INVALID TRANS',
        '914': 'ORIG TRANS NOT FOUND',
        '920': 'PIN ERROR',
        '940': 'CAPTURE CARD SPEC',
    }

    def SetContentTypes(self):
        self.ContentTypes = ContentTypes['PostBridge']

    def SetDataTypes(self):
        '''
        '''
        self.DataType('MTI', DT.ASCII)
        for field in self.ContentTypes.keys():
            self.DataType(field, DT.ASCII)
            if self.LengthType(field) != LT.FIXED:
                self.LengthDataType(field, DT.ASCII)

        self.DataType(1, DT.BIN) # bitmap
        self.DataType(52, DT.BIN) # pin block
        self.DataType(53, DT.BIN) # security related control information
        self.DataType(55, DT.BIN) # ICC data


    def RespCodeDescription(self, response_code):
        '''
        '''
        try:
            return self.RespCodeDescriptions[response_code ]
        except KeyError:
            return ''


class IsoSpecPostBridge2(IsoSpec1987):
    '''
    A PostBridge's flavour of ISO8583 

    MTI is ASCII
    Bitmap is BCD
    DataFields are also ASCII
    '''
    RespCodeDescriptions = {
        '00': 'APPROVED',
        '000': 'APPROVED',
        '001': 'HONR W/ID:',
        '005': 'UNABLE TO PROCESS',
        '020': 'BALANCE IS NEGATIVE',
        '100': 'CARD DECLINED',
        '101': 'EXPIRED CARD',
        '103': 'CALL ISSUER',
        '104': 'CAPTURE CARD SPEC',
        '106': 'PIN-TRIES EXCEED',
        '107': 'CALL ISSUER',
        '109': 'INVALID TERMINAL OR MERCHANT',
        '110': 'INVALID AMOUNT',
        '111': 'INVALID CARD',
        '116': 'INSUFFICIENT FUNDS',
        '117': 'INCORRECT PIN',
        '119': 'SECURITY VIOLATION',
        '120': 'SECURITY VIOLATION',
        '121': 'EXCDS WDRWL LIMT',
        '123': 'EXCDS WDRWL LIMT',
        '125': 'INVALID CARD',
        '202': 'INVALID CARD',
        '203': 'PICK-UP CARD',
        '204': 'PICK-UP CARD',
        '208': 'PICK-UP CARD',
        '209': 'PICK-UP CARD',
        '902': 'INVALID TRANS',
        '903': 'RE-ENTER TRANS',
        '904': 'FORMAT ERROR',
        '907': 'HOST NOT AVAIL.',
        '909': 'INVALID TRANS',
        '910': 'HOST NOT AVAIL.',
        '913': 'INVALID TRANS',
        '914': 'ORIG TRANS NOT FOUND',
        '920': 'PIN ERROR',
        '940': 'CAPTURE CARD SPEC',
    }

    def SetContentTypes(self):
        self.ContentTypes = ContentTypes['PostBridge2']

    def SetDataTypes(self):
        '''
        '''
        self.DataType('MTI', DT.ASCII)
        for field in self.ContentTypes.keys():
            self.DataType(field, DT.ASCII)
            if self.LengthType(field) != LT.FIXED:
                self.LengthDataType(field, DT.ASCII)

        self.DataType(1, DT.BIN) # bitmap
        self.DataType(52, DT.BIN) # pin block
        self.DataType(53, DT.BIN) # security related control information
        self.DataType(55, DT.BIN) # ICC data


    def RespCodeDescription(self, response_code):
        '''
        '''
        try:
            return self.RespCodeDescriptions[response_code ]
        except KeyError:
            return ''
    
ContentTypes = {}

'''
Notes to the BPC's flavour of ISO8583:
 * DE 12 has length of 12, not 6
 * DE 39 has length of 3, not 2
'''
ContentTypes['1987'] = {
    1 :   { 'ContentType':'b',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Bitmap' },
    2 :   { 'ContentType':'n',     'MaxLen': 19,  'LenType': LT.LLVAR,   'Description': 'Primary account number (PAN)' },
    3 :   { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Processing code' },
    4 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, transaction' },
    5 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, settlement' },
    6 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing' },
    7 :   { 'ContentType':'n',     'MaxLen': 10,  'LenType': LT.FIXED,   'Description': 'Transmission date & time (MMDDhhmmss)' },
    8 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing fee' },
    9 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, settlement' },
    10 :  { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, cardholder billing' },
    11 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'System trace audit number' },
    12 :  { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Time, local transaction (YYMMDDhhmmss)' },
    13 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, local transaction (MMDD)' },
    14 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, expiration' },
    15 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Date, settlement' },
    16 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, conversion' },
    17 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, capture' },
    18 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Merchant type' },
    19 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Acquiring institution country code' },
    20 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'PAN extended, country code' },
    21 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Forwarding institution. country code' },
    22 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Point of service entry mode' },
    23 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Application PAN sequence number' },
    24 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Network International identifier (NII)' },
    25 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service condition code' },
    26 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service capture code' },
    27 :  { 'ContentType':'n',     'MaxLen': 1,   'LenType': LT.FIXED,   'Description': 'Authorizing identification response length' },
    28 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction fee' },
    29 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement fee' },
    30 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction processing fee' },
    31 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement processing fee' },
    32 :  { 'ContentType':'n',     'MaxLen': 11,  'LenType': LT.LLVAR,   'Description': 'Acquiring institution identification code' },
    33 :  { 'ContentType':'n',     'MaxLen': 11,  'LenType': LT.LLVAR,   'Description': 'Forwarding institution identification code' },
    34 :  { 'ContentType':'ns',    'MaxLen': 28,  'LenType': LT.LLVAR,   'Description': 'Primary account number, extended' },
    35 :  { 'ContentType':'z',     'MaxLen': 37,  'LenType': LT.LLVAR,   'Description': 'Track 2 data' },
    36 :  { 'ContentType':'n',     'MaxLen': 104, 'LenType': LT.LLLVAR,  'Description': 'Track 3 data' },
    37 :  { 'ContentType':'an',    'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Retrieval reference number' },
    38 :  { 'ContentType':'an',    'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Authorization identification response' },
    39 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Response code' },
    40 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Service restriction code' },
    41 :  { 'ContentType':'ans',   'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Terminal ID' },
    42 :  { 'ContentType':'ans',   'MaxLen': 15,  'LenType': LT.FIXED,   'Description': 'Merchant number' },
    43 :  { 'ContentType':'ans',   'MaxLen': 40,  'LenType': LT.FIXED,   'Description': 'Card acceptor name/location' },
    44 :  { 'ContentType':'an',    'MaxLen': 25,  'LenType': LT.LLVAR,   'Description': 'Additional response data' },
    45 :  { 'ContentType':'an',    'MaxLen': 76,  'LenType': LT.LLVAR,   'Description': 'Track 1 data' },
    46 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Amount, fees' },
    47 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data' },
    48 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data - private' },
    49 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, transaction' },
    50 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, settlement' },
    51 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, cardholder billing' },
    52 :  { 'ContentType':'b',     'MaxLen': 16,   'LenType': LT.FIXED,  'Description': 'PIN data' },
    53 :  { 'ContentType':'n',     'MaxLen': 18,  'LenType': LT.FIXED,   'Description': 'Security related control information' },
    54 :  { 'ContentType':'an',    'MaxLen': 120, 'LenType': LT.LLLVAR,  'Description': 'Additional amounts' },
    55 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'ICC Sys Related Data' },
    56 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved ISO' },
    57 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    58 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    59 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    60 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    61 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    62 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    63 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    64 :  { 'ContentType':'b',     'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code (MAC)' },
    65 :  { 'ContentType' : 'b',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Bitmap, extended' },
    66 :  { 'ContentType' : 'n',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Settlement code' },
    67 :  { 'ContentType' : 'n',   'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'Extended payment code' },
    68 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Receiving institution country code' },
    69 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Settlement institution country code' },
    70 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Network management information code' },
    71 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number' },
    72 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number, last' },
    73 :  { 'ContentType' : 'n',   'MaxLen' : 6,  'LenType': LT.FIXED,   'Description': 'Date, action (YYMMDD)' },
    74 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, number' },
    75 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, reversal number' },
    76 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, number' },
    77 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, reversal number' },
    78 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer number' },
    79 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer, reversal number' },
    80 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Inquiries number' },
    81 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Authorizations, number' },
    82 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, processing fee amount' },
    83 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, transaction fee amount' },
    84 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, processing fee amount' },
    85 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, transaction fee amount' },
    86 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, amount' },
    87 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, reversal amount' },
    88 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, amount' },
    89 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, reversal amount' },
    90 :  { 'ContentType' : 'n',   'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Original data elements' },
    91 :  { 'ContentType' : 'an',  'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'File update code' },
    92 :  { 'ContentType' : 'an',  'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'File security code' },
    93 :  { 'ContentType' : 'an',  'MaxLen' : 5,  'LenType': LT.FIXED,   'Description': 'Response indicator' },
    94 :  { 'ContentType' : 'an',  'MaxLen' : 7,  'LenType': LT.FIXED,   'Description': 'Service indicator' },
    95 :  { 'ContentType' : 'an',  'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Replacement amounts' },
    96 :  { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message security code' },
    97 :  { 'ContentType' : 'an',  'MaxLen' : 17, 'LenType': LT.FIXED,   'Description': 'Amount, net settlement' },
    98 :  { 'ContentType' : 'ans', 'MaxLen' : 25, 'LenType': LT.FIXED,   'Description': 'Payee' },
    99 :  { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Settlement institution identification code' },
    100 : { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Receiving institution identification code' },
    101 : { 'ContentType' : 'ans', 'MaxLen' : 17, 'LenType': LT.LLVAR,   'Description': 'File name' },
    102 : { 'ContentType' : 'ans', 'MaxLen' : 28, 'LenType': LT.LLVAR,   'Description': 'Account identification 1' },
    103 : { 'ContentType' : 'ans', 'MaxLen' : 28, 'LenType': LT.LLVAR,   'Description': 'Account identification 2' },
    104 : { 'ContentType' : 'ans', 'MaxLen' : 100, 'LenType': LT.LLLVAR, 'Description': 'Transaction description' },
    105 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    106 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    107 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    108 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    109 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    110 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    111 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    112 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    113 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    114 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    115 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    116 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    117 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    118 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    119 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    120 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    121 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    122 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    123 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    124 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    125 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    126 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    127 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    128 : { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code' }
}

ContentTypes['CUP'] = {
    1 :   { 'ContentType':'b',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Bitmap' },
    2 :   { 'ContentType':'n',     'MaxLen': 19,  'LenType': LT.LLVAR,   'Description': 'Primary account number (PAN)' },
    3 :   { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Processing code' },
    4 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, transaction' },
    5 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, settlement' },
    6 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing' },
    7 :   { 'ContentType':'n',     'MaxLen': 10,  'LenType': LT.FIXED,   'Description': 'Transmission date & time (MMDDhhmmss)' },
    8 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing fee' },
    9 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, settlement' },
    10 :  { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, cardholder billing' },
    11 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'System trace audit number' },
    12 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Time, local transaction (YYMMDDhhmmss)' },
    13 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, local transaction (MMDD)' },
    14 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, expiration' },
    15 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Date, settlement' },
    16 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, conversion' },
    17 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, capture' },
    18 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Merchant type' },
    19 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Acquiring institution country code' },
    20 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'PAN extended, country code' },
    21 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Forwarding institution. country code' },
    22 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Point of service entry mode' },
    23 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Application PAN sequence number' },
    24 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Network International identifier (NII)' },
    25 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service condition code' },
    26 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service capture code' },
    27 :  { 'ContentType':'n',     'MaxLen': 1,   'LenType': LT.FIXED,   'Description': 'Authorizing identification response length' },
    28 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction fee' },
    29 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement fee' },
    30 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction processing fee' },
    31 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement processing fee' },
    32 :  { 'ContentType':'n',     'MaxLen': 11,  'LenType': LT.LLVAR,   'Description': 'Acquiring institution identification code' },
    33 :  { 'ContentType':'n',     'MaxLen': 11,  'LenType': LT.LLVAR,   'Description': 'Forwarding institution identification code' },
    34 :  { 'ContentType':'ns',    'MaxLen': 28,  'LenType': LT.LLVAR,   'Description': 'Primary account number, extended' },
    35 :  { 'ContentType':'z',     'MaxLen': 37,  'LenType': LT.LLVAR,   'Description': 'Track 2 data' },
    36 :  { 'ContentType':'n',     'MaxLen': 104, 'LenType': LT.LLLVAR,  'Description': 'Track 3 data' },
    37 :  { 'ContentType':'an',    'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Retrieval reference number' },
    38 :  { 'ContentType':'an',    'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Authorization identification response' },
    39 :  { 'ContentType':'an',    'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Response code' },
    40 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Service restriction code' },
    41 :  { 'ContentType':'ans',   'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Terminal ID' },
    42 :  { 'ContentType':'ans',   'MaxLen': 15,  'LenType': LT.FIXED,   'Description': 'Merchant number' },
    43 :  { 'ContentType':'ans',   'MaxLen': 40,  'LenType': LT.FIXED,   'Description': 'Card acceptor name/location' },
    44 :  { 'ContentType':'an',    'MaxLen': 25,  'LenType': LT.LLVAR,   'Description': 'Additional response data' },
    45 :  { 'ContentType':'an',    'MaxLen': 76,  'LenType': LT.LLVAR,   'Description': 'Track 1 data' },
    46 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Amount, fees' },
    47 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data' },
    48 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data - private' },
    49 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, transaction' },
    50 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, settlement' },
    51 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, cardholder billing' },
    52 :  { 'ContentType':'b',     'MaxLen': 16,  'LenType': LT.FIXED,   'Description': 'PIN data' },
    53 :  { 'ContentType':'an',    'MaxLen': 16,  'LenType': LT.FIXED,   'Description': 'Security related control information' },
    54 :  { 'ContentType':'an',    'MaxLen': 120, 'LenType': LT.LLLVAR,  'Description': 'Additional amounts' },
    55 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'ICC Sys Related Data' },
    56 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved ISO' },
    57 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    58 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    59 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    60 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    61 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    62 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    63 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    64 :  { 'ContentType':'b',     'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code (MAC)' },
    65 :  { 'ContentType' : 'b',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Bitmap, extended' },
    66 :  { 'ContentType' : 'n',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Settlement code' },
    67 :  { 'ContentType' : 'n',   'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'Extended payment code' },
    68 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Receiving institution country code' },
    69 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Settlement institution country code' },
    70 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Network management information code' },
    71 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number' },
    72 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number, last' },
    73 :  { 'ContentType' : 'n',   'MaxLen' : 6,  'LenType': LT.FIXED,   'Description': 'Date, action (YYMMDD)' },
    74 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, number' },
    75 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, reversal number' },
    76 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, number' },
    77 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, reversal number' },
    78 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer number' },
    79 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer, reversal number' },
    80 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Inquiries number' },
    81 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Authorizations, number' },
    82 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, processing fee amount' },
    83 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, transaction fee amount' },
    84 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, processing fee amount' },
    85 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, transaction fee amount' },
    86 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, amount' },
    87 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, reversal amount' },
    88 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, amount' },
    89 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, reversal amount' },
    90 :  { 'ContentType' : 'n',   'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Original data elements' },
    91 :  { 'ContentType' : 'an',  'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'File update code' },
    92 :  { 'ContentType' : 'an',  'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'File security code' },
    93 :  { 'ContentType' : 'an',  'MaxLen' : 5,  'LenType': LT.FIXED,   'Description': 'Response indicator' },
    94 :  { 'ContentType' : 'an',  'MaxLen' : 7,  'LenType': LT.FIXED,   'Description': 'Service indicator' },
    95 :  { 'ContentType' : 'an',  'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Replacement amounts' },
    96 :  { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message security code' },
    97 :  { 'ContentType' : 'an',  'MaxLen' : 17, 'LenType': LT.FIXED,   'Description': 'Amount, net settlement' },
    98 :  { 'ContentType' : 'ans', 'MaxLen' : 25, 'LenType': LT.FIXED,   'Description': 'Payee' },
    99 :  { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Settlement institution identification code' },
    100 : { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Receiving institution identification code' },
    101 : { 'ContentType' : 'ans', 'MaxLen' : 17, 'LenType': LT.LLVAR,   'Description': 'File name' },
    102 : { 'ContentType' : 'ans', 'MaxLen' : 28, 'LenType': LT.LLVAR,   'Description': 'Account identification 1' },
    103 : { 'ContentType' : 'ans', 'MaxLen' : 28, 'LenType': LT.LLVAR,   'Description': 'Account identification 2' },
    104 : { 'ContentType' : 'ans', 'MaxLen' : 100, 'LenType': LT.LLLVAR, 'Description': 'Transaction description' },
    105 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    106 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    107 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    108 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    109 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    110 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    111 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    112 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    113 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    114 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    115 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    116 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    117 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    118 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    119 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    120 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    121 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    122 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    123 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    124 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    125 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    126 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    127 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    128 : { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code' }
}

ContentTypes['PostBridge'] = {
    1 :   { 'ContentType':'b',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Bitmap' },
    2 :   { 'ContentType':'n',     'MaxLen': 19,  'LenType': LT.LLVAR,   'Description': 'Primary account number (PAN)' },
    3 :   { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Processing code' },
    4 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, transaction' },
    5 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, settlement' },
    6 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing' },
    7 :   { 'ContentType':'n',     'MaxLen': 10,  'LenType': LT.FIXED,   'Description': 'Transmission date & time (MMDDhhmmss)' },
    8 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing fee' },
    9 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, settlement' },
    10 :  { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, cardholder billing' },
    11 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'System trace audit number' },
    12 :  { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Time, local transaction (YYMMDDhhmmss)' },
    13 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, local transaction (MMDD)' },
    14 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, expiration' },
    15 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, settlement' },
    16 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, conversion' },
    17 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, capture' },
    18 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Merchant type' },
    19 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Acquiring institution country code' },
    20 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'PAN extended, country code' },
    21 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Forwarding institution. country code' },
    22 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Point of service entry mode' },
    23 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Application PAN sequence number' },
    24 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Network International identifier (NII)' },
    25 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service condition code' },
    26 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service capture code' },
    27 :  { 'ContentType':'n',     'MaxLen': 1,   'LenType': LT.FIXED,   'Description': 'Authorizing identification response length' },
    28 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction fee' },
    29 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement fee' },
    30 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction processing fee' },
    31 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement processing fee' },
    32 :  { 'ContentType':'n',     'MaxLen': 11,  'LenType': LT.LLVAR,   'Description': 'Acquiring institution identification code' },
    33 :  { 'ContentType':'n',     'MaxLen': 11,  'LenType': LT.LLVAR,   'Description': 'Forwarding institution identification code' },
    34 :  { 'ContentType':'ns',    'MaxLen': 28,  'LenType': LT.LLVAR,   'Description': 'Primary account number, extended' },
    35 :  { 'ContentType':'z',     'MaxLen': 37,  'LenType': LT.LLVAR,   'Description': 'Track 2 data' },
    36 :  { 'ContentType':'n',     'MaxLen': 104, 'LenType': LT.LLLVAR,  'Description': 'Track 3 data' },
    37 :  { 'ContentType':'an',    'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Retrieval reference number' },
    38 :  { 'ContentType':'an',    'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Authorization identification response' },
    39 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Response code' },
    40 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Service restriction code' },
    41 :  { 'ContentType':'ans',   'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Terminal ID' },
    42 :  { 'ContentType':'ans',   'MaxLen': 15,  'LenType': LT.FIXED,   'Description': 'Merchant number' },
    43 :  { 'ContentType':'ans',   'MaxLen': 40,  'LenType': LT.FIXED,   'Description': 'Card acceptor name/location' },
    44 :  { 'ContentType':'an',    'MaxLen': 25,  'LenType': LT.LLVAR,   'Description': 'Additional response data' },
    45 :  { 'ContentType':'an',    'MaxLen': 76,  'LenType': LT.LLVAR,   'Description': 'Track 1 data' },
    46 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Amount, fees' },
    47 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data' },
    48 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data - private' },
    49 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, transaction' },
    50 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, settlement' },
    51 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, cardholder billing' },
    52 :  { 'ContentType':'b',     'MaxLen': 16,   'LenType': LT.FIXED,  'Description': 'PIN data' },
    53 :  { 'ContentType':'n',     'MaxLen': 18,  'LenType': LT.FIXED,   'Description': 'Security related control information' },
    54 :  { 'ContentType':'an',    'MaxLen': 400, 'LenType': LT.LLLVAR,  'Description': 'Additional amounts' },
    55 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'ICC Sys Related Data' },
    56 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved ISO' },
    57 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    58 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    59 :  { 'ContentType':'an',    'MaxLen': 4,   'LenType': LT.FIXED,  'Description': 'Reserved national' },
    60 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    61 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    62 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    63 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    64 :  { 'ContentType':'b',     'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code (MAC)' },
    65 :  { 'ContentType' : 'b',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Bitmap, extended' },
    66 :  { 'ContentType' : 'n',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Settlement code' },
    67 :  { 'ContentType' : 'n',   'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'Extended payment code' },
    68 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Receiving institution country code' },
    69 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Settlement institution country code' },
    70 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Network management information code' },
    71 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number' },
    72 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number, last' },
    73 :  { 'ContentType' : 'n',   'MaxLen' : 6,  'LenType': LT.FIXED,   'Description': 'Date, action (YYMMDD)' },
    74 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, number' },
    75 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, reversal number' },
    76 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, number' },
    77 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, reversal number' },
    78 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer number' },
    79 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer, reversal number' },
    80 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Inquiries number' },
    81 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Authorizations, number' },
    82 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, processing fee amount' },
    83 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, transaction fee amount' },
    84 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, processing fee amount' },
    85 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, transaction fee amount' },
    86 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, amount' },
    87 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, reversal amount' },
    88 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, amount' },
    89 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, reversal amount' },
    90 :  { 'ContentType' : 'n',   'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Original data elements' },
    91 :  { 'ContentType' : 'an',  'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'File update code' },
    92 :  { 'ContentType' : 'an',  'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'File security code' },
    93 :  { 'ContentType' : 'an',  'MaxLen' : 5,  'LenType': LT.FIXED,   'Description': 'Response indicator' },
    94 :  { 'ContentType' : 'an',  'MaxLen' : 7,  'LenType': LT.FIXED,   'Description': 'Service indicator' },
    95 :  { 'ContentType' : 'an',  'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Replacement amounts' },
    96 :  { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message security code' },
    97 :  { 'ContentType' : 'an',  'MaxLen' : 17, 'LenType': LT.FIXED,   'Description': 'Amount, net settlement' },
    98 :  { 'ContentType' : 'ans', 'MaxLen' : 25, 'LenType': LT.FIXED,   'Description': 'Payee' },
    99 :  { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Settlement institution identification code' },
    100 : { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Receiving institution identification code' },
    101 : { 'ContentType' : 'ans', 'MaxLen' : 17, 'LenType': LT.LLVAR,   'Description': 'File name' },
    102 : { 'ContentType' : 'an',  'MaxLen' : 28, 'LenType': LT.FIXED,   'Description': 'Account identification 1' },
    103 : { 'ContentType' : 'an',  'MaxLen' : 2, 'LenType':  LT.FIXED,   'Description': 'Account identification 2' },
    104 : { 'ContentType' : 'ans', 'MaxLen' : 100, 'LenType': LT.LLLVAR, 'Description': 'Transaction description' },
    105 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    106 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    107 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    108 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    109 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    110 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    111 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    112 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    113 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    114 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    115 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    116 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    117 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    118 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    119 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    120 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    121 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    122 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    123 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'POS Data Code' },
    124 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    125 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    126 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    127 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    128 : { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code' }
}


ContentTypes['PostBridge2'] = {
    1 :   { 'ContentType':'b',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Bitmap' },
    2 :   { 'ContentType':'n',     'MaxLen': 19,  'LenType': LT.LLVAR,   'Description': 'Primary account number (PAN)' },
    3 :   { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Processing code' },
    4 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, transaction' },
    5 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, settlement' },
    6 :   { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing' },
    7 :   { 'ContentType':'n',     'MaxLen': 10,  'LenType': LT.FIXED,   'Description': 'Transmission date & time (MMDDhhmmss)' },
    8 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Amount, cardholder billing fee' },
    9 :   { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, settlement' },
    10 :  { 'ContentType':'n',     'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Conversion rate, cardholder billing' },
    11 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'System trace audit number' },
    12 :  { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Time, local transaction (YYMMDDhhmmss)' },
    13 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, local transaction (MMDD)' },
    14 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, expiration' },
    15 :  { 'ContentType':'n',     'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Date, settlement' },
    16 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, conversion' },
    17 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Date, capture' },
    18 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Merchant type' },
    19 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Acquiring institution country code' },
    20 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'PAN extended, country code' },
    21 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Forwarding institution. country code' },
    22 :  { 'ContentType':'n',     'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Point of service entry mode' },
    23 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Application PAN sequence number' },
    24 :  { 'ContentType':'n',     'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Network International identifier (NII)' },
    25 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Point of service condition code' },
    26 :  { 'ContentType':'n',     'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Point of service capture code' },
    27 :  { 'ContentType':'n',     'MaxLen': 1,   'LenType': LT.FIXED,   'Description': 'Authorizing identification response length' },
    28 :  { 'ContentType':'an',    'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Amount, transaction fee' },
    29 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement fee' },
    30 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, transaction processing fee' },
    31 :  { 'ContentType':'an',    'MaxLen': 9,   'LenType': LT.FIXED,   'Description': 'Amount, settlement processing fee' },
    32 :  { 'ContentType':'an',    'MaxLen': 2,   'LenType': LT.FIXED,   'Description': 'Acquiring institution identification code' },
    33 :  { 'ContentType':'n',     'MaxLen': 2,   'LenType': LT.LLVAR,   'Description': 'Forwarding institution identification code' },
    34 :  { 'ContentType':'ns',    'MaxLen': 28,  'LenType': LT.LLVAR,   'Description': 'Primary account number, extended' },
    35 :  { 'ContentType':'z',     'MaxLen': 37,  'LenType': LT.LLVAR,   'Description': 'Track 2 data' },
    36 :  { 'ContentType':'n',     'MaxLen': 104, 'LenType': LT.LLLVAR,  'Description': 'Track 3 data' },
    37 :  { 'ContentType':'an',    'MaxLen': 12,  'LenType': LT.FIXED,   'Description': 'Retrieval reference number' },
    38 :  { 'ContentType':'an',    'MaxLen': 6,   'LenType': LT.FIXED,   'Description': 'Authorization identification response' },
    39 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Response code' },
    40 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Service restriction code' },
    41 :  { 'ContentType':'ans',   'MaxLen': 8,   'LenType': LT.FIXED,   'Description': 'Terminal ID' },
    42 :  { 'ContentType':'ans',   'MaxLen': 15,  'LenType': LT.FIXED,   'Description': 'Merchant number' },
    43 :  { 'ContentType':'ans',   'MaxLen': 40,  'LenType': LT.FIXED,   'Description': 'Card acceptor name/location' },
    44 :  { 'ContentType':'an',    'MaxLen': 25,  'LenType': LT.LLVAR,   'Description': 'Additional response data' },
    45 :  { 'ContentType':'an',    'MaxLen': 76,  'LenType': LT.LLVAR,   'Description': 'Track 1 data' },
    46 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Amount, fees' },
    47 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data' },
    48 :  { 'ContentType':'an',    'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Additional data - private' },
    49 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, transaction' },
    50 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, settlement' },
    51 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Currency code, cardholder billing' },
    52 :  { 'ContentType':'b',     'MaxLen': 16,   'LenType': LT.FIXED,  'Description': 'PIN data' },
    53 :  { 'ContentType':'n',     'MaxLen': 18,  'LenType': LT.FIXED,   'Description': 'Security related control information' },
    54 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Additional amounts' },
    55 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'ICC Sys Related Data' },
    56 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved ISO' },
    57 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    58 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved national' },
    59 :  { 'ContentType':'an',    'MaxLen': 4,   'LenType': LT.FIXED,   'Description': 'Reserved national' },
    60 :  { 'ContentType':'an',    'MaxLen': 3,   'LenType': LT.FIXED,   'Description': 'Reserved national' },
    61 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    62 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    63 :  { 'ContentType':'ans',   'MaxLen': 999, 'LenType': LT.LLLVAR,  'Description': 'Reserved private' },
    64 :  { 'ContentType':'b',     'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code (MAC)' },
    65 :  { 'ContentType' : 'b',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Bitmap, extended' },
    66 :  { 'ContentType' : 'n',   'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'Settlement code' },
    67 :  { 'ContentType' : 'n',   'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'Extended payment code' },
    68 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Receiving institution country code' },
    69 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Settlement institution country code' },
    70 :  { 'ContentType' : 'n',   'MaxLen' : 3,  'LenType': LT.FIXED,   'Description': 'Network management information code' },
    71 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number' },
    72 :  { 'ContentType' : 'n',   'MaxLen' : 4,  'LenType': LT.FIXED,   'Description': 'Message number, last' },
    73 :  { 'ContentType' : 'n',   'MaxLen' : 6,  'LenType': LT.FIXED,   'Description': 'Date, action (YYMMDD)' },
    74 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, number' },
    75 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Credits, reversal number' },
    76 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, number' },
    77 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Debits, reversal number' },
    78 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer number' },
    79 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Transfer, reversal number' },
    80 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Inquiries number' },
    81 :  { 'ContentType' : 'n',   'MaxLen' : 10, 'LenType': LT.FIXED,   'Description': 'Authorizations, number' },
    82 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, processing fee amount' },
    83 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Credits, transaction fee amount' },
    84 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, processing fee amount' },
    85 :  { 'ContentType' : 'n',   'MaxLen' : 12, 'LenType': LT.FIXED,   'Description': 'Debits, transaction fee amount' },
    86 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, amount' },
    87 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Credits, reversal amount' },
    88 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, amount' },
    89 :  { 'ContentType' : 'n',   'MaxLen' : 16, 'LenType': LT.FIXED,   'Description': 'Debits, reversal amount' },
    90 :  { 'ContentType' : 'n',   'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Original data elements' },
    91 :  { 'ContentType' : 'an',  'MaxLen' : 1,  'LenType': LT.FIXED,   'Description': 'File update code' },
    92 :  { 'ContentType' : 'an',  'MaxLen' : 2,  'LenType': LT.FIXED,   'Description': 'File security code' },
    93 :  { 'ContentType' : 'an',  'MaxLen' : 5,  'LenType': LT.FIXED,   'Description': 'Response indicator' },
    94 :  { 'ContentType' : 'an',  'MaxLen' : 7,  'LenType': LT.FIXED,   'Description': 'Service indicator' },
    95 :  { 'ContentType' : 'an',  'MaxLen' : 42, 'LenType': LT.FIXED,   'Description': 'Replacement amounts' },
    96 :  { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message security code' },
    97 :  { 'ContentType' : 'an',  'MaxLen' : 17, 'LenType': LT.FIXED,   'Description': 'Amount, net settlement' },
    98 :  { 'ContentType' : 'ans', 'MaxLen' : 25, 'LenType': LT.FIXED,   'Description': 'Payee' },
    99 :  { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Settlement institution identification code' },
    100 : { 'ContentType' : 'n',   'MaxLen' : 11, 'LenType': LT.LLVAR,   'Description': 'Receiving institution identification code' },
    101 : { 'ContentType' : 'ans', 'MaxLen' : 17, 'LenType': LT.LLVAR,   'Description': 'File name' },
    102 : { 'ContentType' : 'an',  'MaxLen' : 28, 'LenType': LT.FIXED,   'Description': 'Account identification 1' },
    103 : { 'ContentType' : 'an',  'MaxLen' : 2, 'LenType':  LT.FIXED,   'Description': 'Account identification 2' },
    104 : { 'ContentType' : 'ans', 'MaxLen' : 100, 'LenType': LT.LLLVAR, 'Description': 'Transaction description' },
    105 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    106 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    107 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    108 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    109 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    110 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    111 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for ISO use' },
    112 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    113 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    114 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    115 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    116 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    117 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    118 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    119 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for national use' },
    120 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    121 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    122 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    123 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'POS Data Code' },
    124 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    125 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    126 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    127 : { 'ContentType' : 'ans', 'MaxLen' : 999, 'LenType': LT.LLLVAR, 'Description': 'Reserved for private use' },
    128 : { 'ContentType' : 'b',   'MaxLen' : 8,  'LenType': LT.FIXED,   'Description': 'Message authentication code' }
}
