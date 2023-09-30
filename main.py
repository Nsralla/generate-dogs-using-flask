from flask import Flask, render_template, request, session
import requests
from flask_session import Session

app = Flask(__name__)
user = {}  # this dictionary represents the user with attributes:
# 1- name, 2- total_dogs, 3- num_of_dogs_generated 4- num of login
users = []  # array to store users
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def home():
    global users
    global user
    users = session.get('users', [])  # Retrieve 'users' from the session, or use an empty list if it doesn't exist
    return render_template('logIn.html')  # display the login page


@app.route('/login', methods=['POST'])  # here we are at the login page
def login():
    global users
    global user
    user_name = request.form.get('user_name') # take the user name from the input

    # Fetch the 'users' list from the session, or initialize it as an empty list if it doesn't exist
    users = session.get('users', [])
    # Check if the user already has an account
    user = next((u for u in users if u['name'] == user_name), None)

    if user is None:  # if user doesn't own an account
        user = {'name': user_name, 'total_dogs': 0, 'num_of_login': 1, 'dogs_generated': 0}
        users.append(user)  # add the user to the array
    else:  # else if the user have an account
        user['num_of_login'] += 1  # increase number of logins
        user['dogs_generated'] = 0  # restart this value, since it must start from zero each time, and don't use the
        # saved value

    # Update the 'users' list in the session
    session['users'] = users  # send the new value of the array to the session
    # Sort the 'users' list based on the number of dogs generated
    sorted_users = sorted(users, key=lambda x: x['dogs_generated'], reverse=True)
    return render_template('logged.html', users=sorted_users, current_user=user)  # respawn the page with info for each user


@app.route('/get_dog', methods=['GET'])  # page containes each user info
def changeDog():
    global user
    global users
    if request.method == 'GET':
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        dog_img = response.json()  # to geneate random dog image
        user['dogs_generated'] += 1  # increase num of dogs generated
        user['total_dogs'] += 1  # increase num of total dogs generated
    # you have to sort the array if users depending on the number of dogs generated, but how?
        session['users'] = users  # save the array at the session after updating it
        sorted_users = sorted(users, key=lambda x: x['dogs_generated'], reverse=True)
    return render_template('logged.html', dog_img=dog_img['message'], users=sorted_users, current_user=user)


@app.route('/logout', methods=['POST'])
def logout():
    return render_template('logIn.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

