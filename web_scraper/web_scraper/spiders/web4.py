import scrapy
from pathlib import Path
from urllib.parse import urlparse


class Web1Spider(scrapy.Spider):
    name = "web4"

    def start_requests(self):
        urls = [
            "https://medlineplus.gov/cholesterol.html#:~:text=What%20is%20cholesterol%3F,all%20the%20cholesterol%20it%20needs"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        current_title = None
        section_data = None

        skip_titles = ["Basics","Learn More", "See, Play and Learn","Research","Resources","For You"]
        skip_phrases = ["Advertisement", "Policy", "Cleveland Clinic is a non-profit"]
        unwanted_images = {
            "nih.png", "feed.png", "i_share_twitter.png", "i_share_fb.png",
            "Instagram_Glyph_Gradient_RGB.png", "i_social_media_toolkit.png", "return-top.png",
            "videocamera.gif"
        }

        for elem in response.css('h3, li, p, img'):
            tag = elem.root.tag

            if tag == 'h3':
                if section_data and section_data['title'] not in skip_titles:
                    yield section_data

                current_title = elem.xpath('normalize-space()').get()
                section_data = {
                    'title': current_title,
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
                    img_name = Path(urlparse(img_url).path).name
                    if img_name not in unwanted_images:
                        section_data['images'].append(response.urljoin(img_url))

        if section_data and section_data['title'] not in skip_titles:
            yield section_data