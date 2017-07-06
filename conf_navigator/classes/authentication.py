
import httplib2
from bs4 import BeautifulSoup as bs

login_url = "http://halley.exp.sis.pitt.edu/cn3mobile/authenticateUser.jsp?email=[email]&password=[password]"
# session_key = 'confnav'

class Auth:

	@classmethod
	def login(cls, email, password):
		url = login_url.replace('[email]', email).replace('[password]', password)
		h = httplib2.Http()
		resp, content = h.request(url, method="GET")
		soup = bs(content, 'xml')
		status = soup.find('status').get_text()
		# print str(status).replace('<status>', '').replace('</status>', '')
		if status == "OK":
			user =  {
				'UserID': soup.find('UserID').get_text(),
				'name': soup.find('name').get_text(),
				'username': soup.find('username').get_text(),
				'email': soup.find('email').get_text(),
				'UserroleID': soup.find('UserroleID').get_text(),
				'UserSessionID': soup.find('UserSessionID').get_text()
			}
			print 'Logged in user: ' + user['name']
			return user
		return False

	# @classmethod 
	# def set_session(cls, session_data):
	# 	request.session[session_key] = session_data


	# @classmethod
	# def validate(cls, request):
	# 	if session_key in request.session:
	# 		return True
	# 	return False


