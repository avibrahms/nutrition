import quart
import quart_cors
from quart import request, jsonify
from utils import process_csv, read_nutrients, read_personal_info
from constants import data_file_path, info_file_path, HOST
from spider import spider
from graph import graph

app = quart_cors.cors(quart.Quart(__name__), allow_origin=HOST)
# app = quart.Quart(__name__)

@app.post("/addNutrients")
async def add_nutrients():
    csv_line = request.args.get("csv_line")
    process_csv(data_file_path, csv_line)
    return jsonify({"status": "success"}), 200

@app.get("/generateGraph")
async def generate_graph():
    data = read_nutrients(data_file_path)
    info = read_personal_info(info_file_path)
    # chart(info, data)
    graph(info, data)
    spider(info, data)
    return jsonify({"graph_url": f"{HOST}/nutrients.png", "spider_url": f"{HOST}/spider_charts.png"}), 200

@app.post("/addAndGenerate")
async def add_and_generate():
    csv_line = request.args.get("csv_line")
    process_csv(data_file_path, csv_line)
    data = read_nutrients(data_file_path)
    info = read_personal_info(info_file_path)
    # chart(info, data)
    graph(info, data)
    spider(info, data)
    return jsonify({"graph_url": f"{HOST}/nutrients.png", "spider_url": f"{HOST}/spider_charts.png"}), 200

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5005)

if __name__ == "__main__":
    main()
