import os
import redis
import json
from flask import Flask, render_template, redirect, request, url_for, make_response

if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
else:
    r = redis.Redis(host='127.0.0.1', port='6379')

app = Flask(__name__)

@app.route('/')
def mainpage():

	response = """
	<HTML><BODY><h2>
	<a href="/survey">Take Survey</a><br>
	<a href="/dumpsurveys">Survey Results</a><br>
	</h2>
	</BODY>
	"""
	return response

@app.route('/survey')
def survey():
    resp = make_response(render_template('survey.html'))
    return resp

@app.route('/suthankyou.html', methods=['POST'])
def suthankyou():

    global r
    d = request.form['division']
    s = request.form['state']
    f = request.form['feedback']

    print "Division is " + d
    print "State is " + s
    print "Feedback: " + f

    Counter = r.incr('new_counter')
    print "the counter is now: ", Counter
    ## Create a new key that includes the counter
    newsurvey = 'new_survey' + str(Counter)

    print "Storing the survey now"
    ## Now the key name is the content of the variable newsurvey
    r.hmset(newsurvey,{'division':d,'state':s,'feedback':f})
	
    resp = """
    <h3> - THANKS FOR TAKING THE SURVEY - </h3>
    """
    return resp

@app.route('/dumpsurveys')
def dumpsurveys():

    global r
    response = "Dump of all reviews so far<br>"
    response += "--------------------------<br>"
    print "Reading back from Redis"
    for eachsurvey in r.keys('new_survey*'):
        response += "Division : " + r.hget(eachsurvey,'division') + "<br>"
        response += "State    : " + r.hget(eachsurvey,'state') + "<br>"
        response += "Feedback : " + r.hget(eachsurvey,'feedback') + "<br>"
        response += " ----------------------<br>"

    return response

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
