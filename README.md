BILSANAK
An Airport Translator Multi-Agent System

1. Project Description
BILSANAK is a Python-based Multi-Agent System designed to help international travelers who face language barriers at airports. The system connects travelers with suitable human interpreters for in-person assistance based on their language, airport terminal, and interpreter availability.
The system operates in a simulated airport environment with 19 interpreters across three terminals. It supports five languages: English, Chinese, French, Spanish, and Urdu.

3. System Agents
BILSANAK consists of four cooperating agents:
Request Agent: Receives and validates traveler requests.
Matching Agent: Finds a suitable available interpreter based on language and terminal.
Translator Agent: Handles interpreter acceptance or refusal and updates availability.
Monitoring Agent: Monitors service progress and requests a replacement when a delay or interruption occurs.
The agents use rule-based decision-making and structured messages to coordinate interpretation requests.

3. Technologies Used
Python
Google Colab
Streamlit
LangSmith

4. Installation and Setup
Download or clone the BILSANAK GitHub repository.
Open the project notebook in Google Colab.
Make sure the required project files are available in the Colab environment.
Install the required Python libraries using:
pip install -r requirements.txt

5. How to Run
Open Bilisank.ipynb in Google Colab.
Upload the required files (agents.py and the BILSANAK logo) to the Colab Files section. Make sure the filenames match those used in the notebook.
Run the notebook cells one by one, in order, from top to bottom. Do not run all cells at once.
Wait for each cell to finish before running the next cell.
When prompted, enter your own LangSmith API key.
Continue running the remaining cells until the Cloudflare Tunnel generates a Streamlit application link.
Click the generated link to open the BILSANAK interface.
Important: The notebook must be executed cell by cell in the correct order. The application may not work properly if required files are missing or cells are skipped.

6. User Interface
BILSANAK provides an interactive web interface developed using Streamlit. It includes two main pages:
Traveler Page
Allows travelers to select their preferred language, airport terminal, and required service. The system then searches for a suitable available interpreter and displays the request status.
Admin / Simulation Page
Allows users to view interpreter availability, monitor agent statuses, inspect communication logs, and test different service scenarios.

7. Testing Scenarios
Three scenarios were tested to evaluate the system:
Normal Service: The system successfully assigns an available interpreter.
Translator Refusal: The system searches for another interpreter when the first interpreter refuses the assignment.
Translator Delay: The Monitoring Agent detects a simulated delay and requests a replacement interpreter.
All three scenarios produced the expected results in the simulated airport environment.

8. Team Members
Sarah Adel Alfawaz,
Hessa Shatwi Alhuwail,
Shaden Alkhunayn,
Yara Hammad Alanazi,

Course: Introduction to Agent-Based Systems (CAI461)
Academic Year: 2026–2027
___________________________________________________________________________

Run the Application:
To run the BILSANAK application locally:
Install the required libraries:
pip install -r requirements.txt
Run the Streamlit application:
streamlit run app.py
Open the local URL displayed in the terminal.
Live Application
The BILSANAK application is also available online:
https://bilsanak.streamlit.app
Users can access the Traveler Page to request an interpreter or the Admin / Simulation Page to test different scenarios.
