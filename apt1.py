import streamlit as st
import pandas as pd
from ngl_component import show_ngl_viewer
from Bio.PDB import PDBParser
import io

st.set_page_config(page_title="RADAR - Rapid Aptamer Discovery And Rendering", layout="wide")
st.title("🎯 RADAR — Rapid Aptamer Discovery And Rendering")
st.markdown("Welcome to **RADAR**, an interactive platform to visualize and compare EGFR-targeting aptamers for glioblastoma research.")
st.header("📥 Upload Multiple Aptamers")

# Upload multiple PDB files
aptamer_files = st.file_uploader("Upload multiple aptamer PDB files", type=["pdb"], accept_multiple_files=True)

aptamer_data = []

if aptamer_files:
    st.success(f"{len(aptamer_files)} aptamers uploaded.")
    parser = PDBParser(QUIET=True)
    
    for i, file in enumerate(aptamer_files):
        structure = parser.get_structure(file.name, io.StringIO(file.read().decode("utf-8")))
        atom_count = len([a for a in structure.get_atoms()])
        chain_count = len(list(structure.get_chains()))
        aptamer_data.append({
            "Name": file.name,
            "Chains": chain_count,
            "Atoms": atom_count,
            "Index": i
        })

    df = pd.DataFrame(aptamer_data)
    st.subheader("📊 Aptamer Comparison Table")
    st.dataframe(df)

    selected_index = st.selectbox("🧬 Select Aptamer to View in 3D", df["Index"], format_func=lambda i: df.iloc[i]["Name"])
    
    # Reload file (stream already read above)
    st.subheader("🛠️ Visualization Settings")
col1, col2, col3, col4= st.columns(4)

with col1:
    rep_type = st.selectbox("Representation", ["cartoon", "stick", "surface"])
with col2:
    color_scheme = st.selectbox("Coloring", ["chainid", "element", "residueindex"])
with col3:
    highlight_input = st.text_input("Highlight Residues (comma-separated)", "45,88")
with col4:
    background_color = st.selectbox("Background", ["white", "black", "gray", "lightblue", "beige"])

highlight_residues = [int(r.strip()) for r in highlight_input.split(",") if r.strip().isdigit()]

st.subheader("🧬 Aptamer Structures")

for i, file in enumerate(aptamer_files):
    with st.expander(f"Aptamer {i+1}", expanded=True):
        name = st.text_input(f"Enter name for Aptamer {i+1}", value=file.name, key=f"name_{i}")
        file.seek(0)
        pdb_data = file.read().decode("utf-8")

        # Fallback logic: if user selects "stick", use "ball+stick" to avoid blank rendering
safe_representation = rep_type if rep_type != "stick" else "ball+stick"

show_ngl_viewer(
    pdb_data,
    representation=safe_representation,
    color_scheme=color_scheme,
    highlight_residues=highlight_residues,
    background_color=background_color,
    viewer_id=f"viewer_{i}"
)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.9em; color: gray;'>"
    "© 2025 Myreen Ahsan. All rights reserved.<br>"
    "RADAR — Rapid Aptamer Discovery And Rendering"
    "</div>",
    unsafe_allow_html=True
)
