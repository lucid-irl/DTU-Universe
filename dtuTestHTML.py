from bs4 import BeautifulSoup


def major(f):
    soup = BeautifulSoup(f, 'lxml')
    ul = soup.find('ul',class_='tabNavigation')
    return str(ul.li.a.text).strip()

filename = 'chuongtrinhhoc.html'
with open(filename, 'r', encoding='utf-8') as f:
    print(major(f))
