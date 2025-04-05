import streamlit as st
import pandas as pd
from ngl_component import show_ngl_viewer
from Bio.PDB import PDBParser
import io

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
    selected_file = aptamer_files[selected_index]
    selected_file.seek(0)
    pdb_data = selected_file.read().decode("utf-8")

    st.subheader(f"🧬 3D View of: {selected_file.name}")
    # Show aptamer with custom settings
show_ngl_viewer(
    pdb_data,
    representation="surface",        # "cartoon", "stick", "surface"
    color_scheme="chainid",          # "element", "residueindex"
    highlight_residues=[10, 45, 102] # List of residues to emphasize
)

