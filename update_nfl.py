import json
import urllib.request

def generate_nfl_json():
    print("Récupération des données NFL...")
    url = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    
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
            conferences = data.get('children', [])
            
            for conf in conferences:
                for div in conf.get('children', []):
                    for entry in div.get('standings', {}).get('entries', []):
                        team = entry.get('team', {})
                        stats = {s['name']: s for s in entry.get('stats', [])}
                        
                        gp = stats.get('gamesPlayed', {}).get('value', 0)
                        wins = stats.get('wins', {}).get('value', 0)
                        losses = stats.get('losses', {}).get('value', 0)
                        ties = stats.get('ties', {}).get('value', 0)
                        win_pct = stats.get('winPercent', {}).get('value', 0)
                        
                        home_record = stats.get('home', {}).get('displayValue', '0-0')
                        road_record = stats.get('road', {}).get('displayValue', '0-0')
                        streak = stats.get('streak', {}).get('displayValue', '0')
                        
                        teams_list.append({
                            'TEAM_NAME': team.get('displayName'),
                            'TEAM_ABBREVIATION': team.get('abbreviation'),
                            'GP': int(gp),
                            'W': int(wins),
                            'L': int(losses),
                            'T': int(ties),
                            'WIN_PCT': float(win_pct),
                            'HOME': home_record,
                            'ROAD': road_record,
                            'STREAK': streak
                        })
            
            with open('nfl_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nfl_teams.json' généré avec succès !")
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nfl_json()
