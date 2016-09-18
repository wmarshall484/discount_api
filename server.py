from flask import request, Flask, send_from_directory
from flaskrun import flaskrun
from discount_creator import ShopifyDiscountCreator
import sys
import traceback

app = Flask("MyAPI")

# Main landing page serves form
@app.route('/')
def hello_world():
        return send_from_directory("./", "form.html")

# This API only has one POST endpoint for creating a discount code.
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
