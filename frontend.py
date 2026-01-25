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

# When Run Code is clicked
if run_button:
    output_placeholder.info("Submitting job...")

    response = requests.post(
        f"{API_BASE}/submit",
        json={"code": code}
    )

    if response.status_code != 200:
        output_placeholder.error("Failed to submit job")
    else:
        job_id = response.json()["job_id"]
        output_placeholder.info(f"Job submitted. ID: {job_id}")

        # Polling
        while True:
            time.sleep(1)

            status_res = requests.get(
                f"{API_BASE}/status/{job_id}"
            ).json()

            status = status_res["status"]

            if status in ["queued", "running"]:
                output_placeholder.info(f"Status: {status}...")
            else:
                if status == "success":
                    output_placeholder.success("Execution completed")
                    output_placeholder.code(status_res["output"])
                else:
                    output_placeholder.error("Execution failed")
                    output_placeholder.code(status_res["output"])
                break
