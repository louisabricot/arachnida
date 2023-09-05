from crawler import crawler

def test_simple_crawler():
    crawler("abc", 0, "data")
    assert "abc" == "oij"
    
