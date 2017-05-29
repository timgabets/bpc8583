import binascii
import struct
from enum import Enum
from pytlv.TLV import TLV
from tracetools.tracetools import get_timestamp

# Length Type enumeration
class LT(Enum):
    FIXED   = 0
    LVAR    = 1
    LLVAR   = 2
    LLLVAR  = 3

# Data Type enumeration
class DT(Enum):
    BCD     = 1
    ASCII   = 2
    BIN     = 3

class SpecError(Exception):
        def __init__(self, value):
                self.str = value
        def __str__(self):
                return repr(self.str)

def MemDump(Title, data):
    i = 1

    if isinstance(data, bytes) == False:
        raise TypeError('Expected bytes for data')

    print(Title)
    TheDump = ''
    
    for c in data:
        try: # python 3
            TheDump += '{:02x} '.format(c) 
        except: # python 2.x
            TheDump += '{:02x} '.format(ord(c))
        
        if i % 16 == 0:
            TheDump += '\n'
        i+=1
       
    print(TheDump)


def Bcd2Str(bcd):
    return binascii.hexlify(bcd).decode('latin')


def Str2Bcd(string):
    if len(string) % 2 == 1:
        string = string.zfill(len(string) + 1)
    return binascii.unhexlify(string)


def Bcd2Int(bcd):
    return int(Bcd2Str(bcd))


def Int2Bcd(integer):
    string = str(integer)
    if len(string) % 2 == 1:
        string = string.zfill(len(string) + 1)
    return binascii.unhexlify(string)


class ParseError(Exception):
        def __init__(self, value):
                self.str = value
        def __str__(self):
                return repr(self.str)
class SpecError(Exception):
        def __init__(self, value):
                self.str = value
        def __str__(self):
                return repr(self.str)
class BuildError(Exception):
        def __init__(self, value):
                self.str = value
        def __str__(self):
                return repr(self.str)
            
            
class ISO8583:
    
    ValidContentTypes = ('a', 'n', 's', 'an', 'as', 'ns', 'ans', 'b', 'z')
    
    def __init__(self, IsoMsg = None, IsoSpec = None):
        
        self.strict = False
    
        self.__Bitmap = {}
        self.__FieldData = {}
        self.__iso = b''
        self.tlv = TLV()
        
        self.__IsoSpec = IsoSpec if IsoSpec != None else spec.IsoSpec1987ASCII()
        
        if IsoMsg:
            if isinstance(IsoMsg, bytes) == False:
                raise TypeError('Expected bytes for iso message')
            
            self.__iso = IsoMsg
            self.ParseIso()


    def Strict(self, Value):
        if Value != True and Value != False:
            raise ValueError
        self.strict = Value

        
    def SetIsoContent(self, IsoMsg):
        if isinstance(IsoMsg, bytes) == False:
            raise TypeError('Expected bytes for iso message')
        self.__iso = IsoMsg
        self.ParseIso()
    
    
    
    def ParseMTI(self, p):
        DataType = self.__IsoSpec.DataType('MTI')
        
        if DataType == DT.BCD:
            self.__MTI = Bcd2Str(self.__iso[p:p+2])
            p+=2
        elif DataType == DT.ASCII:
            self.__MTI = self.__iso[p:p+4].decode('latin')
            p+=4
        
        try: # MTI should only contain numbers
            int(self.__MTI)
        except:
            raise ParseError('Invalid MTI: [{0}]'.format(self.__MTI))
            
        if self.strict == True:
            if self.__MTI[1] == '0':
                raise ParseError('Invalid MTI: Invalid Message type [{0}]'.format(self.__MTI))
                  
            if int(self.__MTI[3]) > 5:
                raise ParseError('Invalid MTI: Invalid Message origin [{0}]'.format(self.__MTI))
        
        return p
    
    
    def ParseBitmap(self, p):
        DataType = self.__IsoSpec.DataType(1)

        if DataType == DT.BIN:
            Primary = self.__iso[p:p+8]
            p += 8
        elif DataType == DT.ASCII:
            Primary = binascii.unhexlify(self.__iso[p:p+16])
            p += 16
                
        IntPrimary = struct.unpack_from('!Q', Primary)[0]
        
        for i in range(1, 65):
            self.__Bitmap[i] = (IntPrimary >> (64 - i)) & 0x1

        if self.__Bitmap[1] == 1:
            if DataType == DT.BIN:
                Secondary = self.__iso[p:p+8]
                p += 8
            elif DataType == DT.ASCII:
                Secondary = binascii.unhexlify(self.__iso[p:p+16])
                p += 16
                
            IntSecondary = struct.unpack_from('!Q', Secondary)[0]
            
            for i in range(1, 65):
                self.__Bitmap[i+64] = (IntSecondary >> (64 - i)) & 0x1
            
        return p
            
            
    def ParseField(self, field, p):
        
        try:
            DataType = self.__IsoSpec.DataType(field)
            LenType = self.__IsoSpec.LengthType(field)
            ContentType = self.__IsoSpec.ContentType(field)
            MaxLength = self.__IsoSpec.MaxLength(field)
        except:
            raise SpecError('Cannot parse F{0}: Incomplete field specification'.format(field))

        try:
            if DataType == DT.ASCII and ContentType == 'b':
                MaxLength *= 2
                
            if LenType == LT.FIXED:
                Len = MaxLength
            elif LenType == LT.LVAR:
                pass
            elif LenType == LT.LLVAR:
                LenDataType = self.__IsoSpec.LengthDataType(field)
                if LenDataType == DT.ASCII:
                    Len = int(self.__iso[p:p+2])
                    p+=2
                elif LenDataType == DT.BCD:
                    Len = Bcd2Int(self.__iso[p:p+1])
                    p+=1
            elif LenType == LT.LLLVAR:
                LenDataType = self.__IsoSpec.LengthDataType(field)
                if LenDataType == DT.ASCII:
                    Len = int(self.__iso[p:p+3])
                    p+=3
                elif LenDataType == DT.BCD:
                    Len = Bcd2Int(self.__iso[p:p+2])
                    p+=2
        except ValueError:
            raise ParseError('Cannot parse F{0}: Invalid length'.format(field))
            
        if Len > MaxLength:
            raise ParseError('F{0} is larger than maximum length ({1}>{2})'.format(field, Len, MaxLength))
        
        # In case of zero length, don't try to parse the field itself, just continue
        if Len == 0:
            return p

        try:
            if DataType == DT.ASCII:
                if ContentType == 'n':
                    self.__FieldData[field] = int(self.__iso[p:p+(Len)]) 
                else:
                    self.__FieldData[field] = self.__iso[p:p+(Len)].decode('latin')
                p += Len
            elif DataType == DT.BCD:
                if Len % 2 == 1:
                    Len += 1
                if ContentType == 'n':
                    self.__FieldData[field] = Bcd2Int(self.__iso[p:p+(Len//2)])
                elif ContentType == 'z':
                    self.__FieldData[field] = binascii.hexlify(self.__iso[p:p+(Len//2)]).decode('latin').upper()
                p += Len//2
            elif DataType == DT.BIN:
                self.__FieldData[field] = binascii.hexlify(self.__iso[p:p+(Len)]).decode('latin').upper()
                p += Len
        except:
            raise ParseError('Cannot parse F{0}'.format(field))
        
        if ContentType == 'z':
            self.__FieldData[field] = self.__FieldData[field].replace('D', '=') # in track2, replace d with =  
            self.__FieldData[field] = self.__FieldData[field].replace('F', '') # in track2, remove trailing f
 
        return p
    
    
    def ParseIso(self):
        p = 0
        p = self.ParseMTI(p)
        p = self.ParseBitmap(p)


        for field in sorted(self.__Bitmap):
            # field 1 is parsed by the bitmap function
            if field != 1 and self.Field(field) == 1:
                p = self.ParseField(field, p)
    

    def BuildMTI(self):
        if self.__IsoSpec.DataType('MTI') == DT.BCD:
            self.__iso += Str2Bcd(self.__MTI)
        elif self.__IsoSpec.DataType('MTI') == DT.ASCII:
            self.__iso += self.__MTI.encode('latin')
    
    
    def BuildBitmap(self):
        DataType = self.__IsoSpec.DataType(1)
        
        # check if we need a secondary bitmap
        for i in self.__Bitmap.keys():
            if i > 64:
                self.__Bitmap[1] = 1
                break
        
        IntPrimary = 0
        for i in range(1, 65):
            if i in self.__Bitmap.keys():
                IntPrimary |= (self.__Bitmap[i] & 0x1) << (64 - i)

        Primary = struct.pack('!Q', IntPrimary)

        if DataType == DT.BIN:
            self.__iso += Primary
        elif DataType == DT.ASCII:
            self.__iso += binascii.hexlify(Primary)
            
        # Add secondary bitmap if applicable
        if 1 in self.__Bitmap.keys() and self.__Bitmap[1] == 1:
        
            IntSecondary = 0
            for i in range(65, 129):
                if i in self.__Bitmap.keys():
                    IntSecondary |= (self.__Bitmap[i] & 0x1) << (128 - i)
                
            Secondary = struct.pack('!Q', IntSecondary)

            if DataType == DT.BIN:
                self.__iso += Secondary
            elif DataType == DT.ASCII:
                self.__iso += binascii.hexlify(Secondary)
            
            
    def BuildField(self, field):
        try:
            DataType = self.__IsoSpec.DataType(field)
            LenType = self.__IsoSpec.LengthType(field)
            ContentType = self.__IsoSpec.ContentType(field)
            MaxLength = self.__IsoSpec.MaxLength(field)
        except:
            raise SpecError('Cannot parse F{0}: Incomplete field specification'.format(field))
 

        data = ''
        if LenType == LT.FIXED:
            Len = MaxLength
            
            if ContentType == 'n':
                formatter = '{{0:0{0}d}}'.format(Len)
            elif 'a' in ContentType or 'n' in ContentType or 's' in ContentType:
                formatter = '{{0: >{0}}}'.format(Len)
            else:
                formatter = '{0}'
                
            data = formatter.format(self.__FieldData[field])
                
        else:
            LenDataType = self.__IsoSpec.LengthDataType(field)
            
            try:
                data = '{0}'.format(self.__FieldData[field])
            except KeyError:
                data = ''
            Len = len(data)
            if DataType == DT.BIN:
                Len //=2
                
            if Len > MaxLength:
                raise BuildError('Cannot Build F{0}: Field Length larger than specification'.format(field))
            
            if LenType == LT.LVAR:
                LenData = '{0:01d}'.format(Len)
                
            elif LenType == LT.LLVAR:
                LenData = '{0:02d}'.format(Len)
                
            elif LenType == LT.LLLVAR:
                LenData = '{0:03d}'.format(Len)
                
            if LenDataType == DT.ASCII:
                self.__iso += LenData.encode('latin')
            elif LenDataType == DT.BCD:
                self.__iso += Str2Bcd(LenData)
            elif LenDataType == DT.BIN:
                self.__iso += binascii.unhexlify(LenData)
            
            
        if ContentType == 'z':
            data = data.replace('=', 'D')
            #if(len(data) % 2 == 1):
            #    data = data + 'F'
        
        if DataType == DT.ASCII:
            self.__iso += data.encode('latin')
        elif DataType == DT.BCD:
            self.__iso += Str2Bcd(data)
        elif DataType == DT.BIN:
            self.__iso += binascii.unhexlify(self.__FieldData[field])


    def BuildIso(self):
        self.__iso = b''
        self.BuildMTI()
        self.BuildBitmap()
        
        for field in sorted(self.__Bitmap):
            if field != 1 and self.Field(field) == 1:
                self.BuildField(field)
                
        return self.__iso
    
    
    def RemoveField(self, field):
        '''
        '''
        try:
            self.__FieldData[field] = None
            del(self.__Bitmap[field])
        except KeyError:
            pass


    def Field(self, field, Value = None):
        '''
        Add field to bitmap
        '''
        if Value == None:
            try:
                return self.__Bitmap[field]
            except KeyError:
                return None
        elif Value == 1 or Value == 0:
            self.__Bitmap[field] = Value
        else:
            raise ValueError


    def SetBitmap(self, fields):
        '''
        Set the message bitmap with the value from fields array
        '''
        for field in fields:
            self.Field(field, Value=1)
            

    def FieldData(self, field, Value = None):
        '''
        Add field data
        '''
        if Value == None:
            try:
                return self.__FieldData[field]
            except KeyError:
                return None
        else:
            if len(str(Value)) > self.__IsoSpec.MaxLength(field):
                raise ValueError('Value length larger than field maximum ({0})'.format(self.__IsoSpec.MaxLength(field)))
            
            self.Field(field, Value=1)
            self.__FieldData[field] = Value 
            
            
    def Bitmap(self):
        return self.__Bitmap

    def MTI(self, MTI = None):
        if MTI == None:
            return self.__MTI
        else:
            try: # MTI should only contain numbers
                int(MTI)
            except:
                raise ValueError('Invalid MTI [{0}]: MTI must contain only numbers'.format(MTI))
        
            if self.strict == True:
                if MTI[1] == '0':
                    raise ValueError('Invalid MTI [{0}]: Invalid Message type'.format(MTI))
                      
                if int(MTI[3]) > 5:
                    raise ValueError('Invalid MTI [{0}]: Invalid Message origin'.format(MTI))
            
            self.__MTI = MTI


    def get_MTI(self):
        '''
        '''
        return self.__MTI


    def Description(self, field):
        return self.__IsoSpec.Description(field)
    
    def DataType(self, field, DataType = None):
        return self.__IsoSpec.DataType(field, DataType)
    
    def ContentType(self, field, ContentType = None):
        return self.__IsoSpec.ContentType(field, ContentType)


    def PrintMessage(self):
        self.Print()


    def Print(self, header=None):
        if header:
            print('\t{} at {}:'.format(header, get_timestamp()))
        else:
            print('\tParsed message:')

        try:
            print('\tMTI:    [{0}]'.format(self.__MTI))
        except AttributeError:
            pass
        
        bitmapLine = '\tFields: [ '
        for i in sorted(self.__Bitmap.keys()):
            if i == 1: 
                continue
            if self.__Bitmap[i] == 1:
                bitmapLine += str(i) + ' '
        bitmapLine += ']'
        print(bitmapLine)
        

        for i in sorted(self.__Bitmap.keys()):
            if i == 1:
                continue
            if self.__Bitmap[i] == 1:
                try:
                    FieldData = self.__FieldData[i]
                except KeyError:
                    FieldData = ''
                
                if self.ContentType(i) == 'n' and self.__IsoSpec.LengthType(i) == LT.FIXED:
                    FieldData = str(FieldData).zfill(self.__IsoSpec.MaxLength(i))
                if i == 39:
                    print('\t\t{0:>3d} - {1: <41} [{2}]\t\t\t[{3}]'.format(i, self.__IsoSpec.Description(i), FieldData, self.__IsoSpec.RespCodeDescription(FieldData)))
                elif i == 55:
                    print('\t\t{0:>3d} - {1: <41} [{2}]'.format(i, self.__IsoSpec.Description(i), FieldData))
                    print(self.tlv.dump(self.tlv.parse(FieldData), left_indent='\t\t', desc_column_width=38))
                else:
                    print('\t\t{0:>3d} - {1: <41} [{2}]'.format(i, self.__IsoSpec.Description(i), FieldData))

        print('\n')

currency_codes = {
'AFA': 4,
'ALL': 8,
'DZD': 12,
'ADP': 20,
'AOK': 24,
'ARA': 32,
'AUD': 36,
'ATS': 40,
'BSD': 44,
'BHD': 48,
'BDT': 50,
'AMD': 51,
'BBD': 52,
'BEF': 56,
'BMD': 60,
'BTN': 64,
'BOB': 68,
'BWP': 72,
'BRC': 76,
'BZD': 84,
'SBD': 90,
'BND': 96,
'BGL': 100,
'MMK': 104,
'BIF': 108,
'KHR': 116,
'CAD': 124,
'CVE': 132,
'KYD': 136,
'LKR': 144,
'CLP': 152,
'CNY': 156,
'COP': 170,
'KMF': 174,
'ZRZ': 180,
'CRC': 188,
'HRK': 191,
'CUP': 192,
'CYP': 196,
'CSK': 200,
'CZK': 203,
'DKK': 208,
'DOP': 214,
'ECS': 218,
'SVC': 222,
'GQE': 226,
'ETB': 230,
'EEK': 233,
'FKP': 238,
'FJD': 242,
'FIM': 246,
'FRF': 250,
'DJF': 262,
'GMD': 270,
'DDM': 278,
'DEM': 280,
'GHC': 288,
'GIP': 292,
'GRD': 300,
'GTQ': 320,
'GNF': 324,
'GYD': 328,
'HTG': 332,
'HNL': 340,
'HKD': 344,
'HUF': 348,
'ISK': 352,
'INR': 356,
'IDR': 360,
'IRR': 364,
'IRA': 365,
'IQD': 368,
'IEP': 372,
'ILS': 376,
'ITL': 380,
'JMD': 388,
'JPY': 392,
'KZT': 398,
'JOD': 400,
'KES': 404,
'KPW': 408,
'KRW': 410,
'KWD': 414,
'KGS': 417,
'LAK': 418,
'LBP': 422,
'LSL': 426,
'LVL': 428,
'LRD': 430,
'LYD': 434,
'LTL': 440,
'LUF': 442,
'MOP': 446,
'MGF': 450,
'MWK': 454,
'MYR': 458,
'MVR': 462,
'MLF': 466,
'MTL': 470,
'MRO': 478,
'MUR': 480,
'MXN': 484,
'MNT': 496,
'MDL': 498,
'MAD': 504,
'MZM': 508,
'OMR': 512,
'NAD': 516,
'NPR': 524,
'NLG': 528,
'ANG': 532,
'AWG': 533,
'VUV': 548,
'NZD': 554,
'NIO': 558,
'NGN': 566,
'NOK': 578,
'PKR': 586,
'PAB': 590,
'PGK': 598,
'PYG': 600,
'PEI': 604,
'PHP': 608,
'PLN': 616,
'PTE': 620,
'GWP': 624,
'TPE': 626,
'QAR': 634,
'ROL': 642,
'RUB': 643,
'RWF': 646,
'SHP': 654,
'STD': 678,
'SAR': 682,
'SCR': 690,
'SLL': 694,
'SGD': 702,
'SKK': 703,
'VND': 704,
'SIT': 705,
'SOS': 706,
'ZAR': 710,
'ZWD': 716,
'YDD': 720,
'ESP': 724,
'SSP': 728,
'SDD': 736,
'SDA': 737,
'SRG': 740,
'SZL': 748,
'SEK': 752,
'CHF': 756,
'SYP': 760,
'THB': 764,
'TOP': 776,
'TLP': 777,
'TTD': 780,
'AED': 784,
'TND': 788,
'TRL': 792,
'UGX': 800,
'UAK': 804,
'MKD': 807,
'SUR': 810,
'EGP': 818,
'GBP': 826,
'TZS': 834,
'USD': 840,
'UYP': 858,
'UZS': 860,
'VEB': 862,
'WST': 882,
'YER': 886,
'YUD': 890,
'ZMK': 894,
'TWD': 901,
'BYN': 933,
'TMT': 934,
'SDG': 938,
'AZN': 944,
'TRY': 949,
'XAF': 950,
'XCD': 951,
'XOF': 952,
'XPF': 953,
'ZMW': 967,
'SRD': 968,
'MGA': 969,
'TJS': 972,
'BYR': 974,
'BAM': 977,
'EUR': 978,
'GEL': 981,
'BRL': 986,
'BEL': 992,
'BEC': 993,
'XXX': 999}