"""
This module contains classes implementing the actions to scraping.
Classes describing the actions:
    - gpages; #A class describes the action to get pages from url from html elements.
    - gpagins; #A class describes the action to get pagination pages.
    - gblocks; #A class describes the action to get html from html page.
    - gresults; #A class describes the action to get results from ftml pages.
"""
from . import Action, ThreadAction


"""
                                    Actions with load of pages.
==================================================================================================
"""


class gpages(ThreadAction):
    """
    A class describes the action to get pages from url from html elements.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization action.
        """
        super().__init__(*args, **kwargs)

    def __call__(self, hobbit, path, parent):
        """
        Run action.
        Input:
            frodo -> Object of Frodo trgerring action;
            parent -> parent_url, parent_tag(BeautifulSoup Tag);
        Output:
            yeild url, tag_of_page -> url of page, BeautifulSoup Tag of page;
        """
        _, parent_tag = parent
        target_tags = parent_tag.find_all(*self.args, **self.kwargs) if self.args else [parent_tag]
        urls = self._get_urls(frodo.resource, target_tags)
        yield from self.get_pages(hobbit._robber, urls)

    @staticmethod
    def _get_urls(resource, target_tags):
        """
        Get urls from target_tags(BeautifulSoup Tags).
        Input:
            resource -> Url of resource;
            target_tags -> List of BeautifulSoup Tags;
        """
        return ['{resource}{href}'.format(resource=resource, href=tag['href'])
                for target_tag in target_tags for tag in target_tag.find_all('a')]


class gpagins(ThreadAction):
    """
    Class decribing action of getting pagination pages.
    """
    def __init__(self, pagin_template, filter_function=None,
                 start_page_number=None, finish_page_number=None):
        """
        Initialization action.
        Initialization pagination fields.
        Input:
            super...
            pagin_template -> Template of pagination, like as "?page=";
            start_page_number -> Number of start page;
            finish_page_number -> Number of finish page;
        """
        super().__init__(filter_function=filter_function)
        self.pagin_template = pagin_template
        self.start_page_number = start_page_number if start_page_number else 1
        self.finish_page_number = finish_page_number if finish_page_number else 1000000

    def __call__(self, hobbit, path, parent):
        """
        Run action.
        Input:
            frodo -> Object of Frodo trgerring action;
            parent -> parent_url, parent_tag(BeautifulSoup Tag);
        Output:
            yeild url, tag_of_page -> url of page, BeautifulSoup Tag of page;
        """
        parent_url, _ = parent
        urls = self._get_urls(parent_url)
        yield from self.get_pages(hobbit.robber, urls)

    def _get_urls(self, parent_url):
        """
        Get pagination urls.
        Input:
            parent_url -> Url to pagination;
        """
        return ['{parent_url}/{pagin_template}{page_number}'.format(
                        parent_url=parent_url,
                        pagin_template=self.pagin_template,
                        page_number=page_number)
                for page_number in range(self.start_page_number, self.finish_page_number + 1)]

    def __hash__(self):
        start_page_hash = self._hash_or_empty(self.start_page_number)
        finish_page_hash = self._hash_or_empty(self.finish_page_number)
        filter_function_hash = self._filter_function_hash()
        return start_page_hash ^ finish_page_hash ^ filter_function_hash ^ hash(self.pagin_template)


"""
                                    Actions with finding html blocks.
==================================================================================================
"""


class gblocks(Action):
    """
    Class for find BeautifulSoup Tag in parent BeautifulSoup Tag.
    Class is the interface to BeautifulSoup "find_all".
    """
    def __init__(self, *args, **kwargs):
        """
        Initial of super initial of Action.
        """
        super().__init__(*args, **kwargs)

    def __call__(self, frodo, path, parent):
        """
        Run action.
        Input:
            frodo -> Object of Frodo trgerring action;
            parent -> parent_url, parent_tag(BeautifulSoup Tag);
        Output:
            yeild url, tag_of_page -> Url of page, BeautifulSoup Tag of page;
        """
        parent_url, parent_tag = parent
        for tag in parent_tag.find_all(*self.args, **self.kwargs):
            if self.filter_functions(tag):
                yield (parent_url, tag)


"""
                                        Get results.
==================================================================================================
"""


class gresults:
    """
    Class to get result from parent BeautifulSoup Tag.
    """
    def __init__(self, result_map=None):
        """
        Inital.
        Input:
            result_function -> Function to procces results;
                Input:
                    result_set -> dictionary with results;
            result_map -> Dictionary with result fields(Keys) and result action;
        """
        self.result_map = result_map

    def __call__(self, frodo, path, parent):
        """
        Run action.
        Input:
            parent -> Tuple of url, parent BeautifulSoup Tag;
        """
        url, _ = parent
        result_set = {}
        for result_name, result_action in self.result_map.items():
            result_set.update(result_action(parent, result_name))
        result_set['url'] = url
        frodo.pick_up(result_set)
        yield

    def __hash__(self):
        return hash('results')


class path_selection:
    def __init__(self, condition, true_path, false_path):
        pass

class combine:
    pass
