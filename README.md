# Cooking forum

Cooking forum is a simple Python microservice exposing apis to signup, login and verify users of the forum.


## Usage

The first thing to do to launch the project is to install the requirements.
We strongly suggest to create a virtual environment before running the command below in order not to mess up with all the other packages in your pc.
To do so, enter in the project directory and launch the following commands.

### Prerequisites

```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
Once done that you sould be inside the virtual environment and you can run the command to install the required packages.

```bash
pip install -r requirements.txt
```

### Configuring the env file
In order to use cooking forum apis you must provide a .env file. The project contains an .env.example file containing all the needed variables which are reported here together with comments to explain their purpose.

```bash
SECRET_KEY = 'my-secret-key' #MANDATORY, used for JWT creation

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite' #MANDATORY, used to store users

#OPTIONAL. 
#Configurations for an email server. 
#If missing OTP will be displayed in standard output and in the error message of the api
MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'mailtrap-username'
MAIL_PASSWORD = 'mailtrap-password'
MAIL_USE_TLS = true
MAIL_FROM_NAME ='cooking@forum.com'
```

### Launching the service
Now you can launch the app using this command
```bash
flask --app main run --host=0.0.0.0
```

### Route overview
```bash
http://127.0.0.1:5000/api/
```
The application exposes four main routes, accessible, using the base endpoint stated above.

```bash
/signup #to signup the user
```
During the signup you must specify a valid name, email password and the `has2fa` flag, to state if you want to enable the 2 factor authentication.

```bash
/login #to log the user in
```
You must provide the same email and password provided during the signup. If 2 factor authentication is enabled, the otp that must be provided calling the verify route will be sent via mail or printed in the standard output (and api error message) if email client is not configured. If not, a JWT token is returned.

```bash
/verify #to verify the otp received during login process (if user has 2fa enabled)
```
Route to be called with the same email and password used in the login process and the otp received via mail (or in the standard output (and api error message) if email client is not configured)

```bash
/users #route acessible only if user is logged in
```
Route accessible only providing a valid JWT as bearer token. It displays a list of all subscribed users.

Further informations on the api can be found in the `openapi.yml` in the project

## Using with docker
If you prefer to run the code via docker (or to deploy it in any cloud server), the project's image can be pulled from docker hub using the command 

```bash
docker pull quintavallechristian/cooking-forum:latest
```

Once done that you can launch the application using the command. 

```bash
docker run --publish 5000:5000 quintavallechristian/cooking-forum
```

The image comes with a predefined .env containing only the mandatory fields. In this case emails will not be sent. If you wish to enable the email service you must provide a proper .env file running this command instead.

```bash
docker run --env-file=.env --publish 5000:5000 quintavallechristian/cooking-forum
```