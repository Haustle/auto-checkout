import config, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time



# If there is a size need to add to the list


# cart_url = home_url +'cart.php'
def genreChoose(genre):
    genre = genre.lower()
    home_url = 'https://www.golfwang.com/'


    if genre == 'outerwear': return (home_url +'outerwear')
    elif genre == 'tops' : return (home_url + 'tops')
    elif genre == 'sweats': return (home_url +'sweats')
    elif genre == 'bottoms': return (home_url + 'bottoms')
    elif genre == 'tees': return (home_url + 'tees')
    elif genre == 'hats': return (home_url + 'hats')
    elif genre == 'socks' : return (home_url + 'socks')
    elif genre == 'accessories': return (home_url + 'accessories')
    elif genre == 'le-fleur': return (home_url + 'golf-le-fleur')


def getLink(search=None , category=None, color=None):

    url = genreChoose(category)
    result = requests.get(url)
    page = result.text
    soup = BeautifulSoup(page,'html.parser')
    product_grid = soup.find_all('ul', class_='productGrid')
    # print "This is the length of product grd: {}".format(len(product_grid))

    #First element is the link, second is the score
    top_rated = ["filler url link", 0]

    for x in range(len(product_grid)):
        products = product_grid[x].find_all('li', class_="product")
        # print "There are {} products\n{}\n".format(len(products),url)
        # print url
        for y in range(len(products)):
            # print products
            product_names = products[y].find_all('h4', class_="card-title")
            
            for z in range(len(product_names)):
                # url = product_names[z].find_all('a', href=True)
                product_name = product_names[z].find_all('a', href=True)
                name = (product_name[z].text).lower()
                temp_url = product_name[z]['href']
                temp_counter = 0
                for part in search.split(" "):
                    if part in name.split(" "): temp_counter += 1
                    
                    if temp_counter > top_rated[1]:
                        top_rated[0] = (product_name[z]['href']).encode("utf-8")
                        top_rated[1] = temp_counter
                    elif temp_counter == top_rated[1] and (temp_counter is not 0):
                        top_rated.append([temp_url,temp_counter])

                        

    print "url: {}".format(top_rated[0])
    return top_rated[0]

def size_color_selection(driver,product_page,sizes=None,color=None):
    driver.get(product_page)
    page = (driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")).encode("utf-8")
    soup = BeautifulSoup(page,'html.parser')
    
    product_view = soup.find('div',class_='productView-options')
    forms = product_view.find_all('div', class_="form-field")
    # print "This is the length of forms: {}".format(len(forms))
    for x in range(len(forms)):
        
        label = forms[x].find_all('label', class_="form-label form-label--alternate form-label--inlineSmall")
        # print "This is the length of label tag: {}".format(len(label))
        category = ""
        for u in range(len(label)):
            # THRES A BUNCH OF WHITE SPACE SO I NEED TO GET RID OF IT

            category = label[u].text
            category = " ".join(category.split()) # Pulls the string Size: or Color:
            category = (category.split(" "))[0]
            category = (category.split(":"))[0]
            print category # Size:

        selection_tag = forms[x].find_all('select','form-select form-select--small')
        # print "This is the length of drop downs: {}".format(len(selection_tag))

        for y in range(len(selection_tag)):
            options = selection_tag[y].find_all('option', disabled=None)
            # print 'hello'
            print "This is the length of SIZE OPTIONS: {}".format(len(options))
            if len(options) == 1: print 'They are sold out'
            else:
                print ""
                available_sizes = []
                for z in range(len(options)):
                    if (options[z].text).lower() != category.lower():
                        available_sizes.append((options[z].text).lower())
                print "These are avaiable the {}\'s: ".format(category)
                if sizes is None: sizes = color
                for option in sizes:
                    if option.lower() in available_sizes:
                        print 'We can purchase this in size: {}'.format(option)
                        select = Select(driver.find_element_by_xpath("//*[@class='form-select form-select--small']"))
                        select.select_by_visible_text(option)
                        driver.find_element_by_id("form-action-addToCart").click()
                        time.sleep(1)
                        driver.get('https://www.golfwang.com/cart.php')
                        print 'We got this far'
                        # time.sleep(2)
                        # driver.get_screenshot_as_file('C:\Users\haust\Desktop\golf\purchases\cart2.png')
                        break
                        # time.sleep(10)
                    
            break


        
    return "hello"

    # driver.get(product_page)
    # select = Select(driver.find_element_by_class_name('form-select form-select--small'))
    # official_size = ""
    # for size in sizes:
    #     try:
    #         select.select_by_visible_text(size)
    #     except:
    #         print "This size is out of stock: \'{}\'".format(size)

    # if color is not None:
    #     return "Added a {} {} to cart".format(official_size, color)
    # return "Added a {} to cart".format(official_size)
    

def main(search=None,category=None, size=None, color=None):

    options = Options()
    options.headless = False
    driver = webdriver.Chrome('F:\Program Files (x86)\Google\Chrome\Application\chromedriver',chrome_options=options)
    
    # cart_url = home_url +'cart.php
    start = time.time()
    product_page = getLink(search,category)
    selecting_options = size_color_selection(driver,product_page,size, color)

    end = time.time()
    print "\nIt took {:0.3f} seconds".format(end-start)
    print ""

main(search="duffle bag",category="accessories",color=["Black","Lavender"])

