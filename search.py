import grequests
from bs4 import BeautifulSoup as BS

_site = 'https://myshows.me/'


class Search:
    def __init__(self, name):
        self.input = name
        self.blocks = {}
        for i in filter(lambda block: block, self.get_blocks()):
            self.blocks[self.get_name_from_block(i)] = i
        self.names = list(self.blocks.keys())
        self.films = {}

    def get_blocks(self):
        urls = [_site + f'search/?q={self.input}']
        response = grequests.map((grequests.get(url) for url in urls))[0]
        result = BS(response.content, 'html.parser').find_all(lambda tag: tag.name == 'div' and
                                                                          tag.get('class') == ['Row'])
        return result

    def get_name(self, page):
        return page.find('div', class_='ShowDetails-original').text.strip()

    def get_name_from_block(self, block):
        return block.find('a').text.strip()

    def get_pages(self, blocks):
        result = []
        urls = [_site + block.find('div', attrs={'class': 'ShowCol-title'}).find('a').get('href') for block in
                blocks]
        response = grequests.map((grequests.get(url) for url in urls))
        for i in response:
            result.append(
                BS(i.content, 'html.parser').find('div', class_='ShowDetails'))
        return result

    def get_page_by_name(self, name):
        if name not in self.films:
            urls = [_site + self.blocks[name].find('div', attrs={'class': 'ShowCol-title'}).find('a').get('href')]
            response = grequests.map((grequests.get(url) for url in urls))[0]
            result = BS(response.content, 'html.parser').find('div', class_='ShowDetails')
            self.films[name] = result
        return self.films[name]

    def get_image(self, page):
        return page.find('div', class_='PicturePoster-picture').find('img').get('src')
