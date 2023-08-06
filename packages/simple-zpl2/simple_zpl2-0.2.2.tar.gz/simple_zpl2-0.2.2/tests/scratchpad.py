import pytest
from simple_zpl2 import ZPLDocument

for justification in (None, ):
    with pytest.raises(Exception):
        zdoc = ZPLDocument()
        zdoc.add_field_origin(10, 10, justification)
