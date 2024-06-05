import base64
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import folium
from folium import CircleMarker
from datetime import datetime, timedelta
import streamlit_folium
import plotly.graph_objects as go

#Large elements we want to display for Athletes:
# 1. Profile (name)- complete
# 2. win/loss trackers with expander of data on those-complete
# 3. coach notes and coaching team brief 
# 4. Ai notes
# 5. event map

# 6. nutrition tracking and schedule
# 7. wotrkout tracking and schedule
# 8. training tracking and schedule 

# 9. Match history



def set_background_1():
    """
    Set the background of the Streamlit app using a locally stored image.
    """
    image_path = 'wrestler.png'  # Update this path when new image is created
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """

    st.markdown(background_style, unsafe_allow_html=True)
set_background_1()

st.title("Max Steele")

col2 = st.columns(2)
col3 = st.columns(3)
with col3[0]:
     col3_2 = st.columns(2)
col4 = st.columns([3,1,2,5])
col3_1 = st.columns(3)


#profile info
# Profile information
full_name = "Maximus 'Max' Steele"
hometown = "Boulder, Colorado"
major = "Kinesiology"
weight_class = "74 kg"
height = "5'10\""
year_in_college = "Junior"
position = "Wrestler"
current_ranking = "#5 nationally in his weight class"
current_gpa = "3.85"


with col3[0]:
    def profile_container():
        with stylable_container(
            key="profile_container",
            css_styles="""
            {
                background-color: #708090CC;
                color: #001F3F;
                border: 2px solid #FFCB05;
                border-radius: 5px;
                box-shadow: 0px 0px 15px 3px #FFAA00;
                padding: 5px;
            }
            """,
        ):
        #containers as the first element act as sizing for the stylable container, you can then input columns to fill the containers with all kinds of content
            with st.container(border=False):
                st.subheader("Athlete Profile")
                def info_expander():
                    with stylable_container(
                        key="General_info",
                        css_styles="""
                    {
                        background-color: #BECBEA;
                        color: #00000;
                        border: 2px solid #FFCB05;
                        border-radius: 3px;

                        padding: 5px;
                    }
                    """,
                ):
                        with st.expander("General Information"):
                            st.markdown(f"**Full Name**: {full_name}")
                            st.markdown(f"**Hometown**: {hometown}")
                            st.markdown(f"**Major/Field of Study**: {major}")
                            st.markdown(f"**Weight Class**: {weight_class}")
                            st.markdown(f"**Height**: {height}")
                            st.markdown(f"**Year in College**: {year_in_college}")
                info_expander()
                st.subheader("Current Season (2023-2024)")
                st.markdown(f"**Current GPA**: {current_gpa}")
    profile_container()



# Career records and notable events/matches
career_records_F = """
- **Record**: 20 Wins - 5 Losses
- **Notable Match**: Defeated state champion in a thrilling overtime match
- **Highest Ranking**: #12 nationally in his weight class
- **Awards**: Freshman of the Year in the conference
"""
career_records_S = """
**Sophomore Year (2022-2023)**:
- **Record**: 24 Wins - 3 Losses
- **Notable Match**: Won the conference championship
- **Highest Ranking**: #8 nationally in his weight class
- **Awards**: All-Conference First Team, Academic All-American
"""
#Win and Loss dataset and display
# Create the dataset
data = {
    'Match Date': ['2024-01-15', '2024-01-22', '2024-02-01', '2024-02-10', '2024-02-18', 
                   '2024-03-05', '2024-03-12', '2024-03-20', '2024-04-02', '2024-04-10'],
    'Opponent': ['John Doe', 'Jake Smith', 'Chris Johnson', 'Mike Brown', 'Sam Wilson', 
                 'Tom Green', 'Alex Taylor', 'Brian White', 'David Black', 'Kevin Davis'],
    'Result': ['Win', 'Loss', 'Win', 'Loss', 'Win', 'Win', 'Loss', 'Win', 'Loss', 'Win'],
    'Points Scored': [12, 7, 15, 3, 10, 8, 5, 11, 6, 13],
    'Points Against': [4, 10, 2, 8, 6, 7, 9, 4, 12, 5],
    'Match Type': ['Regular', 'Regular', 'Regular', 'Regular', 'Regular', 
                   'Regular', 'Regular', 'Tournament', 'Tournament', 'Tournament'],
    'Location': ['Chicago, IL', 'Detroit, MI', 'Madison, WI', 'Columbus, OH', 'Indianapolis, IN', 
                 'Ann Arbor, MI', 'Milwaukee, WI', 'Chicago, IL', 'Chicago, IL', 'Madison, WI'],
    'Weight Class': ['65 kg']*10,
    'Notes': ['Strong performance, dominant takedowns', 'Close match, needs improvement on defense',
              'Excellent technique, quick victory', 'Struggled against stronger opponent', 
              'Good recovery, solid takedowns', 'Narrow victory, needs to work on stamina', 
              'Defensive errors, needs to improve', 'Strong start in the tournament', 
              'Tough match, struggled with technique', 'Great finish, dominating performance']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate running totals
total_wins = df[df['Result'] == 'Win'].shape[0]
total_losses = df[df['Result'] == 'Loss'].shape[0]

# Calculate averages
average_points_scored_in_wins = df[df['Result'] == 'Win']['Points Scored'].mean()
average_points_against_in_losses = df[df['Result'] == 'Loss']['Points Against'].mean()

# Display metrics
with col4[0]:
    st.subheader("Current Win/Loss record")
    col4_1 = st.columns(2)
    with col4_1[0]:
        st.metric(label="Total Wins", value=total_wins)
        st.metric(label="Avg Points Scored in Wins", value=f"{average_points_scored_in_wins:.2f}")
    with col4_1[1]:
        st.metric(label="Total Losses", value=total_losses)
        st.metric(label="Avg Points Against in Losses", value=f"{average_points_against_in_losses:.2f}")

# Display the dataset (optional)
    with st.popover("Win/Loss data"):
        st.dataframe(df)

with col4[0]:
    def records_container():
        with stylable_container(
            key="records_container",
            css_styles="""
            {
                background-color: #708090CC;
                color: #001F3F;
                border: 2px solid #FFCB05;
                border-radius: 5px;
                box-shadow: 0px 0px 15px 3px #FFAA00;
                padding: 5px;
            }
            """,
        ):
            st.subheader("Career Records and Notable Events/Matches")
            def record_container_F():
                with stylable_container(
                    key="profile_container_F",
                    css_styles="""
                    {
                        background-color: #BECBEA;
                        color: #001F3F;
                        border: 2px solid #FFCB05;
                        border-radius: 10px;
                        
                        padding: 5px;
                    }
                    """,
                ):
                    with st.expander("Freshman Year (2021-2022)"):
                        career_records_F
            record_container_F()

            def record_container_S():
                with stylable_container(
                    key="record_container_S",
                    css_styles="""
                    {
                        background-color: #BECBEA;
                        color: #001F3F;
                        border: 2px solid #FFCB05;
                        border-radius: 10px;
                        
                        padding: 5px;
                    }
                    """,
                ):
                    with st.expander("Sophomore Year (2022-2023)"):
                        career_records_S
            record_container_S()
    records_container()

# Coach introductions
coach_1_intro = """
### Meet the Coaches

#### Coach John Mitchell

Hi everyone! I'm Coach John Mitchell, and I've been part of the wrestling community for over 15 years. As a former collegiate wrestler and a national championship coach, I've dedicated my life to this incredible sport. My coaching philosophy centers on discipline, hard work, and fostering a supportive team environment. I believe in pushing my athletes to their fullest potential while ensuring they enjoy the journey and learn valuable life skills. I'm thrilled to be here at [College/University Name] and look forward to another successful season with our talented wrestlers!

- **Experience**: 15+ years in wrestling coaching
- **Specialty**: Technique refinement and match strategy
- **Achievements**: Coached multiple national champions and All-Americans
- **Contact**: john.mitchell@university.edu
"""

coach_2_intro = """
#### Coach Sarah Thompson

Hello team! I'm Assistant Coach Sarah Thompson, and I'm excited to be part of the coaching staff here at [College/University Name]. My background includes being a former Division I wrestler and coaching at both the high school and collegiate levels. My approach to coaching is holistic, focusing not only on the physical aspects of wrestling but also on mental toughness and personal development. I strive to create a positive and motivating atmosphere where athletes can thrive both on and off the mat. Let's work together to achieve greatness this season!

- **Experience**: 10+ years in wrestling coaching
- **Specialty**: Strength and conditioning, mental preparation
- **Achievements**: Developed numerous state champions and NCAA qualifiers
- **Contact**: sarah.thompson@university.edu
"""

# Display coach introductions
with col3[2]:
    def new_coaches_container():
                with stylable_container(
                    key="new_coaches_container",
                    css_styles="""
                    {
                        background-color: #708090CC;
                       
                        border: 2px solid #FFCB05;
                        border-radius: 5px;
                        box-shadow: 0px 0px 15px 3px #FFAA00;
                        padding: 5px;
                    }
                    """,
                ):
                    with st.container():
                        col3_1 = st.columns(2)    
                        with col3_1[0]:
                            st.subheader("Messages to the Coaches")                        
                            with st.popover("**(New!!) About Coach John Mitchell**"):
                                coach_1_intro
                    
                            with st.popover("**(New!!) About Assistant Coach Sarah Thompson**"):
                                coach_2_intro
                        with col3_1[1]:
                            # List of test coaches
                            coaches = ["Coach John Mitchell", "Coach Sarah Thompson", "Coach Alex Rodriguez", "Coach Emily Johnson"]

                            # Dropdown for selecting a coach
                            selected_coach = st.selectbox("Select a Coach:", coaches)

                            # Text box for additional information or notes
                            additional_info = st.text_area("Additional Information or Notes:")

                            # Display selected coach and additional information
                            st.markdown(f"### Selected Coach: {selected_coach}")
                            st.markdown(f"**Additional Information or Notes:**\n{additional_info}")
    new_coaches_container()

# Dataset for upcoming events
events = [
    {"name": "Midwest Invitational", "date": "2024-06-10", "time": "10:00 AM", "location": "University of Illinois", "lat": 40.1106, "long": -88.2073, "prestige": "Major Event", "info": "First major event of the season"},
    {"name": "Great Lakes Showdown", "date": "2024-06-17", "time": "2:00 PM", "location": "Michigan State University", "lat": 42.7018, "long": -84.4822, "prestige": "Major Event", "info": "High profile teams participating"},
    {"name": "Summer Slam", "date": "2024-06-24", "time": "9:00 AM", "location": "University of Wisconsin", "lat": 43.0766, "long": -89.4125, "prestige": "Casual", "info": "Good opportunity for new wrestlers"},
    {"name": "Independence Cup", "date": "2024-07-04", "time": "12:00 PM", "location": "Ohio State University", "lat": 40.0015, "long": -83.0197, "prestige": "Major Event", "info": "Celebrating Independence Day"},
    {"name": "Corn Belt Classic", "date": "2024-07-11", "time": "11:00 AM", "location": "University of Iowa", "lat": 41.6611, "long": -91.5302, "prestige": "Major Event", "info": "Prestigious regional competition"},
    {"name": "River City Rumble", "date": "2024-07-18", "time": "1:00 PM", "location": "University of Minnesota", "lat": 44.9738, "long": -93.2277, "prestige": "Casual", "info": "Local teams matchup"},
    {"name": "Bluegrass Open", "date": "2024-07-25", "time": "3:00 PM", "location": "University of Kentucky", "lat": 38.0394, "long": -84.5037, "prestige": "Casual", "info": "Open invitational for all levels"},
    {"name": "Rust Belt Invitational", "date": "2024-08-01", "time": "10:00 AM", "location": "Penn State University", "lat": 40.7982, "long": -77.8599, "prestige": "Major Event", "info": "Key event for national rankings"},
    {"name": "Prairie State Duel", "date": "2024-08-08", "time": "4:00 PM", "location": "Northwestern University", "lat": 42.0565, "long": -87.6753, "prestige": "Casual", "info": "Friendly duel with local schools"},
    {"name": "Sunflower State Clash", "date": "2024-08-15", "time": "9:30 AM", "location": "University of Kansas", "lat": 38.9543, "long": -95.2558, "prestige": "Major Event", "info": "Final major event before season break"}
]



with col4[3]:
    # Get today's date
    today = datetime.now().date()

    # Create a folium map
    m = folium.Map(location=[41.8781, -87.6298], zoom_start=5)  # Centered around Chicago for this example

    # Function to determine the color based on the date difference
    def get_date_color(event_date):
        event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        days_diff = (event_date - today).days
        if days_diff <= 15:
            return "red"
        elif 16 <= days_diff <= 30:
            return "yellow"
        else:
            return "green"

    # Function to determine the border color based on the prestige
    def get_prestige_color(prestige):
        if prestige == "Major Event":
            return "purple"
        else:
            return "lightblue"

    # Add markers to the map
    for event in events:
        date_color = get_date_color(event["date"])
        prestige_color = get_prestige_color(event["prestige"])
        tooltip_info = f"""
        <strong>{event['name']}</strong><br>
        Date: {event['date']}<br>
        Time: {event['time']}<br>
        Location: {event['location']}<br>
        Prestige: {event['prestige']}<br>
        Additional Info: {event['info']}
        """
        folium.Marker(
            location=[event["lat"], event["long"]],
            popup=tooltip_info,
            icon=folium.Icon(color="white", icon="info-sign"),
        ).add_to(m)
        CircleMarker(
            location=[event["lat"], event["long"]],
            radius=10,
            color=prestige_color,
            fill=True,
            fill_color=date_color,
            fill_opacity=0.7,
        ).add_to(m)

    # Display the map in Streamlit
    def event_container():
        with stylable_container(
            key="event_container",
            css_styles="""
            {
                background-color: #708090CC;
                color: #001F3F;
                border: 2px solid #FFCB05;
                border-radius: 5px;
                box-shadow: 0px 0px 15px 3px #FFAA00;
                padding: 5px;
            }
            """,
        ):
            with st.container():
                st.title("Upcoming Events Map")
                st.markdown("This map shows the upcoming wrestling events with color-coded markers based on the date and prestige of the event.")
                st_folium = st.components.v1.html(folium.Map._repr_html_(m), height=500)
    event_container()




# Sample data for past events
data = {
    "Event_Date": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05", "2024-05-15"],
    "Event_Name": ["Winter Open", "Spring Classic", "March Madness", "April Showdown", "May Invitational"],
    "Location": ["Chicago, IL", "Detroit, MI", "Columbus, OH", "Indianapolis, IN", "Milwaukee, WI"],
    "Weight_Class": [65, 65, 65, 65, 65],
    "Placement": [1, 3, 2, 4, 1],
    "Result": ["Win", "Loss", "Win", "Loss", "Win"],
    "Coach_Notes": [
        "Great performance overall. Impressive technique on the mat. Needs to work on endurance.",
        "Tough competition, but showed resilience. Needs to improve on counter moves.",
        "Solid effort, good comeback after the last event. Focus on refining takedowns.",
        "Difficult event, but showed good spirit. Need to focus on agility.",
        "Excellent result, demonstrated significant improvement. Keep working on strength training."
    ],
    "Athlete_Notes": [
        "Felt strong and confident. Happy with my performance, but need to work on stamina.",
        "Disappointed with the loss, but learned a lot. Need to focus on defensive strategies.",
        "Proud of my improvement. Will keep working on my takedowns and overall strategy.",
        "Challenging event, felt sluggish. Need to improve my speed and agility.",
        "Extremely satisfied with my performance. Focused on strength and it paid off."
    ]
}

# Convert to DataFrame
past_events_df = pd.DataFrame(data)

st.title("Wrestling Season Timeline")

# Create timeline using Plotly
fig = go.Figure()

# Add past events to the timeline
for i, row in past_events_df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["Event_Date"]],
        y=[0],
        mode='markers+text',
        marker=dict(size=10),
        name=row["Event_Name"],
        hoverinfo='text',
        text=f"Event: {row['Event_Name']}<br>Location: {row['Location']}<br>Placement: {row['Placement']}<br>Result: {row['Result']}",
        textposition="top center"
    ))

# Add current date marker
today = pd.to_datetime("today").strftime('%Y-%m-%d')
fig.add_trace(go.Scatter(
    x=[today],
    y=[0],
    mode='markers+text',
    marker=dict(size=12, color='red'),
    name='Today',
    hoverinfo='text',
    text='Today',
    textposition="top center"
))

# Layout adjustments
fig.update_layout(
    title='Wrestling Season Timeline',
    xaxis_title='Date',
    yaxis_title='',
    yaxis=dict(showticklabels=False),
    showlegend=False,
    xaxis=dict(
        range=["2024-01-01", "2024-12-31"],
        tickformat='%Y-%m-%d'
    )
)

st.plotly_chart(fig)

# Display details of selected event
selected_event = st.selectbox("Select an Event to View Details", past_events_df["Event_Name"])

if selected_event:
    event_details = past_events_df[past_events_df["Event_Name"] == selected_event].iloc[0]
    st.subheader(f"Details for {selected_event}")
    st.write(f"**Event Date:** {event_details['Event_Date']}")
    st.write(f"**Location:** {event_details['Location']}")
    st.write(f"**Weight Class:** {event_details['Weight_Class']}")
    st.write(f"**Placement:** {event_details['Placement']}")
    st.write(f"**Result:** {event_details['Result']}")
    
    with st.expander("Coach Notes"):
        st.write(event_details["Coach_Notes"])
    
    with st.expander("Athlete Notes"):
        st.write(event_details["Athlete_Notes"])

# Text box for athlete's thoughts
st.subheader("Input Your Thoughts on Recent Events")
recent_event = st.selectbox("Select a Recent Event", past_events_df["Event_Name"])
athlete_thoughts = st.text_area("Your Thoughts", "")
submit_button = st.button("Submit")

if submit_button:
    st.write(f"Your thoughts on {recent_event} have been submitted!")


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample data for goals and their set dates
goals_data = [
    {"goal": "Improve endurance and stamina to maintain high performance throughout matches.", "set_date": "2024-05-01"},
    {"goal": "Perfect takedown techniques to increase scoring opportunities.", "set_date": "2024-05-15"},
    {"goal": "Enhance defensive strategies to reduce opponent scoring chances.", "set_date": "2024-06-01"}
]

# Convert to DataFrame for easier handling
goals_df = pd.DataFrame(goals_data)


st.title("Athlete Goals")

# Function to display goals with set dates
def display_goals(goals_df):
    st.subheader("Goals for the Season")
    for index, row in goals_df.iterrows():
        goal = row["goal"]
        set_date = row["set_date"]
        st.markdown(f"**{index + 1}. {goal}**  \n*Set on: {set_date}*")

display_goals(goals_df)

# Select a goal to replace
st.subheader("Manage Your Goals")
goal_to_replace = st.selectbox("Select a goal to replace or add a new goal:", ["Add a new goal"] + [f"Goal {i+1}" for i in range(len(goals_df))])

# Input for the new goal
new_goal = st.text_area("New Goal")

# Calculate days since goals were set
today = datetime.today()
goals_df["set_date"] = pd.to_datetime(goals_df["set_date"])
goals_df["days_since_set"] = (today - goals_df["set_date"]).dt.days

# Check if the new goal can be set
can_set_goal = True
if len(goals_df) >= 3 and goal_to_replace == "Add a new goal":
    st.warning("You already have 3 goals. Please replace an existing goal to add a new one.")
    can_set_goal = False

# Check if the goal can be changed within 14 days
if goal_to_replace != "Add a new goal":
    goal_index = int(goal_to_replace.split()[1]) - 1
    if goals_df.loc[goal_index, "days_since_set"] < 14:
        days_left = 14 - goals_df.loc[goal_index, "days_since_set"]
        st.warning(f"Caution: this goal has only been live for {goals_df.loc[goal_index, 'days_since_set']} of 14 days. Your goal is not able to be changed until 14 days have been reached. Your training incorporates these goals, so it is imperative to choose goals you are passionate about following.")
        can_set_goal = False

# Submit button to set the new goal
goal_submit_button = st.button("Submit")
if goal_submit_button and can_set_goal:
    if goal_to_replace == "Add a new goal":
        new_goal_data = {"goal": new_goal, "set_date": today.strftime('%Y-%m-%d')}
        goals_df = goals_df.append(new_goal_data, ignore_index=True)
    else:
        goals_df.loc[goal_index, "goal"] = new_goal
        goals_df.loc[goal_index, "set_date"] = today.strftime('%Y-%m-%d')
    
    # Display updated goals
    st.success("Goal has been updated successfully!")
    display_goals(goals_df)
