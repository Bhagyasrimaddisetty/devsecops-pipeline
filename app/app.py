from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data
assets = [
    {"id": 1, "name": "Laptop-001", "status": "active"},
    {"id": 2, "name": "Server-002", "status": "inactive"},
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "devsecops-demo"})

@app.route("/assets", methods=["GET"])
def get_assets():
    return jsonify({"assets": assets, "count": len(assets)})

@app.route("/assets/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404
    return jsonify(asset)

@app.route("/assets", methods=["POST"])
def create_asset():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    new_asset = {
        "id": len(assets) + 1,
        "name": data["name"],
        "status": data.get("status", "active")
    }
    assets.append(new_asset)
    return jsonify(new_asset), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
