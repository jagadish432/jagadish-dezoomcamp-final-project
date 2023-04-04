import pandas as pd



def fix_season_value(season):
    years = season.split("/")
    return years[0]

def clean_match_data(df):
    """
        cleanse the Matches dataset
    """
    # For the matches dataset, These columns doesn't need to be converted as they're already of String type: Team1, Team2, Venue, TossWinner, TossDecision, SuperOver, WinningTeam, WonBy,
    # method, Player_of_Match, Umpire1, Umpire2, Team1Players, Team2Players

    # renaming the columns to follow snake_case format
    df.columns = [
        'id',
        'city',
        'date',
        'season',
        'match_number',
        'team1',
        'team2',
        'venue',
        'toss_winner',
        'toss_decision',
        'superover',
        'winning_team',
        'won_by',
        'margin',
        'method',
        'player_of_the_match',
        'team1_players',
        'team2_players',
        'umpire1',
        'umpire2'
    ]

    print("columns renamed")
    print(f"rows before match data cleansing: {len(df)}")

    # Converting date values to date time
    df['date'] = pd.to_datetime(df['date'])

    # fixing 'Season' values, few values have 2008/09 so we're converting them to the 2008
    df['season'] = df['season'].apply(fix_season_value)
    df['season'] = df['season'].astype(int)

    # Filling/Replacing the superover decided matches Margin(existing as NA) with -1
    df["margin"].fillna(-1, inplace=True)
    df['margin'] = df['margin'].astype(int)

    df['team1_players'] = df['team1_players'].str.split(",")
    df['team2_players'] = df['team2_players'].str.split(",")

    
    print(f"rows after match data cleansing: {len(df)}")

    return df

def clean_ball_data(df):
    """
        mostly no need to transform anything here as the data looks good, so we will just perform filtering here

        cleanse the balls dataset
        columns and their possible values
        innings = 1,2,3,4 , where 1&2 are normal innings, 3&4 are super over innings
        overs = 0-19 , where 0 is 1st over and 19 is 20th over
        ballnumber = 1-10, possibly can be even>10 if bowler bowls many wides/no-balls/etc..
        batter = name of the bastman on-strike 
        bowler = name of the bowler bowling
        non-striker = name of the batsman on non-strike
        extra_type = type of the extra run i.e., no-ball/wide/penalty/byes/leg-byes/NA where NA is normal run
        bastman_run = 0-6
        extras_run = number of extra runs in the particular ball , 0-7, again could be even more based on the extra ball
        total_run = batsman_run + extras_run
        non_boundary = 0 or 1, 
            1 means all runs scored without an actual boundary/extras (could be overthrow) 
            and 0 means actual boundary if total score is 4/6 otherwise just a run
        isWicketDelivery = 0 or 1, 0 means no wicker and 1 means a wicket
        player_out = name of the batsman who was dismissed (could be striker/non-striker)
        kind = type of dismissal
        fielders_involved = fielders involved in the dismissal
        BattingTeam = name of the batting team the batsman belongs to
    """
    # renaming the columns to follow snake_case format
    df.columns = [
        'id',
        'innings',
        'overs',
        'ball_number',
        'batter',
        'bowler',
        'non_striker',
        'extra_type',
        'batsman_run',
        'extras_run',
        'total_run',
        'non_boundary',
        'is_wicket_delivery',
        'player_out',
        'dismissal_type',
        'fielders_involved',
        'batting_team'
    ]

    print("columns renamed")
    print(f"rows before match data cleansing: {len(df)}")

    # dropping the rows which has N/A for any of the below-mentioned columns
    df = df.dropna(subset=
                   ['id', 'innings', 'overs', 'ball_number', 'batter', 'bowler', 'non_striker',
                    'batsman_run', 'total_run', 'is_wicket_delivery'])

    print(f"rows after match data cleansing: {len(df)}")

    return df





