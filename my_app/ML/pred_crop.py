import joblib
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


BASE_DIR = Path(__file__).parent.parent
model_path = BASE_DIR / "ML_models/classification_model.pkl"

model = joblib.load(model_path)
label_dict = {0: 'apple',
 1: 'banana',
 2: 'blackgram',
 3: 'chickpea',
 4: 'coconut',
 5: 'coffee',
 6: 'cotton',
 7: 'grapes',
 8: 'jute',
 9: 'kidneybeans',
 10: 'lentil',
 11: 'maize',
 12: 'mango',
 13: 'mothbeans',
 14: 'mungbean',
 15: 'muskmelon',
 16: 'orange',
 17: 'papaya',
 18: 'pigeonpeas',
 19: 'pomegranate',
 20: 'rice',
 21: 'watermelon'}

def predict_crop(list):
    index = model.predict([list])[0]
    pred_crop = label_dict[index]
    return f"""Based on the Given data I predicted the '{pred_crop}' is suitable crop to be Yield for the ground.\n
    I can Predict the following crops {",".join(list(label_dict.values()))}
    """

if __name__ == "__main__":  
    print(predict_crop([90,42,43,20.879744,82.002744,6.502985,94.824760]))
