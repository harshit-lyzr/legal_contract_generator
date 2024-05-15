import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType

st.set_page_config(
    page_title="Legal Contract Generator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Legal Contract Generator")
st.sidebar.markdown("## Welcome to the Legal Contract Generator!")
st.sidebar.markdown(
    "This App Harnesses power of Lyzr Automata to generate Legal Contracts for Ease process of crafting COntracts. You Need to input Type of Contract, Requirements and involved parties and This app will Craft Legal Contract with this information.")

api = st.sidebar.text_input("Enter our OPENAI API KEY Here", type="password")

if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")

example = f"""
Example input
    [type of contract]: Non-Disclosure Agreement
    [specific requirements]: project collaboration
    [parties involved]: Company X and Consultant Y
Example output
**Non-Disclosure Agreement**

**Between:**
[Company X], a corporation organized and existing under the laws of [Jurisdiction], with its principal place of business at [Address] (hereinafter referred to as "Company X"), 

**and**

[Consultant Y], an individual/professional entity, with its principal place of business at [Address] (hereinafter referred to as "Consultant Y").

**Introduction:**

This Non-Disclosure Agreement ("Agreement") is entered into as of [Date] by and between Company X and Consultant Y to facilitate discussions and collaboration regarding certain projects and initiatives (the "Project").

**1. Services:**

Consultant Y agrees to provide services to Company X as mutually agreed upon in writing by both parties. The scope of services, including but not limited to, deliverables, timelines, and milestones, shall be detailed in separate written agreements or statements of work.

**2. Compensation:**

Company X shall compensate Consultant Y for the services rendered according to the terms outlined in the separate written agreement or statement of work. Payment terms and conditions shall be mutually agreed upon by both parties and specified in writing.

**3. Ownership:**

Any and all intellectual property rights, including but not limited to inventions, patents, trademarks, copyrights, and trade secrets, developed or created by Consultant Y in the course of providing services under this Agreement shall be the exclusive property of Company X.

**4. Confidentiality:**

Both parties agree to maintain the confidentiality of all information disclosed during the course of the Project, including but not limited to trade secrets, proprietary information, business strategies, financial data, and technical know-how (collectively, "Confidential Information"). Consultant Y shall not disclose, directly or indirectly, any Confidential Information to any third party without the prior written consent of Company X. This obligation of confidentiality shall survive the termination of this Agreement.

**5. Termination:**

This Agreement may be terminated by either party upon written notice to the other party. In the event of termination, Consultant Y shall promptly return all Confidential Information and any other materials provided by Company X. The provisions of Sections 3 (Ownership) and 4 (Confidentiality) shall survive termination.

**6. Indemnification:**

Consultant Y agrees to indemnify, defend, and hold harmless Company X and its affiliates, officers, directors, employees, and agents from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or related to Consultant Y's breach of any provision of this Agreement.

**7. Governing Law:**

This Agreement shall be governed by and construed in accordance with the laws of [Jurisdiction]. Any dispute arising under or in connection with this Agreement shall be resolved exclusively by the courts of [Jurisdiction].

**8. Entire Agreement:**

This Agreement constitutes the entire understanding between the parties with respect to the subject matter hereof and supersedes all prior agreements, whether written or oral, relating to such subject matter.

**9. Severability:**

If any provision of this Agreement is held to be invalid, illegal, or unenforceable, the validity, legality, and enforceability of the remaining provisions shall not be affected or impaired thereby.

IN WITNESS WHEREOF, the parties hereto have executed this Agreement as of the date first written above.

[Signature of Company X]                                     [Signature of Consultant Y]

[Printed Name and Title]                                      [Printed Name and Title]
"""


def legal_contract(types, requirement, parties):
    legal_agent = Agent(
        prompt_persona="You Are Expert Legal Advisor.",
        role="Legal Contract Expert",
    )

    contract_task = Task(
        name="JS API Integration",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=legal_agent,
        log_output=True,
        instructions=f"""Your Task is to Generate Legal contract With given details.
        Search about Type of contract and craft personalized Legal contract between given parties and mention necessary rules in contract.
        Define rules based on Requirements given by user.
        Below the document leave some space and Mention companies name for signing document.
        Also Make Important word and points to bold.
        Do not write introduction and conclusion.

        Type of Contract: {types}
        Requirements: {requirements}
        Parties Involved: {parties}
        """,
    )

    output = LinearSyncPipeline(
        name="Generate Legal Contract",
        completion_message="Contract Generated!",
        tasks=[
            contract_task
        ],
    ).run()
    return output[0]['task_output']


contract_type = st.text_input("Type of Contract", placeholder="Non Disclosure Agreement")
requirements = st.text_input("Specific Requirement", placeholder="Project Collaboration")
parties = st.text_input("Parties Involved")

if api and st.button("Generate"):
    solution = legal_contract(contract_type, requirements, parties)
    st.markdown(solution)

