import json
from nba_api.stats.endpoints import leaguestandings

def generate_nba_standings_json():
    print("Récupération des classements NBA complets (Domicile/Extérieur)...")
    
    # Appel de l'endpoint officiel
    standings = leaguestandings.LeagueStandings(timeout=30)
    df = standings.get_data_frames()[0]
    
    teams_list = []
    for _, row in df.iterrows():
        # Les colonnes Home et Road renvoient directement des formats type "8-2" ou similaire dans nba_api
        home_record = row.get('HOME', '0-0')
        road_record = row.get('ROAD', '0-0')
        
        teams_list.append({
            'TEAM_NAME': row.get('TeamName'),
            'TEAM_ABBREVIATION': row.get('TeamAbbreviation'),
            'GP': int(row.get('GP', 0)),
            'W': int(row.get('W', 0)),
            'L': int(row.get('L', 0)),
            'WIN_PCT': float(row.get('WIN_PCT', 0)),
            'HOME': home_record,
            'ROAD': road_record,
            'L10': row.get('L10', '0')
        })
    
    # Sauvegarde du fichier JSON mis à jour
    with open('nba_teams.json', 'w', encoding='utf-8') as f:
        json.dump(teams_list, f, ensure_ascii=False, indent=4)
        
    print("Fichier 'nba_teams.json' généré avec succès avec les stats Domicile/Extérieur !")

if __name__ == "__main__":
    generate_nba_standings_json()
