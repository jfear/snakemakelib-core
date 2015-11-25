# Copyright (C) 2015 by Per Unneberg
# pylint: disable=R0904
from os.path import join
import pytest
from ..io import string_format, IOTarget, IOSampleTarget, MissingRequiredKeyException


class TestIOTarget:
    """Test IOTarget class"""
    filepattern = "{key1}_{key2,[0-9]+}"
    f = IOTarget(filepattern)
    f2 = IOTarget(filepattern, suffix=".suffix")
    fn = "foo_123.suffix"
    fn_short = "foo_123"

    def test_wrong_format(self):
        with pytest.raises(Exception):
            self.f.format(**{'key1':'foo', 'key2':'bar'})


    def test_ok_format(self):
        s = self.f.format(**{'key1':'foo', 'key2':234})
        assert s == "foo_234"


    def test_group_dict(self):
        assert self.f.keys() == {'key1', 'key2'}


    def test_target_w_suffix(self):
        self.f2.match(self.fn)
        assert self.f2.groupdict == {'key1': 'foo', 'key2': '123'}
        self.f2.search(self.fn_short)
        assert self.f2.groupdict == {'key1': 'foo', 'key2': '123'}
        s = self.f2.format(**{'key1':'foo', 'key2':123})
        assert s == "foo_123.suffix"

        

class TestIOSampleTarget:
    """Test IOSampleTarget class"""
    f = IOSampleTarget(join("{SM, [a-zA-Z0-9]+}", "{SM}.{suffix}"))
    fn = "foo/foo.txt"


    def test_sample_wrong_key(self):
        with pytest.raises(MissingRequiredKeyException):
            IOSampleTarget("{Sample}").regex
        
    
    def test_sample_format(self):
        s = self.f.format(**{'SM': 'foo', 'suffix': 'txt'})
        assert s == "foo/foo.txt"


    def test_sample_parse(self):
        self.f.match(self.fn)
        assert self.f.groupdict == {'suffix': 'txt', 'SM': 'foo'}

