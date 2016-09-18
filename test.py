import urllib, urllib2
 
opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
urllib2.install_opener( opener )
# future requests will use the cookie processor that we install here

# log in

params = { 'login': 'myusername', 'password': 'mypassword' }
encoded_params = urllib.urlencode( params )

_file = opener.open( 'https://myshop.myshopify.com/admin/auth/login', encoded_params )
response = _file.read()
_file.close()
