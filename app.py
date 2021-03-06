import os
import redis
from flask import Flask, render_template, redirect, request, url_for, make_response

#r = redis.Redis(host='123.12.148.95', port='15379', password='ABCDEFG1231LQ4L')
r = redis.Redis(host='redis-14970.c11.us-east-1-2.ec2.cloud.redislabs.com', port='14970', password='0kHipVLmq9TZM7iSg7WxrWxNkpvdwlh0', decode_responses=True)

app = Flask(__name__) 

@app.route('/')
def survey():
    resp = make_response(render_template('save.html'))
    return resp

@app.route('/suthankyou.html', methods=['POST'])
def suthankyou():
    d = request.form['LambSwitch']

    print "LambSwitch is " + d
	
    if d not in ['ON', 'OFF', 'AUTO']:
        resp="""
		<h3> - LambSwitch State Error, Please input ON/OFF/AUTO! - </h3>
		"""
        return resp

#    print "Storing the switch now"
    r.hmset('Switch',{'LambSwitch':d})

#    print "--------------------------"
#    print "Reading it back from Redis"
#    print "LambSwitch : " + r.hget('Switch','LambSwitch')
	
    resp = """
    <h3> - LambSwitch Saved - </h3>
    """
    return resp


@app.route('/getstatus.html', methods=['GET'])
def getstatus():
    print 'begin get data'
    d=r.hget('Switch','LambSwitch')
    print "LambSwitch : " + d
#    print 'Switch status:',r
	
#    resp = r
    return d

	
if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
        port=int(os.getenv('PORT', '5000')), threaded=True)

