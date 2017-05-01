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
	slip = ndb.StringProperty(default = None)

class Slip(ndb.Model):
	id = ndb.StringProperty(indexed = True)
	number = ndb.IntegerProperty()
	current_boat = ndb.StringProperty(default= None)
	arrival_date = ndb.StringProperty(default = None)

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
		else:
			all_boats = list()
			bQry = Boat.query()
			for boat in bQry.fetch(keys_only = True):
				b = boat.get()
				b_dict = b.to_dict()
				all_boats.append(b_dict)
			self.response.write(json.dumps(all_boats))
			
	
	def patch(self, id=None): #for modifying existing entries
		if id:
			b = ndb.Key(urlsafe=id).get()
			boat_data = json.loads(self.request.body)
			boat_data_keys = boat_data.keys()
			
			if 'boatname' in boat_data:
				b.boatname = boat_data['boatname']
			if 'type' in boat_data:
				b.type = boat_data['type']
			if 'length' in boat_data:
				b.length = boat_data['length']
			if 'at_sea' in boat_data:
				if boat_data['at_sea'] == true:
					if b.slip is not None:
						s = ndb.Key(urlsafe=b.slip).get()
						s.current_boat = None
					#if boat_data['at_sea'] == false						
				b.at_sea = boat_data['at_sea']
			b.put()
			#for x in boat_data_keys:
			#	b[x] = boat_data[x]
	
	def put(self, id=None): #change all existing values to new ones
		if id:
			b = ndb.Key(urlsafe=id).get()
			boat_data = json.loads(self.request.body)
			
			if 'boatname' in boat_data:
				b.boatname = boat_data['boatname']
			else:
				b.boatname = None
			if 'type' in boat_data:
				b.type = boat_data['type']
			else:
				b.type = None
			if 'length' in boat_data:
				b.length = boat_data['length']
			else:
				b.length = None
			if 'at_sea' in boat_data:
				b.at_sea = boat_data['at_sea']
			else:
				b.at_sea = True
			b.put()
	def delete(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			if b.slip is not None:
				s = ndb.Key(urlsafe=b.slip).get()
				s.current_boat = None
				s.put()
			ndb.Key(urlsafe=id).delete()
				
				
class SlipHandler(webapp2.RequestHandler):
	def post(self):
		slip_data = json.loads(self.request.body)
		new_slip = Slip()
		new_slip.number = slip_data['number']
		#new_slip.arrival_date = slip_data['arrival_date']

		new_slip.put()
		new_slip.id = new_slip.key.urlsafe()
		new_slip.put()
		slip_dict = new_slip.to_dict()
		slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
		self.response.write(json.dumps(slip_dict))
		
	def get(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			b_d = b.to_dict()
			b_d['self'] = "/boat/" + id
			self.response.write(json.dumps(b_d))
		else:
			all_slips = list()
			sQry = Slip.query()
			for slip in sQry.fetch(keys_only = True):
				s = slip.get()
				s_dict = s.to_dict()
				all_slips.append(s_dict)
			self.response.write(json.dumps(all_slips))
			
	def patch(self, id=None): #for modifying existing entries
		if id:
			s = ndb.Key(urlsafe=id).get()
			slip_data = json.loads(self.request.body)
			slip_data_keys = slip_data.keys()
			if s.current_boat is not None:
				webapp2.abort(403)
			
			if 'number' in slip_data:
				s.number = slip_data['number']
			if 'current_boat' in slip_data:
				s.current_boat = slip_data['current_boat']
				#add slip id to boat for better access
				bQry = Boat.query()
				for boat in bQry.fetch(50, keys_only = True):
					b = boat.get()
					#b_dict = b.to_dict()
					#self.response.write(json.dumps(b_dict))
					if b.boatname == s.current_boat:
						b.slip = id
						b.at_sea = False
						b.put()
			if 'arrival_date' in slip_data:
				s.arrival_date = slip_data['arrival_date']
			s.put()
			
	def put(self, id=None): 
		if id:
			s = ndb.Key(urlsafe=id).get()
			slip_data = json.loads(self.request.body)
			slip_data_keys = slip_data.keys()
			
			if 'number' in slip_data:
				s.number = slip_data['number']
			else:
				s.number = None
			if 'current_boat' in slip_data:
				s.current_boat = slip_data['current_boat']
			else:
				s.current_boat = None
			if 'arrival_date' in slip_data:
				s.arrival_date = boat_data['arrival_date']
			else:
				s.arrival_date = None
			b.put()
			
	def delete(self, id=None):
		if id:
			s = ndb.Key(urlsafe=id).get()
			if s.current_boat is not None:
				bQry = Boat.query()
				for boat in bQry.fetch(50, keys_only = True):
					b = boat.get()
					if b.boatname == s.current_boat:
						b.slip = None
						b.at_sea = True
						b.put()
			ndb.Key(urlsafe=id).delete()

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
	('/slip/(.*)', SlipHandler),
], debug=True)
# [END app]
