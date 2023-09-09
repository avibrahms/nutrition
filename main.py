import quart
import quart_cors
from quart import request, jsonify

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
# app = quart.Quart(__name__)

@app.post("/addNutrients")
async def add_nutrients():
    csv_line = request.args.get("csv_line")
    # TODO: Add the CSV line to nutrients.csv
    return jsonify({"status": "success"}), 200

@app.get("/generateGraph")
async def generate_graph():
    # TODO: Generate the graph and return its URL
    return jsonify({"graph_url": "your_graph_url_here"}), 200

@app.post("/addAndGenerate")
async def add_and_generate():
    csv_line = request.args.get("csv_line")
    # TODO: Add the CSV line to nutrients.csv
    # TODO: Generate the graph and return its URL
    return jsonify({"graph_url": "your_graph_url_here"}), 200

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    # TODO: Serve your ai-plugin.json
    return await quart.send_file("ai-plugin.json", mimetype="application/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    # TODO: Serve your OpenAPI specification
    return await quart.send_file("openapi.yaml", mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
