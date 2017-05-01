from google.appengine.ext import ndb
import webapp2
import json

# [START main_page]
class Boat(ndb.Model) :
	id = ndb.KeyProperty()
	boatname = ndb.StringProperty()
	type = ndb.StringProperty()
	length = ndb.FloatProperty()
	at_sea = ndb.BooleanProperty()

class Slip(ndb.Model):
	id = ndb.StringProperty(indexed = True)
	number = ndb.IntegerProperty()
	current_boat = ndb.StringProperty(default="")
	arrival_date = ndb.FloatProperty()

class BoatHandler(webapp2.RequestHandler):
	def post(self):
		boat_data = json.loads(self.request.body)
		new_boat = Boat()
		new_boat.boatname = boat_data['boatname']
		new_boat.type = boat_data['type']
		new_boat.length = boat_data['length']
		new_boat.at_sea = boat_data['at_sea']
		boat_key = new_boat.put()
		self.response.write(json.dumps(new_boat.to_dict()))
		self.response.write('\n')
		self.response.write(boat_key.string_id())

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("Hello")

# [START app]
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler),
], debug=True)
# [END app]
