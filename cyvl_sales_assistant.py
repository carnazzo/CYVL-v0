import streamlit as st
from typing import List, Dict
import openai

# ---- CONFIG ----
openai.api_key = "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"

# ---- MOCK DATA BASED ON CYVL WEBSITE EXAMPLES ----
mock_data = {
    "City of Boston": [
        {"source": "email", "text": "Thanks for the Cyvl demo. We're particularly interested in how your AI mapping system can support our pavement condition assessments and long-range asset planning."},
        {"source": "slack", "text": "Boston wants to understand the process behind roadway data collection and how the platform integrates with existing GIS."},
        {"source": "meeting", "text": "Discussed use cases around curb & sidewalk inventories and how Cyvl integrates with Cartegraph."},
        {"source": "notes", "text": "Requested a proposal by Friday outlining pricing for full municipal coverage and a pilot program in South Boston."},
    ],
    "City of Palo Alto": [
        {"source": "email", "text": "We are exploring options for automating traffic sign and asset data collection. Cyvl's automated inventory system is compelling."},
        {"source": "slack", "text": "Palo Alto asked if our AI could detect ADA compliance across pedestrian infrastructure."},
        {"source": "meeting", "text": "They shared GIS priorities, including network-level planning for bike lanes and lane condition ratings."},
        {"source": "notes", "text": "Considering Cyvl for a full digital twin pilot in Q3. Interested in cloud-hosted vs. on-prem deployment options."},
    ],
}


# ---- FUNCTIONS ----
def generate_summary(customer: str, records: List[Dict]) -> str:
    context = "\n".join([f"[{r['source']}] {r['text']}" for r in records])
    prompt = f"""
    Summarize the following interactions with {customer}. 
    Include key insights and any action items. Format with bullets.
    
    {context}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_followup(customer: str, records: List[Dict], task: str) -> str:
    context = "\n".join([f"[{r['source']}] {r['text']}" for r in records])
    prompt = f"""
    Based on the following notes for {customer}, draft a professional {task}. Use a helpful tone.

    {context}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# ---- UI ----
st.title("Cyvl Sales Assistant v0")

customer = st.selectbox("Select a customer", list(mock_data.keys()))
records = mock_data[customer]

st.subheader("Unified Customer Timeline")
for r in records:
    st.markdown(f"**{r['source'].capitalize()}**: {r['text']}")

if st.button("Generate Summary"):
    with st.spinner("Generating summary..."):
        summary = generate_summary(customer, records)
        st.subheader("AI Summary")
        st.markdown(summary)

st.subheader("Generate Follow-Up Content")
task_type = st.selectbox("Choose content type", ["follow-up email", "proposal outline"])
if st.button("Generate Content"):
    with st.spinner("Generating content..."):
        content = generate_followup(customer, records, task_type)
        st.markdown(f"**AI-Generated {task_type.title()}**")
        st.text_area("", content, height=300)

st.markdown("---")
st.caption("Prototype by Zach Lanter — April 2025")
