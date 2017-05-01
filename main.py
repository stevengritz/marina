from google.appengine.ext import ndb
import webapp2
import json

# [START main_page]
class Boat(ndb.Model) :
	id = ndb.StringProperty()
	boatname = ndb.StringProperty()
	type = ndb.StringProperty()
	length = ndb.FloatProperty()
	at_sea = ndb.BooleanProperty(default = True)

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
		new_boat.put()
		boat_dict = new_boat.to_dict()
		latest_key = dict()
		latest_key['boat_id'] = new_boat.key.urlsafe()
		new_boat.id = new_boat.key.urlsafe()
		new_boat.put()
		self.response.write(json.dumps(latest_key))
		
	def get(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			b_d = b.to_dict()
			b_d['self'] = "/boat/" + id
			self.response.write(json.dumps(b_d))
		#else:
			
			

		
		
class SlipHandler(webapp2.RequestHandler):
	def post(self):
		boat_data = json.loads(self.request.body)
		new_boat = Boat()
		new_boat.boatname = boat_data['boatname']
		new_boat.type = boat_data['type']
		new_boat.length = boat_data['length']
		new_boat.at_sea = boat_data['at_sea']
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))

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
	('/boat/(.*)', BoatHandler),
	('/slip', SlipHandler),
], debug=True)
# [END app]
