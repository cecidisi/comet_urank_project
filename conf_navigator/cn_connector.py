
import httplib2
from bs4 import BeautifulSoup as bs
from conf_navigator_eval.models import UserEval

class CN_connector:

	@classmethod
	def login(cls, email, password=None):
		# login_url = "http://halley.exp.sis.pitt.edu/cn3mobile/authenticateUser.jsp?email=[email]&password=[password]"
		# url = login_url.replace('[email]', email).replace('[password]', password)
		# h = httplib2.Http()
		# resp, content = h.request(url, method="GET")
		# soup = bs(content, 'xml')
		# status = soup.find('status').get_text()
		# # Autheticate with API
		# if status == "OK":
		# 	user =  {
		# 		'UserID': soup.find('UserID').get_text(),
		# 		'name': soup.find('name').get_text(),
		# 		'username': soup.find('username').get_text(),
		# 		'email': soup.find('email').get_text(),
		# 		'UserroleID': soup.find('UserroleID').get_text(),
		# 		'UserSessionID': soup.find('UserSessionID').get_text()
		# 	}
		# 	print 'Logged in user: ' + user['name']
		# 	return user
		# else:
		# 	# Login with DB
		# 	ueval = UserEval.objects.filter(email=email)
		# 	if len(ueval):
		# 		u = ueval[0]
		# 		user =  {
		# 			'UserID': u.pk,
		# 			'name': u.name,
		# 			'username': u.username,
		# 			'email': u.email
		# 		}
		# 		print user
		# 		return user
		# return False
		ueval = UserEval.objects.filter(email=email)
		if len(ueval):
			u = ueval[0]
			user =  {
				'UserID': u.pk,
				'name': u.name,
				'username': u.username,
				'email': u.email
			}
			print user
			return user
		return False



	@classmethod
	def bookmark(cls, user_id, content_id):
		temp_url = 'http://halley.exp.sis.pitt.edu/cn3mobile/bookmarkPaper.jsp?userid=[userid]&contentid=[contentid]'
		url = temp_url.replace('[userid]', user_id).replace('[contentid]', content_id)
		h = httplib2.Http()
		resp, content = h.request(url, method="GET")
		soup = bs(content, 'xml')
		print soup
		status = soup.find('status').get_text()
		if status == "OK":
			return True
		return None


	@classmethod
	def unbookmark(cls, user_id, content_id):
		temp_url = 'http://halley.exp.sis.pitt.edu/cn3mobile/unbookmarkPaper.jsp?userID=[userid]&contentID=[contentid]'
		url = temp_url.replace('[userid]', user_id).replace('[contentid]', content_id)
		h = httplib2.Http()
		resp, content = h.request(url, method="GET")
		soup = bs(content, 'xml')
		print soup
		status = soup.find('status').get_text()
		if status == "OK":
			return True
		return None

