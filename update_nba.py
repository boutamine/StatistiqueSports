import json
import urllib.request

def generate_nba_json():
    print("Récupération des données NBA avec les détails Domicile/Extérieur...")
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
                    
                    # Dictionnaire pour stocker les stats par leur nom
                    stats_dict = {}
                    display_stats = {}
                    
                    for s in entry.get('stats', []):
                        name = s.get('name')
                        stats_dict[name] = s.get('value', 0)
                        display_stats[name] = s.get('displayValue', '0-0')
                        
                    teams_list.append({
                        'TEAM_NAME': team.get('displayName'),
                        'TEAM_ABBREVIATION': team.get('abbreviation'),
                        'GP': int(stats_dict.get('gamesPlayed', 0)),
                        'W': int(stats_dict.get('wins', 0)),
                        'L': int(stats_dict.get('losses', 0)),
                        'WIN_PCT': float(stats_dict.get('winPercent', 0)),
                        # Extraction correcte des stats Domicile et Extérieur d'ESPN
                        'HOME': display_stats.get('home', display_stats.get('Home', '0-0')),
                        'ROAD': display_stats.get('road', display_stats.get('Away', display_stats.get('roadRecord', '0-0'))),
                        'L10': display_stats.get('streak', display_stats.get('L10', '0'))
                    })
            
            with open('nba_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nba_teams.json' généré et forcé avec succès !")
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nba_json()
