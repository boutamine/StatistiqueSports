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
                divisions = conf.get('children', [])
                for div in divisions:
                    entries = div.get('standings', {}).get('entries', [])
                    for entry in entries:
                        team = entry.get('team', {})
                        
                        stats_dict = {}
                        display_stats = {}
                        
                        for s in entry.get('stats', []):
                            name = s.get('name')
                            stats_dict[name] = s.get('value', 0)
                            display_stats[name] = s.get('displayValue', s.get('summary', '0-0'))
                        
                        # Récupération robuste des bilans Domicile et Extérieur
                        home_val = display_stats.get('Home', display_stats.get('home', '0-0'))
                        road_val = display_stats.get('Road', display_stats.get('road', display_stats.get('Away', display_stats.get('away', '0-0'))))
                        streak_val = display_stats.get('streak', '0')
                        
                        teams_list.append({
                            'TEAM_NAME': team.get('displayName', 'Inconnu'),
                            'TEAM_ABBREVIATION': team.get('abbreviation', '---'),
                            'GP': int(stats_dict.get('gamesPlayed', 0)),
                            'W': int(stats_dict.get('wins', 0)),
                            'L': int(stats_dict.get('losses', 0)),
                            'T': int(stats_dict.get('ties', 0)),
                            'WIN_PCT': float(stats_dict.get('winPercent', 0)),
                            'HOME': home_val,
                            'ROAD': road_val,
                            'STREAK': streak_val
                        })
            
            with open('nfl_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print(f"Succès : {len(teams_list)} équipes NFL écrites dans 'nfl_teams.json'.")
            
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nfl_json()
