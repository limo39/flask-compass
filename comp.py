from flask import Flask, render_template, request, redirect, url_for
import math
import time

app = Flask(__name__)

# Default coordinates for the North Pole
north_pole_latitude = 90.0
north_pole_longitude = 135.0

def calculate_heading(latitude1, longitude1, latitude2, longitude2):
    # Calculate the compass heading based on two sets of coordinates
    delta_longitude = longitude2 - longitude1

    y = math.sin(delta_longitude)
    x = math.cos(latitude1) * math.sin(latitude2) - math.sin(latitude1) * math.cos(latitude2) * math.cos(delta_longitude)

    compass_heading = math.atan2(y, x)
    compass_heading = math.degrees(compass_heading)
    compass_heading = (compass_heading + 360) % 360  # Normalize to [0, 360) degrees
    return compass_heading

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user-provided latitude and longitude
        user_latitude = float(request.form.get("latitude"))
        user_longitude = float(request.form.get("longitude"))
        return redirect(url_for("compass", user_latitude=user_latitude, user_longitude=user_longitude))

    return render_template("index.html")

@app.route("/compass/<float:user_latitude>/<float:user_longitude>")
def compass(user_latitude, user_longitude):
    current_heading = calculate_heading(math.radians(user_latitude), math.radians(user_longitude), math.radians(north_pole_latitude), math.radians(north_pole_longitude))
    yield f"data: {current_heading:.2f}\n\n"
    return current_heading

@app.route("/compass")
def compass_default():
    # Use default coordinates for the North Pole if none are provided
    return redirect(url_for("compass", user_latitude=north_pole_latitude, user_longitude=north_pole_longitude))

if __name__ == "__main__":
    app.run(debug=True)
