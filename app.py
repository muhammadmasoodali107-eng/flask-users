from flask import Flask, render_template

app = Flask(__name__)

users = {
    1: {
        "name": "Ali",
        "age": 25,
        "city": "Lahore",
        "job": "Software Engineer"
    },
    2: {
        "name": "Ahmed",
        "age": 28,
        "city": "Islamabad",
        "job": "DevOps Engineer"
    },
    3: {
        "name": "Sara",
        "age": 24,
        "city": "Karachi",
        "job": "Web Developer"
    }
}


@app.route("/")
def home():
    return render_template("index.html", users=users)


@app.route("/user/<int:user_id>")
def user(user_id):
    selected_user = users.get(user_id)

    if selected_user is None:
        return "User not found", 404

    return render_template(
        "user.html",
        user=selected_user
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)