
import streamlit as st
from agents import run_request
from translators_data import TRANSLATORS

st.set_page_config(
    page_title="BILSANAK",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F4F8FA;
    color: #183B63;
}

h1, h2, h3 {
    color: #183B63 !important;
}

.stButton > button[kind="primary"] {
    background-color: #32B5BA;
    border-color: #32B5BA;
    color: white;
}

.stButton > button[kind="primary"]:hover {
    background-color: #238F99;
    border-color: #238F99;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #DCEEF0;
    border-radius: 12px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

st.image("bilsanak_logo.jpeg", width=180)

st.title("BILSANAK")
st.subheader("Airport Human Interpreter Service")
st.write("Connecting travelers with professional human interpreters.")

st.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Traveler Page", "Admin / Simulation Page"]
)

if page == "Traveler Page":
    st.header("Traveler Request")

    language = st.selectbox(
        "Select Language",
        ["English", "Chinese", "French", "Spanish", "Urdu"]
    )

    location = st.selectbox(
        "Your Location",
        ["Terminal 1", "Terminal 2", "Terminal 3"]
    )

    service = st.selectbox(
        "Select Service",
        [
            "Passport Control",
            "Baggage Services",
            "Check-in and Boarding",
            "Airport Navigation",
            "General Inquiries"
        ]
    )

if "translators" not in st.session_state:
    st.session_state.translators = [
        translator.copy() for translator in TRANSLATORS
    ]

if "requests" not in st.session_state:
    st.session_state.requests = []

if "message_log" not in st.session_state:
    st.session_state.message_log = []

if "agent_status" not in st.session_state:
    st.session_state.agent_status = {
        "Request Agent": "Idle",
        "Matching Agent": "Idle",
        "Translator Agent": "Idle",
        "Monitoring Agent": "Idle"
    }


if "simulation_scenario" not in st.session_state:
    st.session_state.simulation_scenario = "Normal Service"

if "max_wait_minutes" not in st.session_state:
    st.session_state.max_wait_minutes = 5

if "simulated_delay" not in st.session_state:
    st.session_state.simulated_delay = 8
