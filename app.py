from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "password"
boggle_game = Boggle()

@app.route("/")
def start():
    game = boggle_game.make_board()
    session['game'] = game
    plays = session.get("plays", 0)
    bestscore = session.get("bestscore", 0)
    return render_template("index.html", game = game, plays = plays, bestscore = bestscore)

@app.route("/checkforword")
def checkforword():
    word = request.args["word"]
    game = session["game"]
    response = boggle_game.check_valid_word(game, word)
    return jsonify({'result': response})

@app.route("/showscore", methods=["POST"])
def showscore():
    score = request.json["score"]
    plays = session.get("plays", 0)
    bestscore = session.get("bestscore", 0)
    session['plays'] = plays + 1
    session['bestscore'] = max(score, bestscore)
    return jsonify(newRecord = score > bestscore)
