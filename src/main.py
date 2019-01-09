import config, requests, time, os
from order_form_sort import getOrders
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException



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
    time_to_find = time.time()
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

    time_to_end = time.time()
    print "It took {} to find the link to the product".format(time_to_end-time_to_find)    
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
        time.sleep(1)
        driver.find_element_by_id("form-action-addToCart").click()
        time.sleep(2)

        return "NONE"
    else:
        # print "WE ARE IN THE LOOP FOR SLECTING"
        while len(forms) != 0:
            # time.sleep(3)
            # print 'forms is not 0'
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
                    # print category
                if (len(forms) == 2) and (x == 0) and (category != 'Color'): 
                    continue

                selection_tag = forms[x].find_all('select','form-select form-select--small')
                # print "This is the length of drop downs: {}".format(len(selection_tag))
                # time.sleep(5)

                for y in range(len(selection_tag)):
                    options = selection_tag[y].find_all('option', disabled=None)
                    # print len(options)
                    if len(options) == 1: return 
                    else:
                        # print ""
                        available_options = []
                        for z in range(len(options)):
                            if ((options[z].text).lower() != 'size') or ((options[z].text).lower() != 'color'):
                                available_options.append((options[z].text).encode("utf-8"))
                        
                        
                        # print "This is the list of available options: {}".format(available_options)
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
                                    if len(forms) == 1:
                                        driver.find_element_by_id("form-action-addToCart").click()
                                        time.sleep(1)

                                        return cop_style
                                    else:
                                        forms.pop(x)
                                        break
                                except:
                                    if user_buy_preference[x] == user_buy_preference[-1]:
                                        return None
                                    else:
                                        print '\nSomething went wrong when selecting a size'
                                
                                    
                            
                                    

                                   
                        
                    break
            

def checkout(driver) :
    driver.get('https://www.golfwang.com/checkout.php')
    time.sleep(1)
    while True:
        try:
            driver.find_element_by_id('checkout-shipping-continue').click()
            break
        except:
            time.sleep(1)

    time.sleep(2)
    while True:
        try:
            driver.find_element_by_id('ccNumber').send_keys(config.cred_num) # WAITING FOR THIS ELEMENT IS CAUSING THE MOS
            break
        except NoSuchElementException:
            time.sleep(1)
    
    driver.find_element_by_id('ccExpiry').send_keys(config.cred_exp)
    driver.find_element_by_id('ccName').send_keys(config.cred_name)
    driver.find_element_by_id('ccCvv').send_keys(config.cred_cvv)

def main(search=None,category=None, size=None, color=None, quantity=None):

    options = Options()
    options.headless = True

    #RETRIEVING ITEMS FROM EXCEL SHEET
    # print "This is the current cwd: {}".format(__file__)
    excel_sheet_location = '{}/ORDER_FORM.xlsx'.format(os.getcwd())
    # print "This is excel sheet location: {}".format(excel_sheet_location)
    orderList = getOrders(excel_sheet_location)

    if len(orderList) > 0:
    # SIGNING INTO THE WEBSITE
        driver = webdriver.Chrome(config.driver_loc,chrome_options=options)
        driver.get('https://golfwang.com/login.php')
        driver.find_element_by_id('login_email').send_keys(config.user)
        driver.find_element_by_id('login_pass').send_keys(config.password)
        driver.find_element_by_css_selector("input[value='Sign in']").click()
        time.sleep(5)
        print 'golfwang.com : SIGNED IN'.format(config.user)
        # print "STARTING"
        
        start = time.time()
        items_copped = []
        for x in range(len(orderList)):
            local_start = time.time()
            quantity = orderList[x][0]
            category = orderList[x][1].lower()
            search = orderList[x][2].lower()
            color = (orderList[x][3]).split(",") if orderList[x][3] != 'None' else None
            size = (orderList[x][4]).split(",") if orderList[x][4] != 'None' else None


            product_page, product = getLink(search,category)
            selecting_options = size_color_selection(driver,product_page,size, color) if (x == len(orderList)-1) else size_color_selection(driver,product_page,size, color)
            local_end = time.time()

            print "\nIt took {:0.3f} seconds to add to cart".format(local_end-local_start)
            if selecting_options is not None:
                items_copped.append("ADDED TO CART: {}\nATTRIBUTES: {}\n".format(product,selecting_options))
                if x == len(orderList)-1:
                    checkout(driver)
                    end = time.time()
                    print "CHECKED OUT IN: {} seconds".format(end-start)

                    for item in items_copped:
                        print "\n{}".format(item)
                    # time.sleep(2)
                    driver.get_screenshot_as_file('{}/purchases/cart{}.png'.format(os.getcwd(),x))
                    time.sleep(10)
                else: continue
            else:
                print "They are sold out"
        

main()

