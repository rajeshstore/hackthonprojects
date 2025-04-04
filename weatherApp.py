from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    temperature = None
    humidity = None  
    city = None
    error_message = None  

    if request.method == "POST":
        city = request.form["city"]
        API_KEY = "bd71398bae1fad7297e4911cfc048d94"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url, timeout=8)

            if response.status_code == 404:
                error_message = "City not found. Please enter a valid city name."
            else:
                response.raise_for_status()
                data = response.json()

                if "main" in data:
                    temperature = data["main"]["temp"]
                    humidity = data["main"]["humidity"]  
                else:
                    error_message = "Weather data not found for the city."

        except requests.exceptions.Timeout:
            error_message = "Request timed out. Please try again later."
        except requests.exceptions.ConnectionError:
            error_message = "Network issue. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            error_message = f"Error: {str(e)}"

    return render_template("index.html", temperature=temperature, humidity=humidity, city=city, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
