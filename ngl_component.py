import streamlit.components.v1 as components
import json

def show_ngl_viewer(
    pdb_data: str,
    representation: str = "cartoon",        # Options: cartoon, surface, stick
    color_scheme: str = "chainid",          # Options: chainid, element, residueindex
    highlight_residues: list = None         # List of residue numbers to highlight
):
    pdb_string = pdb_data.replace("\n", "\\n")
    highlight_script = ""

    # Optional: highlight specific residues
    if highlight_residues:
        for res_id in highlight_residues:
            highlight_script += f"""
            o.addRepresentation("ball+stick", {{
                sele: "resi {res_id}",
                color: "red",
                scale: 3
            }});
            """

    html = f"""
    <div id="viewport" style="width:100%; height:600px;"></div>
    <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
    <script>
        var stage = new NGL.Stage("viewport");
        var pdbData = "{pdb_string}";

        stage.loadFile(new Blob([pdbData], {{ type: 'text/plain' }}), {{ ext: "pdb" }}).then(function(o) {{
            o.addRepresentation("{representation}", {{
                colorScheme: "{color_scheme}"
            }});
            {highlight_script}
            o.autoView();
        }});
    </script>
    """

    components.html(html, height=620)
