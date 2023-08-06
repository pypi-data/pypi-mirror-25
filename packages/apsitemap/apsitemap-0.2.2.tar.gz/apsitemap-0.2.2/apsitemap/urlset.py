#!/usr/bin/env python3
# encoding: utf-8
from xml.dom.minidom import Document
from urllib import parse
import os

from .utility import standardize_url, sitemap_log


class UrlSet(object):

    """A set of urls.

    the container of urls that have the same domain.

    Attribute:
        entry: the entry of website.
    """

    def __init__(self, entry: str, scheme="http://", changefreq=None, lastmod=None):

        self.__entry = standardize_url(entry)
        
        entry_parse = parse.urlparse(self.__entry)
        self.__netloc = entry_parse.netloc
        self.__scheme = entry_parse.scheme if entry_parse.scheme != "" else scheme

        self.__urls = []

        self.__changefreq = changefreq
        
        self.__lastmod = lastmod

        sitemap_log.debug("Initialize urls container...")

    def can_have(self, url: str) -> bool:
        """can url join the set?"""
        return parse.urlparse(standardize_url(url)).netloc == self.__netloc

    def add(self, urls: list):
        urls = self.fix_urls(urls)
        for url in urls:
            if url not in self.__urls:
                self.__urls.append(url)
        self.__urls.sort()

    def fix_urls(self, urls: list) -> list:

        results = []
        for url in urls:
            if isinstance(url, str):
                if url.startswith("/"):
                    results.append("{}://{}{}".format(self.__scheme, self.__netloc, url))
                elif url.startswith("https://") or url.startswith("http://"):
                    if self.can_have(url):
                        results.append(url)
                elif not url.startswith("#") and not url.startswith("javascript"):
                    results.append(standardize_url(url))

        return list(map(lambda url_: parse.urldefrag(parse.unquote(url_)).url, results))
    
    def save_xml(self, file="sitemap.xml"):
        doc = Document()

        urlset = doc.createElement("urlset")
        urlset.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        urlset.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        urlset.setAttribute("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9"
                                                  " http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

        for url_item in self:
            url = doc.createElement("url")
            urlset.appendChild(url)

            # 创建loc节点
            loc = doc.createElement("loc")
            loc_text = doc.createTextNode(url_item)
            loc.appendChild(loc_text)
            url.appendChild(loc)

            # 创建changefreq节点
            if bool(self.__changefreq):
                changefreq = doc.createElement("changefreq")
                changefreq_text = doc.createTextNode(self.__changefreq)
                changefreq.appendChild(changefreq_text)
                url.appendChild(changefreq)

            # 创建lastmod节点
            if bool(self.__lastmod):
                lastmod = doc.createElement("lastmod")
                lastmod_text = doc.createTextNode(self.__lastmod)
                lastmod.appendChild(lastmod_text)
                url.appendChild(lastmod)

        doc.appendChild(urlset)

        with open(file, 'w', encoding="utf-8") as f:
            f.write(doc.toprettyxml())
        
        sitemap_log.info("Urlset was saved as xml file, %s", file)

    def save_txt(self, file="sitemap.txt"):
        with open(file, 'w', encoding="utf-8") as f:
            f.write(os.linesep.join([url for url in self.__urls]))
        
        sitemap_log.info("Urlset was saved as txt file, %s", file)

    def __contains__(self, url: str):
        return url in self.__urls

    def __iter__(self):
        yield from self.__urls

    def __getitem__(self, index):
        return self.__urls[index]

    def __len__(self):
        return len(self.__urls)


if __name__ == '__main__':
    url_lists = [
        "http://www.qiama.com:8888/article/index.html?page=2#html",
        "http://www.qiama.com:8888/article/index.html?page=2#perfect",
        "http://www.qiama.com:8888/article/index.html?page=3#perfect",
        "http://www.qiama.com:8888/你说呢",
        "/pages/2",
        "#main",
        "javascript",
        "http://baidu.com/article/我说我不知道"
    ]
    urlset = UrlSet(entry="www.qiama.com:8888")
    urlset.add(url_lists)
    urlset.save_xml()

