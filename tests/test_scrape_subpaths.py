from spider.scrape import scrape_subpaths

def test_when_to_visit_set_is_empty():
    """ Test the first iteration of the scraper
        All the subpaths found should be added to the to_visit set
        Except base_url
    """
    
    found_paths = scrape_subpaths("https://github.com/louisabricot", 1)

    assert "abc" == "oij"
    
