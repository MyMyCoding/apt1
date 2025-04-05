import streamlit.components.v1 as components

def show_ngl_viewer(
    pdb_data: str,
    representation: str = "cartoon",
    color_scheme: str = "chainid",
    highlight_residues: list = None,
    background_color: str = "white",
    viewer_id: str = "viewport"
):
    pdb_string = pdb_data.replace("\n", "\\n")
    highlight_script = ""

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
    <div id="{viewer_id}" style="width:100%; height:600px; background-color:{background_color};"></div>
    <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            var stage = new NGL.Stage("{viewer_id}", {{
                backgroundColor: "{background_color}"
            }});
            var pdbData = "{pdb_string}";
            stage.loadFile(new Blob([pdbData], {{ type: 'text/plain' }}), {{ ext: "pdb" }}).then(function(o) {{
                o.addRepresentation("{representation}", {{
                    colorScheme: "{color_scheme}"
                }});
                {highlight_script}
                o.autoView();
            }});
        }});
    </script>
    """

    components.html(html, height=620)
