import pyspark, os
from time import time
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

project_name = "ipl-data-analysis"
project_id = "optimum-attic-383216"

start = time()

spark = SparkSession.builder.appName('generate_stats').getOrCreate()

# IPL matches data
ipl_matches_data_gcs_path = "gs://" + project_name + "/IPL_Matches_2008_2022.parquet"
ipl_matches = spark.read.parquet(ipl_matches_data_gcs_path)

# store matches data into BigQuery table
ipl_matches.write.partitionBy("season").format("bigquery").mode('Overwrite') \
    .option("parentProject", project_id) \
    .option("temporaryGcsBucket",project_name) \
    .option('table', 'ipl_data.matches').save()
# register as table to use as a SQL table using spark
ipl_matches.registerTempTable('matches')

# TEAM Stats
# fetching all matches stats for teams mentioned in team1 column
first_innings_stats = spark.sql("""
select team1 as team, season, count(1) as matches_played, 
sum(CASE
    WHEN winning_team == team1 THEN 1
    ELSE 0
END ) AS matches_won
from matches m
group by team1, season
""")

# fetching all matches stats for teams mentioned in team2 column 
second_innings_stats = spark.sql("""
select team2 as team, season, count(1) as matches_played,
sum(CASE
    WHEN winning_team == team2 THEN 1
    ELSE 0
END ) AS matches_won
from matches m
group by team2, season
""")

teams_stats = first_innings_stats.unionAll(second_innings_stats)
teams_stats = teams_stats.groupBy('team', 'season').sum('matches_played', 'matches_won') \
    .sort('season', ascending=True)
teams_stats = teams_stats.withColumnRenamed('sum(matches_played)', 'matches_played') \
    .withColumnRenamed('sum(matches_won)', 'matches_won')

# writing teams statistics yearwise
teams_stats.write.format("bigquery").mode('Overwrite') \
    .option("parentProject", project_id) \
    .option("temporaryGcsBucket",project_name) \
    .option('table', 'ipl_data.teams_stats').save()

# IPL ball by ball data for every match
ipl_ball_by_ball_data_gcs_path = "gs://" + project_name +  "/IPL_Ball_by_Ball_2008_2022.parquet"
ipl_ball_by_ball = spark.read.parquet(ipl_ball_by_ball_data_gcs_path)

# store scores data into BigQuery table
ipl_ball_by_ball.write.format("bigquery").mode('Overwrite') \
    .option("parentProject", project_id) \
    .option("temporaryGcsBucket",project_name) \
    .option('table', 'ipl_data.scores').save()
# register as table to use as a SQL table using spark
ipl_ball_by_ball.registerTempTable('ball_by_ball')

# JOIN matches data and ball_by_ball data to get info/stats for each ball per each match happened
result = spark.sql("""
select b.id, b.batter, b.batsman_run, b.bowler, b.is_wicket_delivery, dismissal_type, m.season
from ball_by_ball b
join matches m
on b.id = m.id
""")

# BATTING Stats
batting_stats = result.groupBy('season', 'b.batter').sum('batsman_run') \
    .withColumnRenamed("sum(batsman_run)", "runs").sort('season', "runs", ascending=False)

# writing batting statistics yearwise
batting_stats.write.partitionBy("season").format("bigquery").mode('Overwrite') \
    .option("parentProject", project_id) \
    .option("temporaryGcsBucket",project_name) \
    .option('table', 'ipl_data.batting_stats').save()

# BOWLING Stats - but not stored anywhere as of now.
bowling_stats = result.filter(result["dismissal_type"] != "run out").groupBy('season', 'b.bowler') \
    .sum('is_wicket_delivery').withColumnRenamed("sum(is_wicket_delivery)", "wickets") \
    .sort('season', "wickets", ascending=False)

end = time()
print("Total time taken by this job: ", end-start)