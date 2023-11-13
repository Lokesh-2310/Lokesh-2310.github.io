#importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


#analysis code
ipl=pd.read_csv("IPL Matches 2008-2020.csv")
ipl=ipl.replace(['Rising Pune Supergiants','Delhi Daredevils','M Chinnaswamy Stadium','Punjab Cricket Association Stadium, Mohali','Bengaluru'],['Rising Pune Supergiant','Delhi Capitals','M.Chinnaswamy Stadium','Punjab Cricket Association IS Bindra Stadium, Mohali','Bangalore'])
ipl['date']=pd.to_datetime(ipl['date'])
ipl['year']=ipl['date'].dt.year


#filling null values
values=ipl[(ipl['city'].isnull()) & (ipl['venue']=='Sharjah Cricket Stadium')].index
ipl.loc[values,'city']='Sharjah'
values=ipl[(ipl['city'].isnull()) & (ipl['venue']=='Dubai International Cricket Stadium')].index
ipl.loc[values,'city']='Dubai'


#citywise analysis
city_list=ipl['city'].unique().tolist()
city_list.insert(0,'Select')
list_of_team=list(np.union1d(ipl['team1'],ipl['team2']))
list_of_team.insert(0,'Select')


#Websitecode
st.set_page_config(page_title='IPL|2008-2020|Analysis',layout='wide')
st.sidebar.title("Cricket Analysis")


#option selection
option1 = st.sidebar.selectbox(
        'Choose option',
        ['Select','Citywise Record','Team Vs Team Record']
    )


#Select option code-
if option1=='Select':
    st.title('About Indian Premier League (IPL)')
    st.image('images-videos/iplit.png')
    st.write(""" Indian Premier League (IPL), Indian professional Twenty20 (T20) cricket league established in 2008. The league, which is based on a round-robin group and knockout format, has teams in major Indian cities.
    The brainchild of the Board of Control for Cricket in India (BCCI), the IPL has developed into the most lucrative and most popular outlet for the game of cricket. Matches generally begin in late afternoon or evening so that at least a portion of them are played under floodlights at night to maximize the television audience for worldwide broadcasts. Initially, league matches were played on a home-and-away basis between all teams, but, with the planned expansion to 10 clubs (divided into two groups of five) in 2011, that format changed so that matches between some teams would be limited to a single encounter. The top four teams contest three play-off matches, with one losing team being given a second chance to reach the final, a wrinkle aimed at maximizing potential television revenue. The play-off portion of the tournament involves the four teams that finished at the top of the tables in a series of knockout games that allows one team that lost its first-round game a second chance to advance to the final match.
    With the advent of the IPL, almost overnight the world’s best cricketers—who had seldom made the kind of money earned by their counterparts in other professional sports—became millionaires. The owners of the IPL franchises, who included major companies, Bollywood film stars, and media moguls, bid for the best players in auctions organized by the league. At the outset of the IPL, the well-financed Mumbai Indians had the league’s biggest payroll, more than 100 million dollar. It cost the Chennai Super Kings 1.5 million dollar to secure the services of Mahendra Dhoni in the initial auction for the 2008 season and the Kolkata Knight Riders 2.4 million dollar to sign Gautam Gambhir, the opening batsman for the Indian national team, in the bidding for the 2011 season.

The eight founding franchises were the Mumbai Indians, the Chennai Super Kings, the Royal Challengers Bangalore, the Deccan Chargers (based in Hyderabad), the Delhi Daredevils, the Punjab XI Kings (Mohali), the Kolkata Knight Riders, and the Rajasthan Royals (Jaipur). In late 2010 two franchises, Rajasthan and Punjab, were expelled from the league by the BCCI for breeches of ownership policy, but they were later reinstated in time for the 2011 tournament. Two new franchises, the Pune Warriors India and the Kochi Tuskers Kerala, joined the IPL for the 2011 tournament. The Kochi club played just one year before the BCCI terminated its contract. In 2013 the Deccan Chargers were replaced in the IPL by the Sunrisers Hyderabad.

The first tournament, held over 44 days in 2008, was won by the Rajasthan Royals, one of the smaller-market franchises, captained by Shane Warne, the great Australian bowler. In the wake of the IPL’s success, other cricketing countries scrambled to grab some of the riches by forming their own domestic T20 leagues.
    """)
    st.subheader('Teams in IPL')

    col1,col2=st.columns(2)
    with col1:
        st.image('images-videos/csk.png')
    with col2:
        st.write('CSK Full Form: CSK stands for Chennai Super Kings, it is also known as the Yellow Army. CSK is known to be one of the fan favourite teams of IPL. CSK is led by MS Dhoni with fellow players like Suresh Raina, Ravindra Jadeja and many others.CSK is known to be a tough competition for other teams in the IPL tournament and is the team with the most winning titles. CSK franchise is based in Tamil Nadu, it plays all the games at the MS Chidambaram Stadium located in Chennai. Apart from being a constant winner at IPL, CSK is believed to have appeared a maximum number of times in the finals and semi-finals alongside the other IPL team. ')

    col1,col2=st.columns(2)
    with col1:
        st.image('images-videos/dc.png',width=380)
    with col2:
        st.write("Delhi Capitals (formerly Delhi Daredevils) are a professional franchise cricket team based in Delhi that plays in the Indian Premier League (IPL). The franchise is jointly owned by the GMR Group and the JSW Sports. The team's home ground is Arun Jaitley Stadium (formerly Feroz Shah Kotla), located in New Delhi. The team is coached by Ricky Ponting. The Capitals appeared in their first IPL final in 2020 against Mumbai Indians.In December 2018, the team changed its name from the Delhi Daredevils to the Delhi Capitals.[5] Speaking to the rationale behind changing the team's name, co-owner and chairman Parth Jindal said,Delhi is the power centre of the country, it is the capital, therefore the name Delhi Capitals.Co-owner Kiran Kumar Grandhi said,The new name symbolizes Delhi's identity and just like the city, we are aiming to be the centre of all action going forward.")


#Select citywise option code
if option1=='Citywise Record':

    city_choose= st.sidebar.selectbox('Choose any one city ',city_list)
    if city_choose!='Select':
        city_sel = city_choose
        temp_ipl = ipl[ipl['city'] == city_sel]


        #match occured
        match_happ = temp_ipl.shape[0]
        st.title(city_sel+" City Match Analysis")
        st.subheader('Total matched played in '+city_sel+' : ' +str(match_happ))


        #neutral venue
        if (((temp_ipl['neutral_venue'] == 1).any())==True):
            st.subheader(" :star: It's a neutral venue ! :star:")


        #stadium
        stadium_no = temp_ipl['venue'].nunique()
        st.subheader(f"Number of stadium in {city_sel} where IPL played : {stadium_no}")

        #List of stadium->
        st.subheader("*List of all the :cricket_bat_and_ball: stadium*")
        stadium_name = temp_ipl['venue'].unique()
        df = pd.DataFrame(stadium_name,columns=['Stadium Name'])
        st.dataframe(df,use_container_width=True,hide_index=True)

        #Table of count
        st.subheader(f"*What teams prefer in {city_sel} after winning the toss*")
        counts = temp_ipl['toss_decision'].value_counts().reset_index().rename(columns={'toss_decision':'Toss decision','count':'Count'})
        st.dataframe(counts,use_container_width=True,hide_index=True)

        #table of matches
        st.subheader(f"Count of matches in particular year (in {city_sel})")
        df=temp_ipl['year'].value_counts().sort_index().reset_index()
        s = df.style.format({"Expense": lambda x: '{:.4f}'.format(x)})
        st.dataframe(s,use_container_width=True,hide_index=True)

        #Team wins by which
        st.subheader(f'Count of teams win by (in {city_sel})')
        df=temp_ipl[~(temp_ipl['result'] == 'tie')]['result'].value_counts().reset_index().rename(columns={'result':'Result','count':'Count'})
        st.dataframe(df,use_container_width=True,hide_index=True)


        #Tie match
        match_tie_df = temp_ipl[temp_ipl['result'] == 'tie'][['date', 'venue', 'team1', 'team2']].rename(columns={'date':'Date (yy-mm-dd)','venue':'Venue','team1':'Team1','team2':'Team2'})
        if ((match_tie_df.shape[0]) !=0):
            st.subheader(f'Number of Match tie in {city_sel} : ' + str(match_tie_df.shape[0]))
            st.dataframe(match_tie_df,use_container_width=True,hide_index=True)

        #d/l rule
        df=temp_ipl[temp_ipl['method'] == 'D/L'][['date','team1','team2','winner']].rename(columns={'date':'Date (yy-mm-dd)','winner':'Winner','team1':'Team1','team2':'Team2'})
        if df.shape[0]!=0:
            st.subheader(f"Duckworth–Lewis–Stern (D/L) method in following matches (in {city_sel}) ")
            st.dataframe(df,use_container_width=True,hide_index=True)
        #Graph1
        st.subheader(f"Visualizing Cricket Stats in {city_sel}")
        col1,col2=st.columns(2)
        with col1:
            st.write('*Visualizing by plotting graph*')
            fig=px.histogram(temp_ipl,x='toss_decision',opacity=0.8,labels={'toss_decision':'Toss decision'})
            st.plotly_chart(fig, use_container_width=True,opacity=0.1)

        #Graph2
        with col2:
            st.write(f'*Matches in particular year in {city_sel}*')
            fig = px.histogram(temp_ipl, x='year', nbins=20,labels={'year':'Year'})
            st.plotly_chart(fig,use_container_width=True)

    else:
        st.header("Images of some of the India's Stadium")
        col1, col2,col3 = st.columns(3)
        with col1:
            st.image('images-videos/ipl.jpg', caption='Wankhede Stadium,Navi Mumbai')
        with col2:
            st.image('images-videos/smsstad.jpg',caption='Sawai Mansingh Stadium,Jaipur')
        with col3:
            st.image('images-videos/1280px-D_Y_Patil_Sports_Stadium.jpg',caption='DY Patil Stadium,Navi Mumbai')

        col1, col2,col3 = st.columns(3)
        with col1:
            st.image('images-videos/Brabourne.jpg',caption='Brabourne Stadium,Mumbai')
        with col2:
            st.image('images-videos/Arun_Jaitley_Stadium_during_World_Cup_2023.jpg',caption="Feroz Shah Kotla Stadium (renamed as Arun Jaitley Stadium),Delhi")
        with col3:
            st.image('images-videos/nms.jpg',caption='Narendra Modi Stadium,Ahmedabad')


#Team vs team select code
if option1=='Team Vs Team Record':

    #choose team1 and team2
    team1=st.sidebar.selectbox('Choose Team1',list_of_team)
    team2=st.sidebar.selectbox('Choose Team2',list_of_team)

    #choose dataframe according to condition-
    temp_ipl = ipl[((ipl['team1'] == team1) | (ipl['team1'] == team2)) & ((ipl['team2'] == team2) | (ipl['team2'] == team1))]

    if ((team1=='Select') or (team2=='Select')):
        st.header('Gallery of some IPL matches')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image('images-videos/dcvssrh.jpg', caption='SRH vs DC')
        with col2:
            st.image('images-videos/mivscsk.jpg',caption='MI vs CSK')
        with col3:
            st.image('images-videos/rrvsrcb.jpg',caption='RR vs RCB')

    elif (team1==team2):
        st.header(f"""Choose one different team""")

    else:
        st.header(f""" "{team1.title()}"  vs "{team2.title()}" """)
        df_ipl = temp_ipl[['city', 'date', 'winner']].rename(columns={'city': 'City', 'date': 'Date (yy-mm-dd)', 'winner': 'Winner'}).sort_values(by='Winner')
        if(df_ipl.shape[0]==0):
            st.subheader("No match found between this teams!")

        else:
            #main code for teamvsteam
            #list of matches
            match_happ=df_ipl.shape[0]
            st.subheader('The number of matches : '+str(match_happ))
            df = temp_ipl[temp_ipl['result'] == 'tie']
            if (df.shape[0] != 0):
                st.subheader('The number of tie match : ' + str(df.shape[0]))

            #
            st.subheader('List of Matches')
            st.dataframe(df_ipl, use_container_width=True, hide_index=True)

            #
            if (df.shape[0] != 0):
                st.subheader('List of Tie Match')
                st.dataframe(df[['city','date','venue']].rename(columns={'city':'City','date':'Date (yy-mm-dd)','venue':'Venue'}),use_container_width=True,hide_index=True)

            df=temp_ipl['toss_winner'].value_counts().reset_index().rename(columns={'toss_winner':'Toss Winner','count':'Count'}).sort_values(by='Toss Winner')
            st.subheader('Count of Toss wins')
            st.dataframe(df,use_container_width=True,hide_index=True)

            st.subheader('Wins by')
            l = []
            for i, key in temp_ipl.groupby(['toss_winner', 'toss_decision']):
                l.append([i[0], i[1], len(key)])
            winsby_df = pd.DataFrame(l, columns=['Team', 'Wins by', 'Count'])
            st.dataframe(winsby_df,use_container_width=True,hide_index=True)


            #d/l method
            df_method= temp_ipl[temp_ipl['method'] == 'D/L'][['city', 'date', 'venue', 'winner']].rename(columns={'city':'City','date':'Date (yy-mm-dd)','venue':'Venue','winner':'Winner'})
            if df_method.shape[0]!=0:
                st.subheader("Duckworth–Lewis–Stern (D/L) method in list")
                st.dataframe(df_method,use_container_width=True,hide_index=True)


            #winner count->
            st.subheader("Visualizing winning count of a team")
            winner_df=temp_ipl['winner'].value_counts().reset_index()
            fig=px.bar(winner_df,x="winner", y="count",labels={'winner':'Match Winner','count':'Count'},hover_name='winner',color='winner',color_discrete_map={team1:"#CB4154",team2:"#AB0B23"})
            st.plotly_chart(fig)

            st.subheader("Visualizing Toss Winning")
            fig = px.bar(df, x="Toss Winner", y="Count",hover_name='Toss Winner', color='Toss Winner',color_discrete_map={team1: "#CB4154", team2: "#AB0B23"})
            st.plotly_chart(fig)

            st.subheader('Visualizing Wins by')
            fig=px.bar(winsby_df,x='Team',y='Count',color='Wins by',barmode='group',hover_name='Team',text_auto=True,color_discrete_map={team1:'#AB0B23',team2:'#CB4154'})
            st.plotly_chart(fig)
            