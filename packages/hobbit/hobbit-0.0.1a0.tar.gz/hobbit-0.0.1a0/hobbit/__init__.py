"""Module contains classes to scraping."""
from time import sleep
from re import match
from concurrent import futures
import urllib.request
import logging

from bs4 import BeautifulSoup

from .robber import Robber
from .actions import Action
from .path import Path, Step
from . import rucksack as default_rucksack


__version__ = '0.0.1a0'


"""
                                            Hobbit.
==================================================================================================
"""


class Hobbit:
    """Class performs scraping."""
    path = Path()

    def __init__(self, rucksack=None):
        """
        Initial.
        Input:
            start_page_url -> Url of start page to scraping;
            path -> Path of scraping;
            ruksack -> Rucksack of Hobbit; (Scraping settings);
        """
        self.rucksack = rucksack or default_rucksack
        self.robber = Robber(rucksack)

    """
                                            Run adventure.
    ==============================================================================================
    """
    def run(self):
        current_steps = self.path.start_steps
        while current_steps:
            current_step = current_steps.pop()
            result, path = current_step(self)
            if path and result:
                next_steps = path.next_steps_for(current_step)
                for next_step in next_steps:
                    current_steps.append(next_step.reinitialize(path, result))
