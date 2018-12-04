
from app import app
from db import get_cursor
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/player')
@app.route('/player/<id>')
def player(id=None):
    return ''


@app.route('/team')
@app.route('/team/<abbr>')
def team(abbr=None):
    return ''


@app.route('/game')
@app.route('/game/<id>')
def game(id=None):
    if id is None:
        return ''

    game = get_cursor().execute('''
SELECT A.TEAM_NAME,B.TEAM_NAME,G.*
FROM jpeel.GAME G,jpeel.TEAM A, jpeel.TEAM B
WHERE A.TEAM_ABBR = HOME_TEAM
  AND B.TEAM_ABBR = AWAY_TEAM
  AND G.id = :0''', (id,)).fetchall()
    stats = get_cursor().execute('''SELECT * FROM STATS S, PLAYERS P WHERE GAME_ID=:0 AND S.PLAYER_ID=P.ID ORDER BY S.TEAM_ABBR''', (id,)).fetchall()

    if len(game) != 1:
        return 'ERROR'

    game = [str(x).strip() for x in game[0]]

    return render_template('game.html', game=game, stats=stats)


@app.route('/season')
@app.route('/season/<season>')
@app.route('/season/<season>/week/<week>')
def season(season=None, week=None):
    if season is None:
        seasons = sorted([x[0] for x in get_cursor().execute('SELECT UNIQUE SEASON FROM GAME')])
        return render_template('season_list.html', seasons=seasons)

    if week is None:
        weeks = sorted([x[0] for x in get_cursor().execute('SELECT UNIQUE WEEK FROM GAME WHERE SEASON=:0', (season,))])
        return render_template('week_list.html', season=season, weeks=weeks)

    games = get_cursor().execute('''
 SELECT A.TEAM_NAME,B.TEAM_NAME,G.*
 FROM jpeel.GAME G,jpeel.TEAM A, jpeel.TEAM B
 WHERE A.TEAM_ABBR = HOME_TEAM
   AND B.TEAM_ABBR = AWAY_TEAM
   AND SEASON=:0
   AND WEEK=:1
 ''', (season, week)).fetchall()
    return render_template('season.html', season=season, week=week, games=games)
