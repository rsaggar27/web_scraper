import scrapy
from pathlib import Path
from scrapy_splash import SplashRequest 


class Web1Spider(scrapy.Spider):
    name = "web3"

    def start_requests(self):
        urls = [
            "https://www.heart.org/en/health-topics/cholesterol/hdl-good-ldl-bad-cholesterol-and-triglycerides"
        ]
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 1},
                headers={"User-Agent": "Mozilla/5.0"})
            
    def parse(self, response):
        current_title = None
        current_sub = None
        section_data = None

        skip_titles = ["Contact Us","About Us", "Get Involved","Our Sites","Speed Bump"]
        skip_phrases = ["Advertisement", "Policy", "Cleveland Clinic is a non-profit"]

        for elem in response.xpath(' //h2 | //h3 | //p | //img'):
            tag = elem.xpath('name()').get()

            if tag == 'h2':
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

            elif tag == 'h3':
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
