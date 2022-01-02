from bottle import route, run, template, static_file, request
from random import randrange, choice
from model import Sub_area, Npipes



@route('/hello/<name>') #tells Bottle on which route to make the function accessible. how to route the functiom
def say(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/')
def index(): #this is the starting point it links with the index.html file where we made the website
    # generate random weather for the first day
    weather_imgs = ['rain.svg', 'sun.svg']
    weather_img = choice(weather_imgs)
    if weather_img=='rain.svg':
        rainfall = randrange(15,20)
    else:
        rainfall = 0

    return template('index',  degree=randrange(25, 32), rainfall=rainfall, weather_img=weather_img,\
                    total_area=Sub_area(), count_pipes=Npipes())

# https://bottlepy.org/docs/dev/tutorial.html#routing-static-files
@route('/static/<filename>') #routes/links with all the files in the static folder where we put all the ststic files
def server_static(filename):
    return static_file(filename, root='./static/')

@route('/webhook', method='POST')
def webhook():
    print(request.json())
    req = request.json()

    intent = req["queryResult"]["intent"]["displayName"]

    responseText = f"you have values me with the  {intent} intent"

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}

    return res


run(host='localhost', port=8080)