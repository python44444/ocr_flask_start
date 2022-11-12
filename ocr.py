from flask import Flask, render_template, request, flash, redirect
import pyocr
from PIL import Image
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(32)


@app.route("/")
def indes():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        if "unko" not in request.files:
            print("shitttttt")
            error_message = "You diedddddd!!!"
            print(error_message)
            return render_template("index.html", result=error_message)

        file = request.files["unko"]

        if file.filename == "":
            error_message = "You lostttttt!!!"
            print(error_message)
            return render_template("index.html", result=error_message)

        if file:
            tools = pyocr.get_available_tools()
            tool = tools[0]

            img = Image.open(file)
            img.save("static/images/image.png")
            image = Image.open("static/images/image.png")

            txt = tool.image_to_string(
                image, lang="eng", builder=pyocr.builders.TextBuilder()
            )
            if len(txt) == 0:
                error_message = "You lost!!!"
                return render_template("index.html", result=error_message)
            else:
                return render_template("index.html", result=txt)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
