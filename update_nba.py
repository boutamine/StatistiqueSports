import json
import time
from nba_api.stats.endpoints import leaguestandings

def generate_nba_standings_json():
    print("Récupération des classements NBA avec délai étendu...")
    
    # Tentative avec gestion d'essai / erreur et timeout étendu
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # On instancie les classements de la ligue
            standings = leaguestandings.LeagueStandings(timeout=60)
            df = standings.get_data_frames()[0]
            
            teams_list = df.to_dict(orient='records')
            
            with open('nba_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams_list, f, ensure_ascii=False, indent=4)
                
            print("Fichier 'nba_teams.json' généré avec succès !")
            return
        except Exception as e:
            print(f"Tentative {attempt + 1} échouée : {e}")
            if attempt < max_retries - 1:
                print("Nouvelle tentative dans 5 secondes...")
                time.sleep(5)
            else:
                print("Échec définitif après plusieurs tentatives.")
                raise e

if __name__ == "__main__":
    generate_nba_standings_json()
