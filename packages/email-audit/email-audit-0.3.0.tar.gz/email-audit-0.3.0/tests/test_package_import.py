import email_audit


def test_package_metadata():
    assert email_audit.__author__
    assert email_audit.__email__
    assert email_audit.__version__
