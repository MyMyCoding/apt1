import streamlit as st
from components.ngl_component import show_ngl_viewer
from utils.interaction_parser import parse_interactions
import pandas as pd
import os

st.set_page_config(page_title="GlioTarget-Aptamer Explorer", layout="wide")

st.title("🧬 GlioTarget-Aptamer Explorer")
st.markdown("Explore EGFR-targeting aptamers and their molecular interactions.")

# Sidebar upload
st.sidebar.header("🔍 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload PDB file", type=['pdb'])
default_path = "data/sample_egfr_aptamer_complex.pdb"

# Load structure
pdb_data = uploaded_file.read().decode("utf-8") if uploaded_file else open(default_path).read()
show_ngl_viewer(pdb_data)

# Interaction Table
st.subheader("🔗 Interaction Table")
interactions = parse_interactions(pdb_data)
st.dataframe(interactions, use_container_width=True)

# Export
st.download_button("Download Interaction Data as CSV", interactions.to_csv(index=False), "interactions.csv", "text/csv")
st.download_button("Download PDB", pdb_data, "structure.pdb", "text/plain")
