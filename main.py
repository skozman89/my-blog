from flask import Flask, render_template, request
import requests
import smtplib

my_email = "skozman.network@gmail.com"
password_2 = "zhlbeqrcgycztzqm"


app = Flask(__name__)

data = requests.get("https://api.npoint.io/674f5423f73deab1e9a7").json()


@app.route('/')
def home():
    return render_template('index.html', posts=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post/<int:index>')
def show_posts(index):
    requested_post = 0
    for blog_post in data:
        if blog_post['id'] == index:
            requested_post = blog_post

    return render_template('post.html', post=requested_post)

name = None
email = None
phone = None
message = None
@app.route("/form-entry", methods=['GET', 'POST'])
def receive_data():
    global name, email, phone, message
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    method_used = request.method
    print({"name": name, "email": email, "phone": phone, "message": message, "method_used": method_used})
    connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=my_email, password=password_2)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="shady.kozman1@gmail.com",
        msg=f"Subject:My Blog Notification\n\nname: {name}\nemail: {email}\nphone: {phone}\nmessage: {message}")
    connection.close()
    return render_template("message.html")


if __name__ == '__main__':
    app.run(debug=True)