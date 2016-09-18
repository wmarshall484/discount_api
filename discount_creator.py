from datetime import datetime
from bs4 import BeautifulSoup
import urllib, urllib2
import random



class ShopifyDiscountCreator:
    post_headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7',
        'X-Prototype-Version': '1.7_rc2',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    def __init__(self, email, password, storename):

        # Required params
        self.email = email
        self.password = password
        self.storename = storename

        self.base_admin_url = "https://" + self.storename + ".myshopify.com/admin/"
        self.login_url = self.base_admin_url + "auth/login/"
        self.discounts_url = self.base_admin_url + "discounts/"
        self.new_discounts_url = self.discounts_url + "new/"


    def new_discount(self, value=None, name=None, discount_type = "fixed_amount", applies_to_resource="",
                     usage_limit_type = "no_limit", usage_limit="", applies_once_per_customer="0",
                     starts_at=str(datetime.today().year)+ '-' + str(datetime.today().month) + '-' + str(datetime.today().day),
                     discount_never_expires = "", minimum_order_amount="0"):
        # If no name is given, for now it's just a random hex string.
        if name is None:
            hex_chars = list("0123456789ABCDEF")
            name = ''.join(random.choice(hex_chars) for i in range(10))

        try:
            # make sure that the value is numeric
            value = str(float(value))
        except:
            raise ValueError("Must provide a discount amount and a numeric type")

        opener = self.__log_in()
        authentication_token = self.__get_auth_token(opener)
        
        headers = [(x, y) for x, y in ShopifyDiscountCreator.post_headers.iteritems()]
        opener.addheaders = headers
        
        form_data = {
            'utf8':"",
            'authenticity_token':authentication_token,
            'discount[code]':name,
            'discount[discount_type]':discount_type,
            'discount[value]':value,
            'discount[applies_to_resource]':applies_to_resource,
            'discount[minimum_order_amount]':minimum_order_amount,
            'usage_limit_type':usage_limit_type,
            'discount[usage_limit]':usage_limit,
            'discount[applies_once_per_customer]':applies_once_per_customer,
            'discount[starts_at]':starts_at,
            'discount_never_expires':discount_never_expires
        }
        
        
        encoded_post_data = urllib.urlencode( form_data )
        # create discount
        _file = opener.open( self.discounts_url, encoded_post_data)
        response = _file.read()
        _file.close()
        
        # discount code created!
        return name

    def __log_in(self):
        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        urllib2.install_opener( opener )
        # future requests will use the cookie processor that we install here
        
        # log in
        
        params = { 'login': self.email, 'password': self.password }
        encoded_params = urllib.urlencode( params )
        
        _file = opener.open( self.login_url, encoded_params )
        response = _file.read()
        #print response
        _file.close()
        return opener


    def __get_auth_token(self, opener):
        _file = opener.open( self.new_discounts_url )
        html = _file.read()
        _file.close()
        
        soup = BeautifulSoup(html, "lxml")
        auth_token = soup.find('input', type='hidden', attrs={'name': 'authenticity_token'})
        authentication_token = auth_token['value']
        return authentication_token


    def parse_discount_args(self, mdict):
        args = {}        
        self.copy_val_if_exists(mdict, args, "value")
        self.copy_val_if_exists(mdict, args, "name")
        self.copy_val_if_exists(mdict, args, "discount_type")
        self.copy_val_if_exists(mdict, args, "applies_to_resource")
        self.copy_val_if_exists(mdict, args, "minimum_order_amount")
        self.copy_val_if_exists(mdict, args, "usage_limit_type")
        self.copy_val_if_exists(mdict, args, "usage_limit")
        self.copy_val_if_exists(mdict, args, "applies_once_per_customer")
        self.copy_val_if_exists(mdict, args, "starts_at")
        self.copy_val_if_exists(mdict, args, "discount_never_expires")
        return args
        
    def copy_val_if_exists(self, mdict, args, key):
        if key in mdict:
            args[key] = mdict[key]
