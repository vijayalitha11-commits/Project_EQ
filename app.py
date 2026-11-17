from flask import Flask, render_template, request

app = Flask(__name__)

def load_planets():
    ###
    # Retrieving data from de API
    ###
    # Fictional records
    return [{"name": "Example a", "method": "Transit", "year": 2014, "radius": 1.2, "period": 12.0}, 
            {"name": "Example b", "method": "Radial velocity", "year": 1999, "radius": 12.0, "period": 4.0}, 
            {"name": "Example c", "method": "Transit", "year": 2017, "radius": 2.5, "period": 30.0}]

def filter_planets(planets):
    method = request.args.get("method", "")
    filtered = []
    for planet in planets:
        if (not method) or (planet["method"] == method):
            filtered.append(planet)
    return filtered

@app.get("/")
def index():
    planets = load_planets()
    filtered=filter_planets(planets)
    return render_template("index.html", 
                           planets=filtered, 
                           methods=sorted({planet["method"] for planet in planets}),
                           selected_method=request.args.get("method", ""),
                           max_radius=request.args.get("max_radius", ""),
                           total=len(planets),
                           error="")

if __name__ == "__main__":
    app.run()