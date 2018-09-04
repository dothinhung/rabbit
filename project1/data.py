from urllib.request import urlopen
from bs4 import BeautifulSoup
import pyexcel


# 1 download webpage

# url = "http://bestslim.org/thuc-don-giam-can/"
# url = "http://bestslim.org/bi-quyet-giam-can/"
url = "http://bestslim.org/bai-tap-giam-can/"
html_content = urlopen(url).read()
# # print(html)

# # Save to file

f = open("exercise.html","wb")
f.write(html_content)
f.close()

# # # ROI 
soup = BeautifulSoup(html_content, "html.parser")
# div = soup.find("div", "ty-pagination-container")
div = soup.find("div", "ty-mainbox-body")

a = soup.find("a", "news-item-title")
# # print(div.prettify())

# # 3
div_list = div.find_all("div", "list-news-item")

posts = []

for div in div_list:
    post = {}
    a = div.find("a", "news-item-title")
    title = a.string
    href = a['href']

    post['title'] = title
    post['href'] = href
    posts.append(post)

    # print(posts)

# # print(a.prettify())

# # save 

pyexcel.save_as(records=posts, dest_file_name="exercise.xlsx")