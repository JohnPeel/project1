
from pprint import pprint
from app import app
from flask import render_template
from db import get_cursor

@app.route('/player')
def player():
    # List some players
    return render_template('player/index.html')

@app.route('/player/<id1>/<id2>/compare')
def compare_players_receiver(id1, id2):
    re_com_sql = '''
WITH common_games AS (
SELECT
  g1.ID
FROM
  JPEEL.PLAYERS p1
  CROSS JOIN JPEEL.PLAYERS p2
  JOIN JPEEL.STATS s1 ON (p1.ID = s1.PLAYER_ID)
  JOIN JPEEL.GAME g1 ON (s1.GAME_ID = g1.ID)
  JOIN JPEEL.STATS s2 ON (p2.ID = s2.PLAYER_ID)
  JOIN JPEEL.GAME g2 ON (s2.GAME_ID = g2.ID)
WHERE
  (p1.ID = :id1
  AND p2.ID = :id2)
  AND g1.ID = g2.ID
), player_stats AS (
SELECT p.ID,
  ROUND(AVG(PASSING_YARDS), 2)         AVG_PASSING_YARDS,
  ROUND(AVG(PASSING_TOUCHDOWNS), 2)    AVG_PASSING_TOUCHDOWNS,
  ROUND(AVG(PASSING_INTERCEPTIONS), 2) AVG_PASSING_INTERCEPTIONS,
  ROUND(AVG(PASSING_ATTEMPTS), 2)      AVG_PASSING_ATTEMPTS
FROM
  common_games
  JOIN JPEEL.STATS s ON (common_games.ID = s.GAME_ID)
  JOIN JPEEL.PLAYERS p ON (s.PLAYER_ID = p.ID)
WHERE
  (p.ID = :id1
  OR p.ID = :id2)
GROUP BY (p.ID)
)
SELECT
  p.ID,
  p.FIRST_NAME,
  p.LAST_NAME,
  AVG_PASSING_YARDS,
  AVG_PASSING_TOUCHDOWNS,
  AVG_PASSING_INTERCEPTIONS,
  AVG_PASSING_ATTEMPTS
FROM
  player_stats ps
  JOIN JPEEL.PLAYERS p ON (ps.ID = p.ID)
    '''.strip()
    data = get_cursor().execute(re_com_sql, id1=id1, id2=id2)
    headers = data.description
    player1 = data.fetchone()
    player2 = data.fetchone()
    label = 'passer'

    return render_template('player/compare.html', label=label, player1=player1, player2=player2, headers=headers)

@app.route('/player/<id>')
def player_stats(id):
    player_sql = '''
    SELECT
        FIRST_NAME,
        LAST_NAME,
        DOB,
        HOMETOWN
    FROM
        JPEEL.PLAYERS
    WHERE
        ID = :id
    '''.strip()

    season_avg_sql = '''
SELECT
    g.SEASON,
    ROUND(AVG(PASSING_YARDS),2) AVG_PASSING_YARDS,
    ROUND(AVG(PASSING_TOUCHDOWNS),2) AVG_PASSING_TOUCHDOWNS,
    ROUND(AVG(PASSING_INTERCEPTIONS),2) AVG_PASSING_INTERCEPTIONS,
    ROUND(AVG(PASSING_ATTEMPTS),2) AVG_PASSING_ATTEMPTS,
    ROUND(AVG(RUSHING_YARDS),2) AVG_RUSHING_YARDS,
    ROUND(AVG(RUSHING_TOUCHDOWNS),2) AVG_RUSHING_TOUCHDOWNS,
    ROUND(AVG(RUSHING_ATTEMPTS),2) AVG_RUSHING_ATTEMPTS,
    ROUND(AVG(RECEIVING_YARDS),2) AVG_RECEIVING_YARDS,
    ROUND(AVG(RECEIVING_TOUCHDOWNS),2) AVG_RECEIVING_TOUCHDOWNS
FROM
    JPEEL.PLAYERS p
    JOIN JPEEL.STATS s ON (p.ID = s.PLAYER_ID)
    JOIN JPEEL.GAME g ON (s.GAME_ID = g.ID)
WHERE
    p.ID = :id
GROUP BY (g.SEASON)
ORDER BY (g.SEASON) ASC
    '''.strip()

    all_avgs_sql = '''
WITH player_avgs AS (
SELECT
    g.SEASON,
    ROUND(AVG(PASSING_YARDS),2) AVG_PASSING_YARDS,
    ROUND(AVG(PASSING_TOUCHDOWNS),2) AVG_PASSING_TOUCHDOWNS,
    ROUND(AVG(PASSING_INTERCEPTIONS),2) AVG_PASSING_INTERCEPTIONS,
    ROUND(AVG(PASSING_ATTEMPTS),2) AVG_PASSING_ATTEMPTS,
    ROUND(AVG(RUSHING_YARDS),2) AVG_RUSHING_YARDS,
    ROUND(AVG(RUSHING_TOUCHDOWNS),2) AVG_RUSHING_TOUCHDOWNS,
    ROUND(AVG(RUSHING_ATTEMPTS),2) AVG_RUSHING_ATTEMPTS,
    ROUND(AVG(RECEIVING_YARDS),2) AVG_RECEIVING_YARDS,
    ROUND(AVG(RECEIVING_TOUCHDOWNS),2) AVG_RECEIVING_TOUCHDOWNS
FROM
    JPEEL.PLAYERS p
    JOIN JPEEL.STATS s ON (p.ID = s.PLAYER_ID)
    JOIN JPEEL.GAME g ON (s.GAME_ID = g.ID)
WHERE
    p.ID = :id
GROUP BY (g.SEASON)
ORDER BY (g.SEASON) ASC
), pa_avgs AS (
SELECT
    g.SEASON,
    ROUND(AVG(PASSING_YARDS),2) AVG_PASSING_YARDS,
    ROUND(AVG(PASSING_TOUCHDOWNS),2) AVG_PASSING_TOUCHDOWNS,
    ROUND(AVG(PASSING_INTERCEPTIONS),2) AVG_PASSING_INTERCEPTIONS,
    ROUND(AVG(PASSING_ATTEMPTS),2) AVG_PASSING_ATTEMPTS
FROM
    JPEEL.PLAYERS p
    JOIN JPEEL.STATS s ON (p.ID = s.PLAYER_ID)
    JOIN JPEEL.GAME g ON (s.GAME_ID = g.ID)
WHERE
    s.PASSING_YARDS > 5
GROUP BY (g.SEASON)
ORDER BY (g.SEASON) ASC
), re_avgs AS (
SELECT
    g.SEASON,
    ROUND(AVG(RECEIVING_YARDS),2) AVG_RECEIVING_YARDS,
    ROUND(AVG(RECEIVING_TOUCHDOWNS),2) AVG_RECEIVING_TOUCHDOWNS
FROM
    JPEEL.PLAYERS p
    JOIN JPEEL.STATS s ON (p.ID = s.PLAYER_ID)
    JOIN JPEEL.GAME g ON (s.GAME_ID = g.ID)
WHERE
    s.RECEIVING_YARDS > 5
GROUP BY (g.SEASON)
ORDER BY (g.SEASON) ASC
), ru_avgs AS (
SELECT
    g.SEASON,
    ROUND(AVG(RUSHING_YARDS),2) AVG_RUSHING_YARDS,
    ROUND(AVG(RUSHING_TOUCHDOWNS),2) AVG_RUSHING_TOUCHDOWNS,
    ROUND(AVG(RUSHING_ATTEMPTS),2) AVG_RUSHING_ATTEMPTS
FROM
    JPEEL.PLAYERS p
    JOIN JPEEL.STATS s ON (p.ID = s.PLAYER_ID)
    JOIN JPEEL.GAME g ON (s.GAME_ID = g.ID)
WHERE
    s.RUSHING_YARDS > 5
GROUP BY (g.SEASON)
ORDER BY (g.SEASON) ASC
)
SELECT
    pa.SEASON,
    player.AVG_PASSING_YARDS AVG_PASSING_YARDS,
    player.AVG_PASSING_TOUCHDOWNS AVG_PASSING_TOUCHDOWNS,
    player.AVG_PASSING_INTERCEPTIONS AVG_PASSING_INTERCEPTIONS,
    player.AVG_PASSING_ATTEMPTS AVG_PASSING_ATTEMPTS,
    player.AVG_RUSHING_YARDS AVG_RUSHING_YARDS,
    player.AVG_RUSHING_TOUCHDOWNS AVG_RUSHING_TOUCHDOWNS,
    player.AVG_RUSHING_ATTEMPTS AVG_RUSHING_ATTEMPTS,
    player.AVG_RECEIVING_YARDS AVG_RECEIVING_YARDS,
    player.AVG_RECEIVING_TOUCHDOWNS AVG_RECEIVING_TOUCHDOWNS,
    pa.AVG_PASSING_YARDS ALL_AVG_PASSING_YARDS,
    pa.AVG_PASSING_TOUCHDOWNS ALL_AVG_PASSING_TOUCHDOWNS,
    pa.AVG_PASSING_INTERCEPTIONS ALL_AVG_PASSING_INTERCEPTIONS,
    pa.AVG_PASSING_ATTEMPTS ALL_AVG_PASSING_ATTEMPTS,
    ru.AVG_RUSHING_YARDS ALL_AVG_RUSHING_YARDS,
    ru.AVG_RUSHING_TOUCHDOWNS ALL_AVG_RUSHING_TOUCHDOWNS,
    ru.AVG_RUSHING_ATTEMPTS ALL_AVG_RUSHING_ATTEMPTS,
    re.AVG_RECEIVING_YARDS ALL_AVG_RECEIVING_YARDS,
    re.AVG_RECEIVING_TOUCHDOWNS ALL_AVG_RECEIVING_TOUCHDOWNS
FROM
    pa_avgs pa
    JOIN ru_avgs ru ON (pa.SEASON = ru.SEASON)
    JOIN re_avgs re ON (pa.SEASON = re.SEASON)
    JOIN player_avgs player ON (pa.SEASON = player.SEASON)
    '''.strip()

    player = get_cursor().execute(player_sql, id=id)
    all_avgs = get_cursor().execute(all_avgs_sql, id=id)
    avgs_data = all_avgs.fetchall()
    avgs_headers = all_avgs.description
    seasons = [i[0] for i in avgs_data]

    return render_template('player/player.html',
                           player_data=player.fetchone(), player_data_headers=player.description,
                           seasons=seasons, avgs_data=avgs_data, avgs_headers=avgs_headers)

# Route simply returns an ID or null
@app.route('/player/search/<name>')
def player_search(name):
    sql = '''
SELECT
    p.ID
FROM
    JPEEL.PLAYERS p
WHERE
    (UPPER(TRIM(p.FIRST_NAME)) = :first
    AND UPPER(TRIM(p.LAST_NAME)) = :last)
    OR p.ID = :name
    '''.strip()

    first = name
    last = ''
    if ('+' in name):
        name_parts = name.split('+', 1)
        first = name_parts[0].strip().upper()
        last = name_parts[1].strip().upper()
    player = get_cursor().execute(sql, first=first, last=last, name=name).fetchone()
    if (player is None):
        return ''
    return player[0]
