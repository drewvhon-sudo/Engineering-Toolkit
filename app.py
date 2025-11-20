from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------------- UNIT CONVERSION DATA ---------------------- #
conv = {
    "Length": {"m": 1, "cm": 100, "km": 0.001, "in": 39.3701, "ft": 3.28084, "yd": 1.09361, "mile": 0.000621371},
    "Weight": {"kg": 1, "g": 1000, "lb": 2.20462, "oz": 35.274},
    "Time": {"s": 1, "min": 1 / 60, "hr": 1 / 3600, "day": 1 / 86400},
    "Area": {"m2": 1, "cm2": 10000, "km2": 0.000001, "acre": 0.000247105},
    "Volume": {"L": 1, "mL": 1000, "m3": 0.001, "cm3": 1000, "gal": 0.264172},
    "Pressure": {"Pa": 1, "kPa": 0.001, "MPa": 1e-6, "GPa": 1e-9, "atm": 9.869e-6, "bar": 1e-5, "psi": 1.45038e-4},
    "Energy": {"J": 1, "kJ": 0.001, "cal": 0.239006, "kcal": 0.000239006},
    "Speed": {"m/s": 1, "km/h": 3.6, "mph": 2.23694}
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    value = float(data["value"])
    category = data["category"]
    unitFrom = data["unitFrom"]
    unitTo = data["unitTo"]

    # Temperature conversions (special case)
    if category == "Temperature":
        if unitFrom == "C" and unitTo == "F":
            res = value * 9/5 + 32
        elif unitFrom == "F" and unitTo == "C":
            res = (value - 32) * 5/9
        elif unitFrom == "C" and unitTo == "K":
            res = value + 273.15
        elif unitFrom == "K" and unitTo == "C":
            res = value - 273.15
        elif unitFrom == "F" and unitTo == "K":
            res = (value - 32) * 5/9 + 273.15
        elif unitFrom == "K" and unitTo == "F":
            res = (value - 273.15) * 9/5 + 32
        else:
            res = value
    else:
        res = value * conv[category][unitTo] / conv[category][unitFrom]

    return jsonify({"result": round(res, 4)})


@app.route("/compute", methods=["POST"])
def compute():
    data = request.json
    formula = data["formula"]
    values = [float(v) for v in data["values"]]

    result, unit = 0, ""

    match formula:
        case "F=ma":
            result = values[0] * values[1]; unit = "N"
        case "T=Fr":
            result = values[0] * values[1]; unit = "Nm"
        case "σ=F/A":
            result = values[0] / values[1]; unit = "Pa"
        case "P=Fv":
            result = values[0] * values[1]; unit = "W"
        case "W=Fd":
            result = values[0] * values[1]; unit = "J"
        case "KE=1/2mv2":
            result = 0.5 * values[0] * values[1]**2; unit = "J"
        case "PE=mgh":
            result = values[0] * values[1] * values[2]; unit = "J"
        case "a=F/m":
            result = values[0] / values[1]; unit = "m/s²"
        case "w=v/r":
            result = values[0] / values[1]; unit = "rad/s"
        case "Fc=mv2/r":
            result = values[0] * values[1]**2 / values[2]; unit = "N"

    return jsonify({"result": round(result, 4), "unit": unit})


if __name__ == "__main__":
    app.run(debug=True)

