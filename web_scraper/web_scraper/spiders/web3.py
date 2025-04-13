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

        skip_titles = ["Contact Us","About Us", "Get Involved","Our Sites","Speed Bump","Trending Search"]
        skip_phrases = ["Advertisement", "Policy", "Cleveland Clinic is a non-profit"]
        unwanted_images = [
            "https://www.heart.org/en/-/media/Images/Health-Topics/Cholesterol/What-is-Cholesterol.jpg?sc_lang=en",
            "https://www.heart.org/en/-/media/Images/Health-Topics/Watch-Learn-and-Live/Cholesterol.jpg?sc_lang=en",
            "https://www.heart.org/en/-/media/Feature/Navigation/Social/x_color.svg?h=54&iar=0&mw=1910&w=54&sc_lang=en",
            "https://www.heart.org/en/-/media/Feature/Navigation/Social/facebook.svg?h=52&iar=0&mw=1910&w=52&sc_lang=en",
            "https://www.heart.org/en/-/media/Feature/Navigation/Social/linkedin.svg?h=52&iar=0&mw=1910&w=52&sc_lang=en",
            "https://www.heart.org/en/-/media/Feature/Social/mail.svg?h=52&iar=0&mw=1910&w=52&sc_lang=en",
            "https://www.heart.org/en/-/media/Feature/Social/copylink.svg?h=52&iar=0&mw=1910&w=52&sc_lang=en",
            "https://www.heart.org/en/-/media/Feature/Social/print.svg?h=52&iar=0&mw=1910&w=52&sc_lang=en",
            "https://www.heart.org/-/media/Images/Health-Topics/Cholesterol/doctor-reviewing-chart-with-patient.jpg?h=503&w=800&sc_lang=en&hash=297C80A167B17BCF8CF4A3FDC429B210",
            "https://www.heart.org/en/-/media/Images/Logos/Global-Do-No-Edit/Header/AHA_Full.svg?h=256&iar=0&mw=1910&w=426&sc_lang=en"
        ]

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
                    img_url = response.urljoin(img_url)
                    if img_url not in unwanted_images:
                        section_data['images'].append(img_url)

        if section_data and section_data['title'] not in skip_titles:
            yield section_data
