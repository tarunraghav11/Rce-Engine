import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="RCE Engine", layout="wide")

st.title("🧠 Remote Code Execution Engine")

# Layout
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Code Editor")
    code = st.text_area(
        "Write your Python code here:",
        height=300,
        value='print("Hello from RCE Engine")'
    )

    run_button = st.button("▶ Run Code")

with right_col:
    st.subheader("Output Console")
    output_placeholder = st.empty()

if run_button:

    if not code.strip():
        output_placeholder.error("Please enter some code before running.")
        st.stop()

    output_placeholder.info("Running your code...")

    response = requests.post(
        f"{API_BASE}/submit",
        json={"code": code}
    )

    if response.status_code != 200:
        output_placeholder.error("Something went wrong.")
        st.stop()

    job_id = response.json()["job_id"]

    while True:
        time.sleep(1)
        status_res = requests.get(
            f"{API_BASE}/status/{job_id}"
        ).json()

        status = status_res["status"]

        if status in ["queued", "running"]:
            output_placeholder.info("Executing...")
        else:
            if status == "success":
                output_placeholder.success("Execution Complete")
                output_placeholder.code(status_res["output"])
            else:
                output_placeholder.error("Execution Failed")
                output_placeholder.code(status_res["output"])
            break

