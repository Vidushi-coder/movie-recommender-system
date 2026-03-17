from flask import Flask,render_template, request, redirect, url_for
import recommendation
from recommendation import movie_recommendation

app = Flask(__name__)

@app.route("/",methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/add",methods=['POST'])
def movie():
    movieName=request.form.get("movie")
    output = movie_recommendation(movieName)
    print("Movie received:", movieName)   
    print("Movies Recommended:",output)
    return render_template("index.html",Recommendations=output,MovieName=movieName)

if __name__ == '__main__':
    app.run(debug=True)
