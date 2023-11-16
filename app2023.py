import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# if __name__ =='__main__':

#pandas
ball=pd.read_csv('each_ball_records.csv')
ball.iloc[17858:,2] = 1
match=pd.read_csv('each_match_records.csv')
total_match=pd.merge(ball,match,left_on="match_no",right_on="match_number")
# total_match['date'] = pd.to_datetime(total_match['date'])
total_match['season'] = total_match['season'].astype(np.int32)
total_match['score'] = total_match['score'].astype(np.int32)
total_match['match_no'] = total_match['match_no'].astype(np.int32)
total_match['ballnumber'] = total_match['ballnumber'].astype(np.int32)
total_match['inningno'] = total_match['inningno'].astype(np.int8)
total_match['match_number'] = total_match['match_number'].astype(np.int32)
# total_match = total_match.drop(columns=['comment'])
# total_match['winner_wickets']=total_match['winner_wickets'].astype(np.int32)

def ipl2023data():
    st.sidebar.title('*Ipl 2023 Analysis*')
    select_first_option=st.sidebar.selectbox('Choose any one option',['Overall Analysis','Team Analysis','Team Vs Team'])

    if select_first_option=='Overall Analysis':

        total_no_match = total_match['match_no'].unique().max()
        league_match = match[match['match_type'] == 'Group'].shape[0]
        playoff_match = total_no_match - league_match


        st.header('*Overall Analysis of 2023 IPL*')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Matches",total_no_match)
        with col2:
            st.metric("League Matches",league_match)
        with col3:
            st.metric("Playoff Matches", playoff_match)



        final_match_details = total_match[total_match['match_type'] == 'Final'].sort_values(by=['inningno', 'over'],ascending=[True, True])
        first_inning_team_details = final_match_details[final_match_details['inningno'] == 1]
        second_inning_team_details = final_match_details[final_match_details['inningno'] == 2]
        final_match_details['date'] = pd.to_datetime(final_match_details['date'],yearfirst=True)
        dayname = final_match_details['date'].dt.day_name().unique()[0]
        final_match_details['date'] = final_match_details['date'].dt.date
        team1 = final_match_details['team1'].unique()[0]
        team2 = final_match_details['team2'].unique()[0]
        date = final_match_details['date'].unique()[0]
        toss_winner = final_match_details['toss_won'].unique()[0]
        toss_decision = final_match_details['toss_decision'].unique()[0]
        match_type = final_match_details['match_type'].unique()[0]
        venue = final_match_details['venue'].unique()[0]
        location = final_match_details['location'].unique()[0]
        man_of_match = final_match_details['man_of_match'].unique()[0]
        over2 = second_inning_team_details['over'].nunique() / 6
        over1 = first_inning_team_details['over'].nunique() / 6
        umpire1 = final_match_details['umpire1'].unique()[0]
        umpire2 = final_match_details['umpire2'].unique()[0]
        reserve_umpire = final_match_details['reserve_umpire'].unique()[0]
        match_refree = final_match_details['match_referee'].unique()[0]
        winner = final_match_details['winner'].unique()[0]
        winsbyruns = final_match_details['winner_runs'].unique()[0]
        winsbywicket = final_match_details['winner_wickets'].unique()[0]
        run1_inn = first_inning_team_details['score'].sum()
        run2_inn = second_inning_team_details['score'].sum()
        wicket1_inn = (first_inning_team_details['outcome'] == 'w').sum()
        wicket2_inn = (second_inning_team_details['outcome'] == 'w').sum()


        def batting_decision(toss_winner, toss_decision):
            if (toss_winner == team1 and toss_decision == 'field') or (
                    toss_winner == team2 and toss_decision == 'bat'):
                batting1_team = team2
                batting2_team = team1
                return (batting1_team, batting2_team)
            else:
                batting1_team = team1
                batting2_team = team2
                return (batting1_team, batting2_team)

        batting1_team,batting2_team=batting_decision(toss_winner,toss_decision)

        st.header('*Final Match Details*')
        st.subheader(f"{batting1_team} {run1_inn}-{wicket1_inn}({over1} ov) VS {batting2_team} {run2_inn}-{wicket2_inn}({over2} ov) , {match_type} match")
        # st.subheader(f'{batting1_team} ( {run1_inn}/{wicket1_inn} )')
        # st.subheader(f'{batting2_team} ( {run2_inn}/{wicket2_inn} )')
        l=[["Date of match",f"{date},{dayname}"],
           ["Toss Winner",f'{toss_winner} won the toss'],
           ['Toss Decision',toss_decision.capitalize()],
           ['Winner',f'{winner} won (D/L)'],
           ['Man of the Match',man_of_match],
           ["Umpire1",umpire1],
           ['Umpire2',umpire2],
           ["Reserve umpire",reserve_umpire],
           ["Match refree",match_refree],
           ["Venue",f'{venue}, {location}']]

        df=pd.DataFrame(l,columns=['Match Information',""])
        st.dataframe(df,use_container_width=True,hide_index=True)

        stadium_names = (total_match['venue'] + "," + total_match["location"]).reset_index().drop_duplicates(subset=[0]).drop(columns=['index']).rename(columns={0: "Stadium Name"}).sort_values(by='Stadium Name')
        no_of_stadium = stadium_names.shape[0]
        venue_count = (match['venue'] + "," + match['location']).value_counts().sort_index().reset_index()
        stadium_name_count = pd.merge(left=stadium_names, right=venue_count, left_on='Stadium Name',right_on="index").drop(columns=['index']).rename(columns={'count':f"Number of matches ({total_no_match})"}).sort_values(by=f'Number of matches ({total_no_match})',ascending=False)

        st.subheader("List of all the stadium where Ipl played in 2023")
        st.dataframe(stadium_name_count,use_container_width=True,hide_index=True)

        st.subheader("Most of the time the player of the match award goes to")
        man_of_match_df = match['man_of_match'].value_counts().head().reset_index().rename(columns={'man_of_match':"Man of the match",'count':"Times"})
        st.dataframe(man_of_match_df,use_container_width=True,hide_index=True)


        st.subheader('List of Top players scoring 500 above runs in IPL')
        no_balls_match = total_match[total_match['outcome'].str.contains('nb')]
        num_of_no_balls = no_balls_match['batter'].value_counts().sort_values(ascending=False)
        no_balls_score_by_player = no_balls_match.groupby('batter')['score'].sum().sort_values(ascending=False)
        no_ball_runs = (no_balls_score_by_player - num_of_no_balls).reset_index().rename(columns={0: 'noball_count_runs'})
        without_noball_runs = total_match[total_match['outcome'].str.isdigit()].groupby('batter')['score'].sum().sort_values(ascending=False).reset_index()
        total_ipl_runs = pd.merge(without_noball_runs, no_ball_runs, how='left', on='batter')
        total_ipl_runs = total_ipl_runs.fillna(0)
        total_ipl_runs['total_score'] = total_ipl_runs['score'] + total_ipl_runs['noball_count_runs']
        total_ipl_runs.sort_values(by='total_score', ascending=False, inplace=True)
        highest_run_player = total_ipl_runs[total_ipl_runs['total_score'] > 500]
        highest_run_player = highest_run_player[['batter', 'total_score']].rename(columns={'batter': 'Batter', 'total_score': 'Total Score'})
        st.dataframe(highest_run_player,use_container_width=True,hide_index=True)


        max_six_player = total_match[total_match['outcome'].isin(['6', '7nb'])]['batter'].value_counts().reset_index().rename(columns={'batter': 'Batter', 'count': 'Number of sixes'})
        max_six_player=max_six_player[max_six_player['Number of sixes']>=25]
        st.subheader("Most number of sixes by")
        st.dataframe(max_six_player,use_container_width=True,hide_index=True)

        max_four_player = total_match[total_match['outcome'].isin(['4', '5nb'])]['batter'].value_counts().reset_index().rename(columns={'batter': 'Batter', 'count': 'Number of fours'})
        max_four_player = max_four_player[max_four_player['Number of fours'] >= 50]
        st.subheader('Most number of fours by')
        st.dataframe(max_four_player,use_container_width=True,hide_index=True)

        st.subheader('Most wicket taker in IPL')
        runout = total_match[total_match['comment'].str.contains('Wicket - runout')]['bowler'].value_counts().reset_index()
        l = []
        for name, value in total_match.groupby('bowler'):
            wicket = sum(value['outcome'].isin(['w']))
            l.append([name, wicket])
        wicket_total = pd.DataFrame(l).rename(columns={0: "bowler", 1: "number of wicket"})
        temp_df = pd.merge(wicket_total, runout, on="bowler", how='left')
        temp_df.fillna(0, inplace=True)
        temp_df['count'] = temp_df['count'].astype(np.int32)
        temp_df['actual wicket'] = temp_df['number of wicket'] - temp_df['count']
        temp_df=temp_df.drop(columns=['number of wicket', 'count']).sort_values(by='actual wicket', ascending=False).rename(columns={'bowler': "Bowler", 'actual wicket':'Number of wickets'})
        temp_df=temp_df[temp_df['Number of wickets']>18]
        st.dataframe(temp_df,use_container_width=True,hide_index=True)
        st.subheader("Most number of sixes in certain over")
        option = st.selectbox(
            'Sixes in last how many overs?',
            ('Select',1,2,3,4,5))
        if option!='Select':
            over=(20-option)+0.1
            temp_df=total_match[(total_match['over'] >= over) & (total_match['outcome'].isin(['6', '7nb']))]['batter'].value_counts().head().reset_index().rename(columns={'batter': 'Batter', 'count': f'Number of sixes in last {option} overs'})

            st.dataframe(temp_df,use_container_width=True,hide_index=True)

        st.subheader("Most numbers of wicket taker in certain overs")
        option = st.selectbox(
            'Wickets in last how many overs?',
            ('Select', 1, 2, 3, 4, 5))
        if option != 'Select':
            over = (20 - option) + 0.1
            temp_df=total_match[(total_match['over'] >= over) & (total_match['outcome'].isin(['w'])) & (~(total_match['comment'].str.contains('Wicket - runout')))]['bowler'].value_counts().head().reset_index().rename(columns={'bowler':'Bowler','count':f'Number of wickets taken in last {option} overs'})

            st.dataframe(temp_df,use_container_width=True,hide_index=True)

        first_inning_team_details = total_match[total_match['inningno'] == 1]
        second_inning_team_details = total_match[total_match['inningno'] == 2]
        no_ball_1_score =first_inning_team_details[first_inning_team_details['outcome'].str.contains('nb')].groupby('batter')['score'].sum().sort_index()
        no_ball_2_score =second_inning_team_details[second_inning_team_details['outcome'].str.contains('nb')].groupby('batter')['score'].sum().sort_index()
        no_ball_2_played = second_inning_team_details[second_inning_team_details['outcome'].str.contains('nb')]['batter'].value_counts().sort_index()
        no_ball_1_played = first_inning_team_details[first_inning_team_details['outcome'].str.contains('nb')]['batter'].value_counts().sort_index()
        no_ball_actual_score_1 = (no_ball_1_score - no_ball_1_played).reset_index()
        no_ball_actual_score_2 = (no_ball_2_score - no_ball_2_played).reset_index()
        total_2_wihtout_no_ball_scored =second_inning_team_details[second_inning_team_details['outcome'].str.isdigit()].groupby('batter')['score'].sum().sort_index().reset_index()
        total_1_wihtout_no_ball_scored =first_inning_team_details[first_inning_team_details['outcome'].str.isdigit()].groupby('batter')['score'].sum().sort_index().reset_index()
        proper_df = pd.merge(total_1_wihtout_no_ball_scored, no_ball_actual_score_1, how='left', on='batter').fillna(0)
        proper_df['score'] = proper_df['score'] + proper_df[0]
        proper_df.drop(columns=[0], inplace=True)
        proper_df=proper_df.sort_values(by='score', ascending=False).head(10)

        st.subheader("Players who scored most of the run during 1st inning")

        st.dataframe(proper_df,use_container_width=True,hide_index=True)

        proper_df_2 = pd.merge(total_2_wihtout_no_ball_scored, no_ball_actual_score_2, how='left',on='batter').fillna(0)
        proper_df_2['score'] = proper_df_2['score'] + proper_df_2[0]
        proper_df_2.drop(columns=[0], inplace=True)
        proper_df_2=proper_df_2.sort_values(by='score', ascending=False).head(10)

        st.subheader("Players who scored most of the run during 2nd inning (chasing)")
        st.dataframe(proper_df_2,use_container_width=True,hide_index=True)

        dummy = total_match.copy()
        dummy = dummy.reset_index()
        temp_dummy = dummy[dummy['outcome'].str.isdigit()][['index', 'score']].rename(columns={'score': 'actual score'})
        dummy1 = pd.merge(dummy, temp_dummy, how='left', on='index')
        dummy1['actual score'] = dummy1['actual score'].fillna(0)

        dummy2 = dummy1[dummy1['outcome'].str.contains('nb')][['index', 'outcome']]
        dummy2['no_ball_runs'] = dummy2['outcome'].str[0]
        dummy2['no_ball_runs'] = dummy2['no_ball_runs'].astype(np.int32)
        dummy2['no_ball_runs'] = dummy2['no_ball_runs'] - 1
        dummy2 = dummy2.drop(columns=['outcome'])

        dummy3 = pd.merge(dummy1, dummy2, how='left', on='index')
        dummy3['no_ball_runs'] = dummy3['no_ball_runs'].fillna(0)
        dummy3['actual score'] = dummy3['actual score'] + dummy3['no_ball_runs']
        dummy3['actual score'] = dummy3['actual score'].astype(np.int32)
        dummy3['no_ball_runs'] = dummy3['no_ball_runs'].astype(np.int32)


        dummy3_1_inning = dummy3[dummy3['inningno'] == 1]
        dummy3_2_inning = dummy3[dummy3['inningno'] == 2]

        def batting_decision(team1, team2, toss_winner, toss_decision):
            if (toss_winner == team1 and toss_decision == 'field') or (
                    toss_winner == team2 and toss_decision == 'bat'):
                batting1_team = team2
                batting2_team = team1
                return (batting1_team, batting2_team)
            else:
                batting1_team = team1
                batting2_team = team2
                return (batting1_team, batting2_team)

        l = []
        for key, values in dummy3_1_inning.groupby(['match_number', 'team1', 'team2']):
            batting1_team, batting2_team = batting_decision(values['team1'].unique()[0],values['team2'].unique()[0],values['toss_won'].unique()[0],values['toss_decision'].unique()[0])
            l.append([key[0], batting1_team, batting2_team, values['score'].sum()])
        temp_df1 = pd.DataFrame(l, columns=['Match number', 'Target giving team', 'Target chasing team','Target given'])
        st.subheader('Max Target giving team')
        st.dataframe(temp_df1.sort_values(by='Target given',ascending=False).head(10),use_container_width=True,hide_index=True)


        l = []
        for key, values in dummy3_2_inning.groupby(['match_number', 'team1', 'team2']):
            batting1_team, batting2_team = batting_decision(values['team1'].unique()[0],
                                                            values['team2'].unique()[0],
                                                            values['toss_won'].unique()[0],
                                                            values['toss_decision'].unique()[0])
            l.append([key[0], batting1_team, batting2_team, values['score'].sum()])
        temp_df2 = pd.DataFrame(l, columns=['Match number', 'Target chasing team', 'Target giving team','Target chased'])
        d1 = pd.merge(temp_df1, temp_df2, on=['Match number']).drop(
            columns=['Target chasing team_y', 'Target giving team_y']).rename(
            columns={'Target giving team_x': 'Target giving team', 'Target chasing team_x': 'Target chasing team'})
        d2 = d1[d1['Target chased'] > d1['Target given']].sort_values(by='Target chased', ascending=False).head(
            10).drop(columns=['Match number'])
        st.subheader('Max target chased team')
        st.dataframe(d2,use_container_width=True,hide_index=True)









































        # final_match_winner = match[match['match_type'] == 'Final']
        # season = final_match_winner['season'].values[0]
        # date = final_match_winner['date'].values[0]
        # venue = final_match_winner['venue'].values[0]
        # location = final_match_winner['location'].values[0]
        # winner = final_match_winner['winner'].values[0]
        # name = ""
        # for i in winner.split(" "):
        #     name = name + (i[0])
        # winsbywicket = int(final_match_winner.loc[:, 'winner_wickets'].values[0])
        # team1 = final_match_winner['team1'].values[0]
        # firstteam=""
        # for i in team1.split(" "):
        #     firstteam = firstteam + (i[0])
        # team2 = final_match_winner['team2'].values[0]
        # secteam = ""
        # for i in team2.split(" "):
        #     secteam = secteam + (i[0])
        #
        # final_match = total_match[total_match['match_type'] == 'Final'].sort_values(by=['inningno', 'over'],ascending=True)
        # grp_final = final_match.groupby('inningno')
        # l=[]
        # for key, i in grp_final:
        #     l.append([key,len(i[i['outcome'] == 'w'])])
        # toss_decision = final_match['toss_decision'].unique()[0]
        # toss_won = final_match['toss_won'].unique()[0]
        # if (((toss_won == team2) & (toss_decision == 'field')) | ((toss_won == team1) & (toss_decision == 'bat'))):
        #     # team1 will play
        #     score1=grp_final['score'].sum()[1]
        #     score2=grp_final['score'].sum()[2]
        #     print(score1,score2)
        # else:
        #     score2=grp_final['score'].sum()[1]
        #     score1=grp_final['score'].sum()[2]
        # st.header(f'Final Competitor')
        # st.subheader(f"*{team2} {score2}/{l[0][1]}*")
        # st.subheader(f"*{team1} {score1}/{l[1][1]}*")
        # st.write('D/L method apply')
        #
        # m=[["Date",date],['Winner',winner],["Wins by",str(winsbywicket)+" wicket"],["Venue",venue]]
        # df=pd.DataFrame(m,columns=["Match Information",""])
        # st.dataframe(df,use_container_width=True,hide_index=True)
        # # col1, col2, col3 = st.columns(3)
        # # with col1:
        # #     st.metric('Season',season)
        # # with col2:
        # #     pass
        # # with col3:
        # #     st.metric("Date", date)
        # # col4,col5, col6 = st.columns(3)
        # # with col4:
        # #     st.metric("Winner", name)
        # # with col5:
        # #     pass
        # # with col6:
        # #     st.metric("Wins by",f"{winsbywicket} wickets")
        # # st.metric("Venue",f'{venue}, {location}')



# ipl2023data()