from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import JsonResponse

from django.core.handlers.wsgi import WSGIRequest
import requests
import random
from django.conf import settings
from pathlib import Path
import base64

from .ML import pred_crop
import google.generativeai as genai
from PIL import Image

import os
from dotenv import load_dotenv
load_dotenv()

gemini_chat = None

# Create your views here.
def home_page(request:WSGIRequest):

    return render(request=request, template_name="base.html", context={})

def search_query(request:WSGIRequest):

    question = request.POST.get("query")
    image_file = request.FILES.get("image",False)
    image_url = None
    if image_file:

        save_dir = Path(settings.MEDIA_ROOT, "query_images")
        save_dir.mkdir(parents=True, exist_ok=True)

        image_path = save_dir / "ai_last_upload.png"   # 👈 always same filename
        with open(image_path, "wb") as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        image_url = Image.open(image_path)

    ai_response = get_answer_from_gemini(question,image_url)
    response = render(request=request,template_name="partials/new_chat_row.html",context={"answer":ai_response,"is_saved_model":False})
    
    return response

def get_base64_for_image(image_path):
    with open(image_path,"rb") as fo:
        return base64.b64encode(fo.read()).decode("utf-8")
    
def build_gemini_model():
    global gemini_chat

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY_1"))

    # for model in genai.list_models():
    #     print(f"Model Name: {model.name}")
    #     print(f"  Supported Methods: {model.supported_generation_methods}")
    #     print("-" * 20)

    model = genai.GenerativeModel('models/gemini-pro-latest', 
            system_instruction = """
            You are an expert agriculture assistant. Your role is to provide accurate, helpful, and practical information about crops, farming techniques, soil health, and pest or disease management.
            You can analyze both text and images. When a user provides an image of a crop, identify the type of plant and predict any visible diseases or pest infections. Describe the disease or pest in detail, including symptoms, causes, and how it spreads.
            You should also recommend appropriate fertilizers, pesticides, or treatments to save the crop. If possible, provide product links to trusted pesticide or treatment options.
            Only respond to queries related to agriculture, and politely decline any unrelated questions.
            Your responses must be in clear, plain paragraph format without using symbols like #, *, or bullet points.
            """
    )

    # Start a chat session with the model
    gemini_chat = model.start_chat(history=[])

def get_answer_from_gemini(question,img=None):
    global gemini_chat

    # Send a message to the bot
    if not gemini_chat:
        build_gemini_model()
    
    else:
        api_keys_list = [os.environ.get("GOOGLE_API_KEY_1"),os.environ.get("GOOGLE_API_KEY_2")]
        # gets a random api key
        api_key = random.choice(api_keys_list)

        genai.configure(api_key=api_key)


    content = [question]
    if img:
        content.append(img)

    try:
        response = gemini_chat.send_message(content)
        return response.text
    
    except Exception as e:
        return str(e)


def answer_from_ML_modals(request:WSGIRequest):

    modal_no = request.GET.get("modal_no",False)

    if modal_no == "0":
        return HttpResponse("hi")
    
    elif modal_no == "1":
        response = render(request=request, template_name="partials/crop_predict.html",context={})
        response["HX-Trigger-After-Swap"] = "success"
        return response
    
    
def predict_crop(request:WSGIRequest):
    
    values = list(request.GET.dict().values())
    values = list(map(lambda x:float(x),values))

    answer = pred_crop.predict_crop(values)

    context = {"answer":answer,"is_saved_model":True}
    
    response = render(request=request, template_name="partials/new_chat_row.html",context=context)
    return response
