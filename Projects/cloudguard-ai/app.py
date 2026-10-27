import streamlit as sl

sl.set_page_config(
    page_title="CloudGuard AI",
    page_icon="🛡️",
    layout="wide"
)

sl.title("🛡️ CloudGuard AI")
sl.subheader("AI powered Cloud Security Monitoring")
sl.success("Development environment is Ready!")
sl.write(
    "CloudGuard AI will analyze AWS Cloudtrial logs, "
    "detect suspicious activity and generate "
    "AI assisted incident explanation"
)
sl.info("Current Phase - Weekend 1 - Environment Setup")