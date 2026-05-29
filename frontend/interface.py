import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Banking AI-Agent")
st.title("Banking AI-Agent")
st.caption(f"Connected to API: {API_BASE_URL}")

message = st.text_area("Customer message", "I can't transfer money, it keeps failing.")

if st.button("Run agent", type="primary"):
    with st.spinner("Running the agentic workflow..."):
        try:
            resp = requests.post(
                f"{API_BASE_URL}/run-agent",
                json={"message": message},
                timeout=180,
            )
            resp.raise_for_status()
            data = resp.json()

            st.subheader("Final reply")
            st.success(data["final_reply"])
            st.write(f"**Routing action:** `{data['action']}`")

            st.subheader("Agent trace")
            st.json(data["trace"])
        except Exception as exc:
            st.error(f"Request failed: {exc}")

with st.sidebar:
    st.header("System")
    if st.button("Check /health"):
        try:
            st.json(requests.get(f"{API_BASE_URL}/health", timeout=10).json())
        except Exception as exc:
            st.error(exc)
    if st.button("Show /config"):
        try:
            st.json(requests.get(f"{API_BASE_URL}/config", timeout=10).json())
        except Exception as exc:
            st.error(exc)
