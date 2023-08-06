import pytest
from simple_zpl2 import *

# TODO: Flush out all Code128 functionality in tests prior to coding.


def test_code128():
    bc = Code128_Barcode('123', 'N', 30, 'Y', 'Y')
    assert(str(bc) == '^BCN,30,Y,Y\n^FD123^FS\n')


def test_code128_barcode():
    assert ('Code 128 Barcode Tests Created' == 'YES')
