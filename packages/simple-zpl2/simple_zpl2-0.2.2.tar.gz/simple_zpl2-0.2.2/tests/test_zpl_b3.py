import pytest
from simple_zpl2 import ZPLDocument, Code39_Barcode


def test_code_39_barcode():
    assert('Code 39 Barcode Tests Created' == 'YES')



def test_code_39():
    bc = Code39_Barcode('01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ-.$/+% ',
                        'N', 'Y', 200, 'N')
    assert(str(bc) == '^B3N,Y,200,N\n^FD01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ-.$/+% ^FS\n')

    with pytest.raises(ValueError):
        bc = Code39_Barcode(chr(128) + chr(129), 'N', 'Y', extended_ascii=True)

    bc = Code39_Barcode(chr(1) + chr(127) + chr(4), 'N', extended_ascii=True)
    assert(str(bc) == '^B3N\n^FD+$$A%T$D-$^FS\n')
