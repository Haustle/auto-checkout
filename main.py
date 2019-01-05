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
    og_name = ""
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
                name = product_name[z].text
                temp_url = product_name[z]['href']
                temp_counter = 0
                for part in search.lower().split(" "):
                    if part in name.lower().split(" "): temp_counter += 1
                # print "{}: {}".format(name,temp_counter)
                if temp_counter > top_rated[1]:
                    og_name = name
                    top_rated[0] = (product_name[z]['href']).encode("utf-8")
                    top_rated[1] = temp_counter
                elif temp_counter == top_rated[1] and (temp_counter is not 0):
                    # print "{}: {}".format(name,temp_counter)
                    top_rated.append([temp_url,temp_counter])

                        
    print "url: {}".format(top_rated[0])
    return top_rated[0],og_name

def size_color_selection(driver,product_page,sizes=None,color=None):
    cop_style = []
    driver.get(product_page)
    time.sleep(1)
    page = (driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")).encode("utf-8")
    soup = BeautifulSoup(page,'html.parser')


    num_options = soup.find('form',action="https://www.golfwang.com/cart.php")
    first_div = num_options.find('div')
    forms = first_div.find_all('div', class_="form-field")


    # print "This is the length of forms: {}".format(len(forms))
    if len(forms) == 0:
        driver.find_element_by_id("form-action-addToCart").click()
        time.sleep(2)
        # driver.get('https://www.golfwang.com/cart.php')
        checkout(driver)

        return "NONE"
    else:
        while len(forms) != 0:
            # time.sleep(3)
            for x in range(len(forms)):
                # time.sleep(3)
                # print 'This form number: {}'.format(x+1)
                label = forms[x].find_all('label', class_="form-label form-label--alternate form-label--inlineSmall")
                # print "This is the length of label tag: {}".format(len(label))
                category = ""
                for u in range(len(label)):
                    # print 'There are {} different options'.format(len(label))
                    # THRES A BUNCH OF WHITE SPACE SO I NEED TO GET RID OF IT

                    category = label[u].text
                    category = " ".join(category.split()) # Pulls the string Size: or Color:
                    category = (category.split(" "))[0]
                    category = (category.split(":"))[0]
                if (len(forms) == 2) and (x == 0) and (category != 'Color'): 
                    continue

                selection_tag = forms[x].find_all('select','form-select form-select--small')
                # print "This is the length of drop downs: {}".format(len(selection_tag))


                for y in range(len(selection_tag)):
                    options = selection_tag[y].find_all('option', disabled=None)

                    if len(options) == 1: return 
                    else:
                        print ""
                        available_options = []
                        for z in range(len(options)):
                            if ((options[z].text).lower() != 'size') or ((options[z].text).lower() != 'color'):
                                available_options.append((options[z].text).encode("utf-8"))
                        
                        
                        # print len(forms)
                        user_buy_preference = []
                        if category == 'Size': user_buy_preference = sizes
                        elif category == 'Color': user_buy_preference = color

                        
                        # print "These are the user preferences: {}".format(user_buy_preference)
                        for z in range(len(user_buy_preference)):
                            # print "This is the length of user buy preference: {}".format(len(user_buy_preference))
                            option = user_buy_preference[z].title() if category == "Color" else user_buy_preference[z].upper()
                            # print "These are avaiable the {}\'s: {}".format(category,available_options)
                            # print "This is the first test_case : {}".format(option)
                            
                            if option in available_options:
                                select = driver.find_elements_by_xpath("//*[@class='form-select form-select--small']")
                                # print "This is the len of select: {}".format(len(select))
                                select = Select(driver.find_elements_by_xpath("//*[@class='form-select form-select--small']")[x])
                                
                                try:
                                    # print "Trying to select option: {}".format(option)
                                    select.select_by_visible_text(option)
                                    cop_style.append(option)
                                    # print "hello"
                                    if len(forms) == 1:
                                        # print 'Waiting to click checkout'
                                        driver.find_element_by_id("form-action-addToCart").click()
                                        # time.sleep(2)
                                        driver.get('https://www.golfwang.com/cart.php')
                                        checkout(driver)
                                        return cop_style
                                    else:
                                        forms.pop(x)
                                        print len(forms)
                                        break
                                except:
                                    if user_buy_preference[x] == user_buy_preference[-1]:
                                        return None
                                    else:
                                        print '\nSomething went wrong when selecting a size'
                                
                                    
                            
                                    

                                   
                        
                    break
            

def checkout(driver) :
    driver.get('https://www.golfwang.com/checkout.php')
    while True:
        try:
            driver.find_element_by_id('checkout-shipping-continue').click()
            break
        except:
            time.sleep(1)

    time.sleep(1)
    driver.find_element_by_id('ccNumber').send_keys(config.cred_num)
    driver.find_element_by_id('ccExpiry').send_keys(config.cred_exp)
    driver.find_element_by_id('ccName').send_keys(config.cred_name)
    driver.find_element_by_id('ccCvv').send_keys(config.cred_cvv)

def main(search=None,category=None, size=None, color=None, quantity=None):

    options = Options()
    options.headless = False

    driver = webdriver.Chrome('/Users/ty/Documents/chromedriver',chrome_options=options)
    driver.get('https://golfwang.com/login.php')
    driver.find_element_by_id('login_email').send_keys(config.user)
    driver.find_element_by_id('login_pass').send_keys(config.password)
    driver.find_element_by_css_selector("input[value='Sign in']").click()
    print '{}: SIGNED IN'.format(config.user)
    time.sleep(1)


    print "\nGOLF COP 30000 STARTIN IN 4 SECONDS"
    time.sleep(4)
    print "starting"
    start = time.time()
    product_page, product = getLink(search,category)
    selecting_options = size_color_selection(driver,product_page,size, color)

    end = time.time()
    print "\nIt took {:0.3f} seconds".format(end-start)
    if selecting_options is not None:
        print "COPPED: {}\nATTRIBUTES: {}\n".format(product,selecting_options)
        time.sleep(2)
        driver.get_screenshot_as_file('/Users/ty/Desktop/fsociety/py_programs/golf/purchases/cart2.png')
        time.sleep(10)
    else:
        print "They are sold out"

main(search="save the bees",category="tops",size=["XS","XL","L"] ,color=["Safety Orange","Black"])

