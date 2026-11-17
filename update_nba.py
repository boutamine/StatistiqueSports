import json
import urllib.request

def generate_nba_json():
    print("Récupération des données NBA via le flux direct...")
    url = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"
    
    # En-têtes complets pour simuler un vrai navigateur et éviter tout blocage
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
            for conference in data.get('children', []):
                for entry in conference.get('standings', {}).get('entries', []):
                    team = entry.get('team', {})
                    stats = {s['name']: s['displayValue'] for s in entry.get('stats', [])}
                    raw_stats = {s['name']: s['value'] for s in entry.get('stats', [])}
                    
                    teams_list.append({
                        'TEAM_NAME': team.get('displayName'),
                        'TEAM_ABBREVIATION': team.get('abbreviation'),
                        'GP': raw_stats.get('gamesPlayed', 0),
                        'W': raw_stats.get('wins', 0),
                        'L': raw_stats.get('losses', 0),
                        'WIN_PCT': raw_stats.get('winPercent', 0),
                        'HOME': stats.get('home', '0-0'),
                        'ROAD': stats.get('road', '0-0'),
                        'L10': stats.get('streak', '0')
                    })
            
            with open('nba_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nba_teams.json' généré et sauvegardé avec succès !")
    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        raise e

if __name__ == "__main__":
    generate_nba_json()
