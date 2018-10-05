
from keras.models import load_model

from form_data import *

app = Flask(__name__)

try:
    Crime_model = load_model("Cha_Crime_Onehot.h5")
except:
    function_return = "Error with loading the model into Flask."

@app.route("/MLform")
def index(location_list=location_list,hours=hours,crime_type=crime_type,beat=beat):
    return render_template("MLform.html",location_list=location_list,hours=hours,crime_type=crime_type,beat=beat)

@app.route("/ML",methods=['POST'])
def ML():
    form_data = request.form
    ML_predict = np.random.choice(["True","False"], p=[0.3,0.7])
    ML_results = np.random.random()
    data = [form_data, {"Result": ML_predict, "Probability": ML_results}]
    return jsonify(data)