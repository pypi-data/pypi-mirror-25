"""Models of this library."""

import os
import csv
from lxml import html
import requests

class AppEntry(object):
    """Class for a single app information requester."""

    _page = None
    _tree = None
    def __init__(self, package):
        self.package = package
        self._url = "https://play.google.com/store/apps/details?id={}&hl=en".format(package)

    def _get_page_and_tree(self):
        """Return app's page from google play."""
        if self._page is None:
            self._page = requests.get(self._url)
            self._tree = html.fromstring(self._page.content)
        return self._page, self._tree

    def get_rating(self):
        "Get rating value and count of ratings."
        _, tree = self._get_page_and_tree()
        rating = tree.xpath('//div[@itemprop="aggregateRating"]')[0]
        value = rating.xpath('//meta[@itemprop="ratingValue"]')[0].attrib["content"]
        count = rating.xpath('//meta[@itemprop="ratingCount"]')[0].attrib["content"]
        return float(value), int(count)

    def get_downloads(self):
        "Get range number of downloads."
        _, tree = self._get_page_and_tree()
        downloads = tree.xpath('//div[@itemprop="numDownloads"]')[0].text
        return downloads.strip()

    def get_category(self):
        "Get category of the app."
        _, tree = self._get_page_and_tree()
        downloads = tree.xpath('//span[@itemprop="genre"]')[0].text
        return downloads.strip()

    def get_name(self):
        "Get name of the app."
        _, tree = self._get_page_and_tree()
        name = tree.xpath('//div[@class="id-app-title"]')[0].text
        return name.strip()

class AppDatabase():
    """Class to maintain a CSV database with several apps' information."""

    _CSV_HEADER = [
        "package",
        "rating_value",
        "rating_count",
        "downloads"
    ]
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        if not os.path.isfile(self.csv_filename):
            with open(self.csv_filename, 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=self._CSV_HEADER)
                csv_writer.writeheader()

    def already_processed(self, package):
        """Check whether an app was already collected."""
        with open(self.csv_filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return package in (row['package'] for row in csv_reader)
        return False

    def process(self, package):
        """Collect and save information about a single app."""
        if self.already_processed(package):
            print("Skipping {}: already processed.".format(package))
            return
        try:
            app = AppEntry(package)
            rating_value, rating_count = app.get_rating()
            downloads = app.get_downloads()
        except IndexError:
            print("Warning: could not find {} on Google Play".format(package))
            rating_value = rating_count = downloads = None
        with open(self.csv_filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self._CSV_HEADER)
            csv_writer.writerow({
                "package": package,
                "rating_value": rating_value,
                "rating_count": rating_count,
                "downloads": downloads,
            })


    def bulk_process(self, packages):
        """Process list of packages."""
        for package in packages:
            print("Collecting info for {}.".format(package))
            self.process(package)




if __name__ == "__main__":
    #pylint: disable=invalid-name
    app_entry = AppEntry("com.newsblur")
    print(app_entry.get_name())
    collector = AppDatabase("test.csv")
    print(collector.already_processed("com.showmehills"))
    collector.bulk_process(["com.newsblur", "eu.siacs.conversations", "com.showmehills"])
