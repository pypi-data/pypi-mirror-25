from unittest import TestCase

from statscraper.scrapers.VantetiderScraper import VantetiderScraper


class TestPXWeb(TestCase):

    def test_pxweb_scraper(self):
        """ Extending the basescraper """
        scraper = VantetiderScraper()
        self.assertTrue(len(scraper.items))
