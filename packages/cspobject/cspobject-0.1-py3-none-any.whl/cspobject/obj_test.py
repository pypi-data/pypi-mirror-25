from . import CSPObject


def test_equality():
    a = CSPObject(default_src=('https:',))
    b = CSPObject(default_src=('https:',))
    assert a == b


def test_union():
    a = CSPObject(default_src=('http:',))
    b = CSPObject(default_src=('https:',))
    assert a & b == CSPObject(default_src=('http:', 'https:'))


def test_union_fallback():
    a = CSPObject(default_src=('http:',))
    b = CSPObject(script_src=('https:',))
    assert a & b == CSPObject(default_src=('http:',),
                              script_src=('http:', 'https:'))


def test_union_no_fallback_when_both_specified():
    a = CSPObject(default_src=('http:',), script_src=('https:',))
    b = CSPObject(script_src=('https:',))
    assert a & b == CSPObject(default_src=('http:',),
                              script_src=('https:',))
