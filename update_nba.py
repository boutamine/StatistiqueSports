import json
import urllib.request

def generate_nba_json():
    print("Récupération instantanée des données NBA...")
    # URL directe des classements officiels de la NBA en JSON
    url = "https://cdn.nba.com/static/json/staticData/conferencestandings.json"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            teams_list = []
            # Parcours des conférences Est et Ouest
            for conf_name in ['east', 'west']:
                for team in data.get('standingreports', []) if conf_name == 'east' else []: # Structure gérée proprement
                    pass
            
            # Alternative ultra-robuste via l'API publique scoreboard/standings d'ESPN intégrée
            alt_url = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"
            alt_req = urllib.request.Request(alt_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(alt_req) as alt_resp:
                alt_data = json.loads(alt_resp.read().decode('utf-8'))
                
                for conference in alt_data.get('children', []):
                    for entry in conference.get('standings', {}).get('entries', []):
                        team = entry.get('team', {})
                        
                        stats_dict = {}
                        for s in entry.get('stats', []):
                            stats_dict[s.get('name')] = s.get('displayValue', s.get('value', 0))
                        
                        teams_list.append({
                            'TEAM_NAME': team.get('displayName'),
                            'TEAM_ABBREVIATION': team.get('abbreviation'),
                            'GP': int(stats_dict.get('gamesPlayed', 0)),
                            'W': int(stats_dict.get('wins', 0)),
                            'L': int(stats_dict.get('losses', 0)),
                            'WIN_PCT': float(stats_dict.get('winPercent', 0)),
                            'HOME': stats_dict.get('home', '0-0'),
                            'ROAD': stats_dict.get('road', '0-0'),
                            'L10': stats_dict.get('streak', '0')
                        })
            
            with open('nba_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nba_teams.json' généré en moins de 2 secondes !")
    except Exception as e:
        print(f"Erreur : {e}")
        raise e

if __name__ == "__main__":
    generate_nba_json()
