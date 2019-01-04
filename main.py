import config, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

home_url = 'https://www.golfwang.com/'
all_url = home_url +'all'
cart_url = home_url +'cart.php'
outwear_url = home_url +'outerwear'
tops_url = home_url + 'tops'
sweats_url = home_url +'sweats'
bottoms_url = home_url + 'bottoms'
tees_url = home_url + 'tees'
hats_url = home_url + 'hats'
socks_url = home_url + 'socks'
accessories_url = home_url + 'accessories'
golf_le_fleur_url = home_url + 'golf-le-fleur'

# If there is a size need to add to the list

# options = Options()

# # Cant run chrome headless if you have extensions you want to add
# options.headless = False
# driver = webdriver.Chrome('F:\Program Files (x86)\Google\Chrome\Application\chromedriver',chrome_options=options)

item , base_url = ["alligator crocodile ", outwear_url]
result = requests.get(base_url)

page = result.text
soup = BeautifulSoup(page,'html.parser')
product_grid = soup.find_all('ul', class_='productGrid')
print "This is the length of product grd: {}".format(len(product_grid))
top_rated = ["filler url link", 0]

start = time.time()
for x in range(len(product_grid)):
    products = product_grid[x].find_all('li', class_="product")
    print "There are {} products\n{}\n".format(len(products),base_url)
    print base_url
    for y in range(len(products)):
        # print products
        product_names = products[y].find_all('h4', class_="card-title")
        
        for z in range(len(product_names)):
            # url = product_names[z].find_all('a', href=True)
            product_name = product_names[z].find_all('a', href=True)
            name = (product_name[z].text).lower()
            temp_url = product_name[z]['href']
            temp_counter = 0
            for part in item.split(" "):
               if part in name.split(" "): temp_counter += 1
            
            if temp_counter > top_rated[1]:
                top_rated[0] = (product_name[z]['href']).encode("utf-8")
                top_rated[1] = temp_counter
            elif temp_counter == top_rated[1] and (temp_counter is not 0):
                top_rated.append([temp_url,temp_counter])


end = time.time()
print "It took {:0.2f} seconds".format(end-start)
print ""
print top_rated




# driver.get(accessories_url)

