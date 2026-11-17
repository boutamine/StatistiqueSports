import json
from nba_api.stats.endpoints import leaguestandings

def generate_nba_standings_json():
    print("Récupération des classements NBA...")
    
    # Récupération via la bibliothèque officielle NBA API
    standings = leaguestandings.LeagueStandings()
    df = standings.get_data_frames()[0]
    
    # Conversion en liste de dictionnaires
    teams_list = df.to_dict(orient='records')
    
    # Sauvegarde dans le fichier JSON attendu par Google Apps Script
    with open('nba_teams.json', 'w', encoding='utf-8') as f:
        json.dump(teams_list, f, ensure_ascii=False, indent=4)
        
    print("Fichier 'nba_teams.json' généré avec succès !")

if __name__ == "__main__":
    generate_nba_standings_json()
