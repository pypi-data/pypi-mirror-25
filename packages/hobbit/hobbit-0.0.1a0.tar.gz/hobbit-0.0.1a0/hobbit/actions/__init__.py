"""
Module contains classes descripbing actions of scraping.
For parsing used BeautifulSoup.
BeautifulSoup documetnation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import MutableMapping
from functools import reduce
from operator import xor

from bs4 import BeautifulSoup


"""
                                        Base Action classes.
==================================================================================================
"""


class Action:
    """
    The base class for scrapping actions.
    """
    def __init__(self, *args, **kwargs):
        """
        Input:
            filter_function -> Function to filtering result of action;
                               Input:
                                    url, bs_tag;

            HTML block description
            ----------------------
            Use arguments and named arguments to find_all() method from BeautifulSoup.
            args -> Argumnets for find_all(), like as html block name - 'a', 'div' and etc;
            kwargs -> Named arguments for find_all(), like as "attrs={'class': 'some_css_class'}";
        """
        self.args = args
        self.kwargs = kwargs

    """
    ____________________________________________hash__________________________________________
    """

    def __hash__(self):
        kwargs_hash = self._get_kwargs_hash(self.kwargs)
        args_hash = reduce(xor, map(hash, self.args)) if self.args else hash('')
        return kwargs_hash ^ args_hash

    def _get_kwargs_hash(self, kwargs):
        kwargs_hash = hash('')
        for key, value in kwargs.items():
            kwargs_hash ^= self._get_kwargs_hash(value) if isinstance(value, MutableMapping)\
                                                   else hash(key) ^ hash(value)
        return kwargs_hash

    @staticmethod
    def _hash_or_empty(value):
        return hash(value) if value else hash('')


class ThreadAction(Action):
    """
    The base class for the actions of working with multiple threads.
    Thread used to load pages with Frodo.
    """
    def __init__(self, *args, **kwargs):
        """
        Init is similar to the Action init. Added max_workers variable to limit threads count.
        """
        super().__init__(*args, **kwargs)
        self.max_workers = 20

    def get_pages(self, robber, urls):
        """
        Get BeautifulSoup Tag of pages from urls.
        Input:
            frodo -> Frodo object for load page_text;
            urls -> List of urls;
        Output:
            yeild url, tag_of_page -> url of page, BeautifulSoup Tag of page;
        """
        check_page_repeat = CheckPageRepeat()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_set = {executor.submit(robber.get_region, url): url for url in urls}
            for future in as_completed(future_set):
                page_text = future.result()
                page_tag = BeautifulSoup(page_text, 'html.parser')
                if not check_page_repeat(page_text)\
                   and self.filter_function(future_set[future], page_tag):
                    yield (future_set[future], page_tag)
                elif check_page_repeat.check_break:
                    break


class CheckPageRepeat:
    """
    Class to check of page repeat.
    """
    def __init__(self, max_page_repeat=3):
        """
        Initial.
        Input:
            max_page_repeat -> Maximum repeat of page.
                               If repeat is maximum then check_break is True;
        """
        self.__last_page_text = None
        self.__repeat_page = 0
        self.__check_break = False
        self.max_page_repeat = max_page_repeat

    @property
    def check_break(self):
        """
        Break if repeat.
        """
        return self.__check_break

    def __call__(self, page_text):
        """
        Check repeat page.
        Input:
            page_text -> Text of html page;
        Output:
            True, if repeat, False if not;
        """
        repeat = False
        if page_text == self.__last_page_text:
            self.__repeat_page += 1
            repeat = True
        else:
            self.__repeat_page = 0
            self.__last_page_text = page_text
        if self.__repeat_page > self.__repeat_page:
            self.__check_break = True
        return repeat
