# GoCD Queue Monitor ( both the the project and the documentation are under construction  )
An web app to monitor the GoCD continuos delivery server, showing the current queue of pipelines and jobs waiting to be executed.

## Requirements

- Python 3
- Pip

Run to install the project dependencies:
```
pip install -r requirements.txt
```

## How to run

This project requires some environment variables to run. You can create a `.env` file on the root directory and the application will try to extract all the variables from there, alternatively you can create the variables yourself.

The required variables are:
```
#The GoCD API endpoint
GOCD_API_URL=https://gocd.example.com.br:8888/go/api/
#A GoCD user that can consume the API
GOCD_USER=exampleuser
#The above user password
GOCD_PASSWORD=examplepass123
# Flask requires this variable to be set to the file that contains the Flask app, in this project I'm using  main.py
FLASK_APP=main.py
```

Otionally you can also set:

```
# This makes flags more information on the logs, and enable cool dev features like hot-reloading on the app
FLASK_DEBUG=1
```

After the variables are set you can start the app with:

```
python -m flask run
```