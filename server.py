from flask import request, Flask, send_from_directory
from flaskrun import flaskrun
from discount_creator import ShopifyDiscountCreator
import sys
import traceback

#sdc = ShopifyDiscountCreator("wmarshall484@gmail.com", "randompass1", "marshall-emporium")
#sdc.new_discount(value="11", name="asdfasdf")

app = Flask("MyAPI")

@app.route('/')
def hello_world():
        return send_from_directory("./", "form.html")

@app.route('/new_discount', methods=['POST'])
def new_discount():
        try:
                sdc = ShopifyDiscountCreator(request.form['email']
                                             ,request.form['password']
                                             ,request.form['storename'])


                args =  sdc.parse_discount_args(request.form)
                discount_name = sdc.new_discount(**args)
                return "Created new discount code: " + discount_name
        except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print e        
        return "Error creating discount code"

flaskrun(app, default_host = "0.0.0.0", default_port="8000")
