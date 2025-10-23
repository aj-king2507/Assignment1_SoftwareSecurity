from detector import is_suspicious

def test_detector_flags_or_tautology():
    sql = "SELECT * FROM users WHERE username = 'admin' OR 1=1 --"
    matches = is_suspicious(sql)
    assert isinstance(matches, list)
    assert len(matches) >= 1

def test_detector_no_false_positive_simple_query():
    sql = "SELECT * FROM users WHERE username = 'normaluser'"
    matches = is_suspicious(sql)
    assert matches == [] or len(matches) == 0
