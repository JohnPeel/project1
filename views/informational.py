
from app import app
from db import get_cursor
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/team')
@app.route('/team/<abbr>')
def team(abbr=None):
    if abbr is None:
        teams = [[j.strip() for j in i] for i in get_cursor().execute('SELECT UNIQUE TEAM_ABBR, TEAM_NAME FROM TEAM').fetchall()]
        return render_template('team_list.html', teams=teams)

    team = get_cursor().execute('SELECT * FROM TEAM WHERE TRIM(TEAM_ABBR)=:0', (abbr,)).fetchall()
    if len(team) != 1:
        return 'ERROR: Unknown Team Abbr %s' % abbr

    stats = get_cursor().execute('''
        SELECT
              S1.SEASON,
              RECEIVING_YARDS,
              RECEIVING_TOUCHDOWNS,
              PASSING_YARDS,
              PASSING_TOUCHDOWNS,
              PASSING_INTERCEPTIONS,
              PASSING_ATTEMPTS,
              DEFENSIVE_SAFETIES,
              DEFENSIVE_TACKLES,
              DEFENSIVE_SACKS,
              DEFENSIVE_ASSIST_TACKLES,
              DEFENSIVE_INTERCEPTIONS,
              RUSHING_TOUCHDOWNS,
              RUSHING_YARDS,
              RUSHING_ATTEMPTS
        FROM (
            SELECT
                SEASON,

                ROUND(AVG(RECEIVING_YARDS),2) RECEIVING_YARDS,
                ROUND(AVG(RECEIVING_TOUCHDOWNS),2) RECEIVING_TOUCHDOWNS
            FROM
                 STATS
            inner join GAME ON (GAME.ID = GAME_ID)
            WHERE
                TRIM(TEAM_ABBR)=:0
            AND (RECEIVING_YARDS IS NOT NULL
             OR RECEIVING_TOUCHDOWNS IS NOT NULL)
            GROUP BY SEASON
        ) S1
        join (
            SELECT
                SEASON,

                ROUND(AVG(PASSING_YARDS),2) PASSING_YARDS,
                ROUND(AVG(PASSING_TOUCHDOWNS),2) PASSING_TOUCHDOWNS,
                ROUND(AVG(PASSING_INTERCEPTIONS),2) PASSING_INTERCEPTIONS,
                ROUND(AVG(PASSING_ATTEMPTS),2) PASSING_ATTEMPTS
            FROM
                 STATS
            inner join GAME ON (GAME.ID = GAME_ID)
            WHERE
                TRIM(TEAM_ABBR)=:0
            AND (PASSING_YARDS IS NOT NULL
             OR PASSING_TOUCHDOWNS IS NOT NULL
             OR PASSING_INTERCEPTIONS IS NOT NULL
             OR PASSING_ATTEMPTS IS NOT NULL)
            GROUP BY SEASON
        ) S2 ON (S1.SEASON = S2.SEASON)
        join (
            SELECT
                SEASON,

                ROUND(AVG(DEFENSIVE_SAFETIES),2) DEFENSIVE_SAFETIES,
                ROUND(AVG(DEFENSIVE_TACKLES),2) DEFENSIVE_TACKLES,
                ROUND(AVG(DEFENSIVE_SACKS),2) DEFENSIVE_SACKS,
                ROUND(AVG(DEFENSIVE_ASSIST_TACKLES),2) DEFENSIVE_ASSIST_TACKLES,
                ROUND(AVG(DEFENSIVE_INTERCEPTIONS),2) DEFENSIVE_INTERCEPTIONS
            FROM
                 STATS
            inner join GAME ON (GAME.ID = GAME_ID)
            WHERE
                TRIM(TEAM_ABBR)=:0
            AND (DEFENSIVE_SAFETIES IS NOT NULL
             OR DEFENSIVE_TACKLES IS NOT NULL
             OR DEFENSIVE_SACKS IS NOT NULL
             OR DEFENSIVE_ASSIST_TACKLES IS NOT NULL
             OR DEFENSIVE_INTERCEPTIONS IS NOT NULL)
            GROUP BY SEASON
        ) S3 ON (S1.SEASON = S3.SEASON)
        join (
            SELECT
                SEASON,

                ROUND(AVG(RUSHING_TOUCHDOWNS),2) RUSHING_TOUCHDOWNS,
                ROUND(AVG(RUSHING_YARDS),2) RUSHING_YARDS,
                ROUND(AVG(RUSHING_ATTEMPTS),2) RUSHING_ATTEMPTS
            FROM
                 STATS
            inner join GAME ON (GAME.ID = GAME_ID)
            WHERE
                TRIM(TEAM_ABBR)=:0
            AND (RUSHING_TOUCHDOWNS IS NOT NULL
             OR RUSHING_YARDS IS NOT NULL
             OR RUSHING_ATTEMPTS IS NOT NULL)
            GROUP BY SEASON
        ) S4 ON (S1.SEASON = S4.SEASON)
        ORDER BY SEASON ASC
        ''', (abbr,)).fetchall()

    seasons = [t[0] for t in stats]
    headers = [
        'Rec Yds',
        'Rec TD',
        'Pas Yds',
        'Pas TD',
        'Pas Int',
        'Pas Att',
        'Saf',
        'Takl',
        'Sack',
        'Ass Tkl',
        'Int',
        'Rush TD',
        'Rush Yds',
        'Rush Att'
    ]

    return render_template('team.html', headers=headers, seasons=seasons, team=team, stats=stats)


@app.route('/game/<id>')
def game(id):
    game = get_cursor().execute('''
SELECT A.TEAM_NAME,B.TEAM_NAME,G.*
FROM jpeel.GAME G,jpeel.TEAM A, jpeel.TEAM B
WHERE A.TEAM_ABBR = HOME_TEAM
  AND B.TEAM_ABBR = AWAY_TEAM
  AND G.id = :0''', (id,)).fetchall()

    if len(game) != 1:
        return 'ERROR: Unknown Game ID %s' % id

    stats = get_cursor().execute('''
    SELECT
           TEAM_ABBR,
           PLAYER_ID,
           FIRST_NAME,
           LAST_NAME,
           RECEIVING_YARDS,
           RECEIVING_TOUCHDOWNS,
           PASSING_YARDS,
           PASSING_TOUCHDOWNS,
           PASSING_INTERCEPTIONS,
           PASSING_ATTEMPTS,
           DEFENSIVE_SAFETIES,
           DEFENSIVE_TACKLES,
           DEFENSIVE_SACKS,
           DEFENSIVE_ASSIST_TACKLES,
           DEFENSIVE_INTERCEPTIONS,
           RUSHING_TOUCHDOWNS,
           RUSHING_YARDS,
           RUSHING_ATTEMPTS
    FROM
         STATS S
    JOIN PLAYERS P
        ON (S.PLAYER_ID = P.ID)
    WHERE GAME_ID=:0
    ORDER BY S.TEAM_ABBR
    ''', (id,)).fetchall()

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
