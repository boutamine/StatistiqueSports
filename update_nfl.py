import json
import urllib.request

def generate_nfl_json():
    print("Début du script de récupération NFL...")
    url = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*'
        }
    )
    
    try:
        print(f"Connexion à l'URL : {url}")
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
            print(f"Réponse reçue, taille : {len(raw_data)} caractères.")
            
            data = json.loads(raw_data)
            teams_list = []
            
            conferences = data.get('children', [])
            print(f"Nombre de conférences trouvées : {len(conferences)}")
            
            for conf in conferences:
                entries = []
                # Pour la NFL, les équipes sont directement dans conf['standings']['entries']
                if 'standings' in conf and 'entries' in conf['standings']:
                    entries = conf['standings']['entries']
                # Sécurité au cas où il y aurait des divisions imbriquées
                elif 'children' in conf:
                    for div in conf.get('children', []):
                        if 'standings' in div and 'entries' in div['standings']:
                            entries.extend(div['standings']['entries'])
                
                print(f" Conférence {conf.get('name')} -> {len(entries)} équipes trouvées.")
                
                for entry in entries:
                    team = entry.get('team', {})
                    team_name = team.get('displayName', 'Inconnu')
                    
                    stats_dict = {}
                    display_stats = {}
                    
                    for s in entry.get('stats', []):
                        name = s.get('name')
                        stats_dict[name] = s.get('value', 0)
                        display_stats[name] = s.get('displayValue', s.get('summary', '0-0'))
                    
                    home_val = display_stats.get('Home', display_stats.get('home', '0-0'))
                    road_val = display_stats.get('Road', display_stats.get('road', display_stats.get('Away', display_stats.get('away', '0-0'))))
                    streak_val = display_stats.get('streak', '0')
                    
                    teams_list.append({
                        'TEAM_NAME': team_name,
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
            
            print(f"Total équipes traitées : {len(teams_list)}")
            
            with open('nfl_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nfl_teams.json' écrit avec succès.")
            
    except Exception as e:
        print(f"ERREUR CRITIQUE DANS LE SCRIPT : {e}")
        raise e

if __name__ == "__main__":
    generate_nfl_json()
