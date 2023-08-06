class Robber:
    def __init__(self, rucksack):
        self.browser = self._get_browser(rucksack)
        self.max_concurrent_steps = rucksack.MAX_CONCURRENT_STEPS
        self.wait_time = rucksack.WAIT_TIME
        self.render_wait_time = rucksack.RENDER_WAIT_TIME
        self.current_concurrent_steps = 0

    @staticmethod
    def _get_browser(rucksack):
        if 'BROWSER' in rucksack.__dict__.keys() or not rucksack.BROWSER:
            browser = BrowserSubstitute
        else:
            browser = rucksack.BROWSER
        return browser

    """
                                            Get region.
    ==============================================================================================
    Region is a text of html page.
    """
    def get_region(self, url):
        """
        Get page of text from url.
        Input:
            url -> Url address of page;
        Output:
            page_text -> Source text of html page;
        """
        self._grab_region()
        browser = self.browser()
        browser.get(url)
        begin_page_text = browser.page_source
        self._release_region()
        if self.render_wait_time and begin_page_text == browser.page_source:
            sleep(self.render_wait_time)
        page_text = browser.page_source
        browser.close()
        return page_text

    def _grab_region(self):
        """
        Wait one's turn.
        Increase counter self.current_concurrent_steps with grab.
        """
        while self.current_concurrent_steps >= self.max_concurrent_steps:
            sleep(self.wait_time)
        self.current_concurrent_steps += 1

    def _release_region(self):
        """
        Release region.
        """
        self.current_concurrent_steps -= 1


class BrowserSubstitute:
    def __init__(self):
        self.page_source = ""

    def get(self, url):
        with urllib.request.urlopen(url) as request:
            return request.read()

    def close(self):
        pass
