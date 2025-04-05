import streamlit.components.v1 as components

def show_ngl_viewer(pdb_data: str):
    """
    Renders an interactive 3D viewer using NGL for a given PDB structure string.
    """
    pdb_string = pdb_data.replace("\n", "\\n")
    
    html = f"""
    <div id="viewport" style="width:100%; height:600px;"></div>
    <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
    <script>
        var stage = new NGL.Stage("viewport");
        var pdbData = "{pdb_string}";
        stage.loadFile(new Blob([pdbData], {{ type: 'text/plain' }}), {{ ext: "pdb" }}).then(function(o) {{
            o.addRepresentation("cartoon");
            o.autoView();
        }});
    </script>
    """
    
    components.html(html, height=620)
