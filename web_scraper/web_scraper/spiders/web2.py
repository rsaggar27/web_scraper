import scrapy
from pathlib import Path


class Web1Spider(scrapy.Spider):
    name = "web2"

    def start_requests(self):
        urls = [
            "https://www.webmd.com/cholesterol-management/understanding-numbers"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,headers={"User-Agent": "Mozilla/5.0"})

    def parse(self, response):
        current_title = None
        current_sub = None
        section_data = None

        skip_titles = ["Care at Cleveland Clinic", "A note from Cleveland Clinic"]
        skip_phrases = ["Advertisement", "Policy", "Cleveland Clinic is a non-profit"]

        for elem in response.css('h1, h2,strong, li, p, img'):
            tag = elem.root.tag

            if tag == 'h1' or tag == 'h2':
                if section_data and section_data['title'] not in skip_titles:
                    yield section_data

                current_title = elem.xpath('normalize-space()').get()
                current_sub = None
                section_data = {
                    'title': current_title,
                    'sub_title': None,
                    'content': [],
                    'images': []
                }

            elif tag == 'strong':
                if section_data and section_data['title'] not in skip_titles:
                    yield section_data

                current_sub = elem.xpath('normalize-space()').get()
                section_data = {
                    'title': current_title,
                    'sub_title': current_sub,
                    'content': [],
                    'images': []
                }

            elif tag in ['p', 'li']:
                text = elem.xpath('normalize-space()').get()
                if (
                    text
                    and section_data
                    and section_data['title'] not in skip_titles
                    and not any(skip in text for skip in skip_phrases)
                ):
                    section_data['content'].append(text)

            elif tag == 'img':
                img_url = elem.attrib.get('src')
                if img_url and section_data and section_data['title'] not in skip_titles:
                    section_data['images'].append(response.urljoin(img_url))

        if section_data and section_data['title'] not in skip_titles:
            yield section_data