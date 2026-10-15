from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Data - 5 Marla houses in Multan (Shah Rukn, Model Town, DHA)
# Features: total_bedrooms, floors, has_garage(1/0), has_bethak(1/0) -> Price in Lakh
data = pd.DataFrame({
    'bedrooms': [2, 2, 3, 4, 4, 4, 5],
    'floors': [1, 1, 1, 1, 2, 2, 2],
    'garage': [0, 1, 1, 1, 1, 1, 1],
    'price': [45, 65, 85, 110, 135, 150, 180]
})
model = LinearRegression()
model.fit(data[['bedrooms', 'floors', 'garage']], data['price'])

HTML = """
<h1>5 Marla House - Price Prediction</h1>
<p>Ground: 2BHK + Kitchen + Garage + TV Lounge + Bethak | 1st Floor: 2BHK</p>
<hr>
<form method="post">
 Bedrooms (Total): <input type="number" name="bed" value="{{ bed }}"><br><br>
 Floors: <input type="number" name="floor" value="{{ floor }}"><br><br>
 Garage (1=Yes): <input type="number" name="garage" value="{{ garage }}"><br><br>
 <input type="submit" value="Ghar ki Price Nikalo">
</form>
<h2 style="color:green;">{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = "Apna data daal ke check karo"
    bed, floor, garage = 4, 2, 1
    if request.method == "POST":
        bed = int(request.form["bed"])
        floor = int(request.form["floor"])
        garage = int(request.form["garage"])
        price = model.predict([[bed, floor, garage]])[0]
        result = f"Tere {bed} Bed, {floor} Floor, Garage wale 5 Marla ghar ki price: {int(price)} Lakh Rs (Approx)"

    return render_template_string(HTML, result=result, bed=bed, floor=floor, garage=garage)

if __name__ == "__main__":
    app.run(debug=True)