import json
from nba_api.stats.endpoints import leaguestandings

def generate_nba_standings_json():
    print("Récupération des classements NBA via nba_api...")
    
    # Appel de l'endpoint officiel de la bibliothèque nba_api
    standings = leaguestandings.LeagueStandings(timeout=30)
    df = standings.get_data_frames()[0]
    
    # Conversion du DataFrame en dictionnaire JSON propre
    teams_list = df.to_dict(orient='records')
    
    # Sauvegarde du fichier JSON
    with open('nba_teams.json', 'w', encoding='utf-8') as f:
        json.dump(teams_list, f, ensure_ascii=False, indent=4)
        
    print("Fichier 'nba_teams.json' généré avec succès !")

if __name__ == "__main__":
    generate_nba_standings_json()
