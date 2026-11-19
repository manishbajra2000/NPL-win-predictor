import streamlit as st
import pickle
import pandas as pd

teams = [
    'Biratnagar Kings',
    'Kathmandu Gorkhas',
    'Karnali Yaks',
    'Sudurpaschim Royals',
    'Chitwan Rhinos',
    'Lumbini Lions',
    'Pokhara Avengers',
    'Janakpur Bolts'
]

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title("NPL Win Predictor")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the Bowling Team', sorted(teams))

target = st.number_input('Target', min_value=0)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', min_value=0)
with col4:
    over = st.number_input(
        'Overs Completed',
        min_value=0,
        max_value=19,
        step=1
    )

    balls = st.selectbox(
        'Balls Completed',
        [0, 1, 2, 3, 4, 5]
    )

    overs = over + balls / 6
with col5:
    wickets = st.number_input('Wickets Out', min_value=0, max_value=10)

if st.button('Predict Probability'):
    balls_bowled = over * 6 + balls
    balls_left = 120 - balls_bowled

    if batting_team == bowling_team:
        st.error('Batting and bowling teams cannot be the same.')
    elif target <= 0:
        st.error('Please enter a target greater than 0.')
    elif score >= target:
        st.success('The batting team has already reached the target!')
    elif wickets >= 10:
        st.error('The innings is over because all 10 wickets have fallen.')
    elif balls_left <= 0:
        st.error('The 20-over innings is complete.')
    else:
        runs_left = target - score
        balls_left = 120 - (over * 6 + balls)
        wickets_left = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })
        st.table(input_df)
        result = pipe.predict_proba(input_df)
        win_p = result[0][1]
        loss_p = result[0][0]
        st.subheader(f"{batting_team} Win Probability: {win_p*100:.2f}%")
        st.subheader(f"{bowling_team} Win Probability: {loss_p*100:.2f}%")