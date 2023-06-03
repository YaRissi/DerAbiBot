if __name__ == '__main__':
    import re
    import cloudscraper
    from bs4 import BeautifulSoup

    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})

    html = scraper.get("https://sullygnome.com/channel/der_abi__/2021").content

    soup = BeautifulSoup(html, 'html.parser')

    match = re.findall('<div class="InfoStatPanelTLCell"[^>]*>[^>]*</div>', str(soup))

    firstyear = int(match[3].split("<")[1].split(">")[1])

    html = scraper.get("https://sullygnome.com/channel/der_abi__/2022").content

    soup = BeautifulSoup(html, 'html.parser')

    match = re.findall('<div class="InfoStatPanelTLCell"[^>]*>[^>]*</div>', str(soup))

    secondyear = int(match[3].split("<")[1].split(">")[1])

    if secondyear > firstyear:
        highest = secondyear
    else:
        highest = firstyear

    print(highest)




