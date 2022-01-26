import requests
import json
from datetime import date


# Select a team and run through rest of schedule adding opposing team points to total
def get_standings():
    url = "https://statsapi.web.nhl.com/api/v1/standings"
    w = requests.get(url)
    result = json.loads(w.content)['records']
    w.close()
    return result


def parse_standings(standings):
    result = []
    for division in standings:
        teams_list = division['teamRecords']
        for team in teams_list:
            result.append({'id': team['team']['id'], 'name': team['team']['name'], 'games_played': team['gamesPlayed'],
                           'points': team['points']})
    return result


def get_prev_team_schedule_by_id(team_id):
    today = date.today().strftime('%Y-%m-%d')
    url = f'https://statsapi.web.nhl.com/api/v1/schedule?teamId={team_id}&startDate=2021-10-12&endDate={today}'
    return get_content_from_url(url, 'dates')


def get_team_schedule_by_id(team_id):
    today = date.today().strftime('%Y-%m-%d')
    url = f'https://statsapi.web.nhl.com/api/v1/schedule?teamId={team_id}&startDate={today}&endDate=2022-12-31'
    return get_content_from_url(url, 'dates')


def get_content_from_url(url, endpoint):
    w = requests.get(url)
    result = json.loads(w.content)[endpoint]
    w.close()
    return result


rangers_id = 1


def get_opposing_team_points(team_id):
    global opposing_team_points
    game = schedule_date['games'][0]
    if game['teams']['away']['team']['id'] != team_id:
        opposing_team_id = game['teams']['away']['team']['id']
    else:
        opposing_team_id = game['teams']['home']['team']['id']
    opposing_team_points = next((item for item in teams_points if item["id"] == opposing_team_id), None)['points']
    return opposing_team_points


results = []

if __name__ == '__main__':
    standings = get_standings()
    teams_points = parse_standings(standings)
    for team in teams_points:
        team_schedule = get_team_schedule_by_id(team['id'])
        total_opposing_points = 0
        for schedule_date in team_schedule:
            opposing_team_points = get_opposing_team_points(team['id'])
            total_opposing_points += opposing_team_points
        avg = int(total_opposing_points / (82 - team['games_played']))
        results.append({'name': team['name'], 'total': total_opposing_points, 'by_games_played': avg})
    sorted_results = sorted(results, key=lambda i: i['by_games_played'], reverse=True)
    for count, k in enumerate(sorted_results, start=1):
        print(f"{count}. {k['name']} | total:{k['total']} | avg by games remaining:{k['by_games_played']}")


