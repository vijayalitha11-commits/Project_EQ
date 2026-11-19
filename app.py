import csv
import re
from pathlib import Path
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data earthquakes.csv"


def load_earthquakes():
    earthquakes = []
    with open(CSV_FILE, newline="", encoding="cp1252") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            date = (row.get("Date") or "").strip()
            match = re.search(r"(\d{2,4})\s*$", date)
            if not match:
                continue

            year = int(match.group(1))
            if year < 100:
                year += 1900

            raw_mortality = (row.get("Mortality") or "").strip().replace(" ", "")
            try:
                mortality = int(raw_mortality) if raw_mortality else 0
            except ValueError:
                continue

            earthquakes.append({
                "area": (row.get("Area") or "").strip(),
                "country": (row.get("Country") or "").strip(),
                "date": date,
                "year": year,
                "magnitude": (row.get("Magnitude") or "").strip(),
                "mortality": mortality,
            })

    return earthquakes


def filter_earthquakes(earthquakes):
    selected_decade = request.args.get("result", "")
    min_death = request.args.get("min_death", "").strip()
    filtered = earthquakes

    if selected_decade:
        decade = int(selected_decade)
        filtered = [
            earthquake for earthquake in filtered
            if decade <= earthquake["year"] < decade + 10
        ]

    if min_death:
        minimum = int(min_death)
        filtered = [
            earthquake for earthquake in filtered
            if earthquake["mortality"] >= minimum
        ]

    return filtered


@app.get("/")
def index():
    earthquakes = load_earthquakes()
    filtered = filter_earthquakes(earthquakes)
    decades = sorted({
        (earthquake["year"] // 10) * 10
        for earthquake in earthquakes
    } | {1950})
    return render_template(
        "eq.html",
        earthquakes=filtered,
        results=decades,
        selected_result=request.args.get("result", ""),
        min_death=request.args.get("min_death", ""),
        total=len(earthquakes),
        error=""
    )


if __name__ == "__main__":
    app.run(debug=True)