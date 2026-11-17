import json
import urllib.request

def generate_nba_json():
    print("Récupération des données NBA avec séries Domicile/Extérieur...")
    url = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"
    
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            teams_list = []
            for conference in data.get('children', []):
                for entry in conference.get('standings', {}).get('entries', []):
                    team = entry.get('team', {})
                    
                    stats_dict = {}
                    home_val = "0-0"
                    road_val = "0-0"
                    streak_val = "0"
                    home_streak = "-"
                    road_streak = "-"
                    
                    for s in entry.get('stats', []):
                        name = s.get('name')
                        display_val = s.get('displayValue', s.get('summary', '0-0'))
                        
                        if name == 'gamesPlayed':
                            stats_dict['GP'] = s.get('value', 0)
                        elif name == 'wins':
                            stats_dict['W'] = s.get('value', 0)
                        elif name == 'losses':
                            stats_dict['L'] = s.get('value', 0)
                        elif name == 'winPercent':
                            stats_dict['WIN_PCT'] = s.get('value', 0)
                        elif name in ['home', 'Home']:
                            home_val = display_val
                        elif name in ['road', 'Away', 'away', 'roadRecord']:
                            road_val = display_val
                        elif name in ['streak', 'L10']:
                            streak_val = display_val
                        elif name in ['homeStreak', 'homestreak']:
                            home_streak = display_val
                        elif name in ['roadStreak', 'awayStreak', 'roadstreak', 'awaystreak']:
                            road_streak = display_val

                    teams_list.append({
                        'TEAM_NAME': team.get('displayName'),
                        'TEAM_ABBREVIATION': team.get('abbreviation'),
                        'GP': int(stats_dict.get('GP', 0)),
                        'W': int(stats_dict.get('W', 0)),
                        'L': int(stats_dict.get('L', 0)),
                        'WIN_PCT': float(stats_dict.get('WIN_PCT', 0)),
                        'HOME': home_val,
                        'ROAD': road_val,
                        'HOME_STREAK': home_streak,
                        'ROAD_STREAK': road_streak,
                        'L10': streak_val
                    })
            
            with open('nba_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nba_teams.json' généré avec les séries Domicile/Extérieur !")
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nba_json()
