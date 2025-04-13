# Web Scraper with Scrapy 🕷️

This project uses [Scrapy](https://scrapy.org/) to scrape content from [WebMD](https://docs.google.com/spreadsheets/d/1gnFSagLXtFyx2UgNa4oSPa4PV12R-LROPHHFFj2ICts/edit?usp=sharing
)

- web1.py - scraps first two websites
- web2.py - for third
- web3.py - for fourth(for JS rendered websites)
- web4.py - for fifth

## 📌 Features

- Extracts hierarchical content structure (titles, subtitles, paragraphs, list items)
- Handles multiple images per section
- Handles JS rendered websites
- Outputs data in structured JSON format
- Easy to customize for other websites

## 🛠️ Installation

1. **Clone the repository**  
2. **Install all dependencies**
    using pip install -r requirements.txt
3. **Install Docker image for Splash**
    using docker pull scrapinghub/splash
4. **Run Docker image**
    using docker run -p 8050:8050 scrapinghub/splash

## 🚧 Challenges Faced

1. HTML structure was very inconsistent
2. Associating multiple images within the same section and maintaining their relationship with the textual content.
3. Handling JS rendered websites.
4. Handling anti-scrapping measures.
