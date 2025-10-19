from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

# JavaScript'ten gelen tarama isteğini karşılar.
@app.route("/scan", methods=['POST'])
def scan():
    data = request.get_json()
    domain = data.get('domain')
    
   
    if domain:
        print(f"Tarama isteği alındı: {domain}")
        return jsonify({"status": "success", "message": f"{domain} için tarama başlatıldı."})
    
    return jsonify({"status": "error", "message": "Domain belirtilmedi."}), 400

if __name__ == '__main__':
    app.run(debug=True)