import json
import urllib.request

def generate_nba_json():
    print("Récupération des données NBA...")
    url = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            teams_list = []
            for conference in data.get('children', []):
                for entry in conference.get('standings', {}).get('entries', []):
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
                        'WIN_PCT': stats_dict.get('winPercent', 0),
                        'HOME': next((s.get('displayValue', '0-0') for s in entry.get('stats', []) if s.get('name') == 'home'), '0-0'),
                        'ROAD': next((s.get('displayValue', '0-0') for s in entry.get('stats', []) if s.get('name') == 'road'), '0-0'),
                        'L10': next((s.get('displayValue', '0') for s in entry.get('stats', []) if s.get('name') == 'streak'), '0')
                    })
            
            with open('nba_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nba_teams.json' généré avec succès !")
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nba_json()
