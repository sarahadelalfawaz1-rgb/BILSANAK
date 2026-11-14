
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

if page == "Traveler Page":

    if st.button("Find a Translator", type="primary"):

        decisions = {
            translator["translator_id"]: True
            for translator in st.session_state.translators
        }

        service_updates = {
            translator["translator_id"]: []
            for translator in st.session_state.translators
        }

        scenario = st.session_state.simulation_scenario
        max_wait = st.session_state.max_wait_minutes
        simulated_delay = st.session_state.simulated_delay

        candidates = [
            translator
            for translator in st.session_state.translators
            if translator["language"] == language
            and translator["location"] == location
            and translator["status"] == "Available"
        ]

        if candidates:

            first_translator_id = candidates[0]["translator_id"]

            if scenario == "Translator Refusal":
                decisions[first_translator_id] = False

            elif scenario == "Translator Delay":
                service_updates[first_translator_id] = [
                    {
                        "elapsed_minutes": simulated_delay,
                        "arrived": False,
                        "interrupted": False
                    }
                ]

        def on_update(agent, status):
            st.session_state.agent_status[agent] = status

        result, messages = run_request(
            language=language,
            location=location,
            service=service,
            translators=st.session_state.translators,
            max_wait_minutes=max_wait,
            decisions=decisions,
            service_updates=service_updates,
            on_update=on_update
        )

        request_id = f"R{len(st.session_state.requests) + 1:03d}"

        st.session_state.requests.append({
            "request_id": request_id,
            "language": language,
            "location": location,
            "service": service,
            "status": result["status"],
            "translator_id": result.get("translator_id")
        })

        st.session_state.message_log.extend(messages)

        if result["status"] == "In Progress":
            st.success(
                f'Request {request_id}: Translator {result["translator_id"]} assigned!'
            )
        else:
            st.warning(
                f'Request {request_id}: {result["status"]}'
            )

if page == "Traveler Page":

    st.divider()
    st.header("📋 Active Requests")

    if not st.session_state.requests:
        st.info("No requests yet. Submit a traveler request to get started.")

    for request in st.session_state.requests:
        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(f'✈️ Request {request["request_id"]}')

            with col2:
                if request["status"] == "In Progress":
                    st.markdown("🟠 **In Progress**")
                elif request["status"] == "Completed":
                    st.markdown("🟢 **Completed**")
                else:
                    st.markdown(f'🔴 **{request["status"]}**')

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f'🌐 **Language:** {request["language"]}')
                st.write(f'📍 **Location:** {request["location"]}')

            with col2:
                st.write(f'🧳 **Service:** {request["service"]}')

            with col3:
                st.write(
                    f'👤 **Translator:** {request["translator_id"] or "Not Assigned"}'
                )

            if request["status"] == "In Progress":
                if st.button(
                    "✓ Complete Service",
                    key=f'complete_{request["request_id"]}'
                ):
                    request["status"] = "Completed"

                    for translator in st.session_state.translators:
                        if translator["translator_id"] == request["translator_id"]:
                            translator["status"] = "Available"
                            break

                    st.session_state.agent_status["Monitoring Agent"] = (
                        f'Service completed by {request["translator_id"]}'
                    )

                    st.rerun()

if page == "Admin / Simulation Page":

    st.divider()
    st.header("⚙️ Simulation Controls")

    st.selectbox(
    "Simulation Scenario",
    ["Normal Service", "Translator Refusal", "Translator Delay"],
    key="_simulation_scenario",
    on_change=lambda: st.session_state.update(
        simulation_scenario=st.session_state._simulation_scenario
    ),
    index=[
        "Normal Service",
        "Translator Refusal",
        "Translator Delay"
    ].index(st.session_state.simulation_scenario)
)

    st.slider(
        "Maximum Waiting Time (minutes)",
        min_value=1,
        max_value=15,
        key="max_wait_minutes"
    )

    if st.session_state.simulation_scenario == "Translator Delay":
        st.slider(
            "Simulated Delay (minutes)",
            min_value=0,
            max_value=20,
            key="simulated_delay"
        )

    st.divider()
    st.header("👥 Translator Availability")

    available_count = sum(
        translator["status"] == "Available"
        for translator in st.session_state.translators
    )

    busy_count = sum(
        translator["status"] == "Busy"
        for translator in st.session_state.translators
    )

    unavailable_count = sum(
        translator["status"] == "Unavailable"
        for translator in st.session_state.translators
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🟢 Available", available_count)

    with col2:
        st.metric("🟠 Busy", busy_count)

    with col3:
        st.metric("🔴 Unavailable", unavailable_count)

    with col4:
        st.metric(
            "👥 Total Translators",
            len(st.session_state.translators)
        )

    st.subheader("Translator Directory")

    st.dataframe(
        st.session_state.translators,
        use_container_width=True,
        hide_index=True,
        column_config={
            "translator_id": st.column_config.TextColumn(
                "Translator ID"
            ),
            "language": st.column_config.TextColumn(
                "Language"
            ),
            "location": st.column_config.TextColumn(
                "Terminal"
            ),
            "status": st.column_config.TextColumn(
                "Status"
            )
        }
    )

if page == "Admin / Simulation Page":

    st.divider()
    st.header("🤖 Agent Status")

    agent_icons = {
        "Request Agent": "📩",
        "Matching Agent": "🔎",
        "Translator Agent": "🗣️",
        "Monitoring Agent": "📊"
    }

    cols = st.columns(4)

    for col, (agent, status) in zip(
        cols, st.session_state.agent_status.items()
    ):
        with col:
            with st.container(border=True):
                st.markdown(f"### {agent_icons[agent]}")
                st.markdown(f"**{agent}**")
                st.caption(status)

    st.divider()
    st.header("💬 Agent Communication Log")

    if st.session_state.message_log:
        st.caption(
            f"Total Messages: {len(st.session_state.message_log)}"
        )

        for i, message in enumerate(
            st.session_state.message_log, start=1
        ):
            with st.expander(
                f'💬 Message {i} | '
                f'{message["sender"]} → {message["receiver"]}'
            ):
                st.write(
                    f'**Performative:** {message["performative"]}'
                )
                st.json(message)
    else:
        st.info(
            "No messages yet. Agent communication will appear here."
        )
