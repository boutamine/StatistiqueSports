import json
import urllib.request

def generate_nfl_json():
    print("Récupération des données NFL...")
    url = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.espn.com/',
            'Origin': 'https://www.espn.com'
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
                        
                        # Extraction sécurisée de toutes les statistiques
                        stats_dict = {}
                        for s in entry.get('stats', []):
                            name = s.get('name')
                            val = s.get('value', s.get('displayValue', 0))
                            stats_dict[name] = val
                            
                        teams_list.append({
                            'TEAM_NAME': team.get('displayName'),
                            'TEAM_ABBREVIATION': team.get('abbreviation'),
                            'GP': stats_dict.get('gamesPlayed', 0),
                            'W': stats_dict.get('wins', 0),
                            'L': stats_dict.get('losses', 0),
                            'T': stats_dict.get('ties', 0),
                            'WIN_PCT': stats_dict.get('winPercent', 0),
                            'HOME': next((s.get('displayValue', '0-0') for s in entry.get('stats', []) if s.get('name') in ['Home', 'home']), '0-0'),
                            'ROAD': next((s.get('displayValue', '0-0') for s in entry.get('stats', []) if s.get('name') in ['Road', 'road', 'Away', 'away']), '0-0'),
                            'STREAK': next((s.get('displayValue', '0') for s in entry.get('stats', []) if s.get('name') == 'streak'), '0')
                        })
            
            with open('nfl_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print(f"Succès : {len(teams_list)} équipes NFL écrites dans 'nfl_teams.json'.")
            
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nfl_json()
