from transformers import pipeline
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import pandas as pd
import requests
import plotly.express as px
from utils import writeUser, readUser, countUser


def getQuotes(emotion): #https://api-ninjas.com/api/quotes
    category = 'happiness'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'NpCVYR55PG5hrEEwaTQtHA==FMyv3usVDiNuPj8l'})
    if response.status_code == requests.codes.ok:
        response_dict = response.json() #json to make it subcriptable
        return response_dict[0]['quote']
    else:
        print("Error:", response.status_code, response.text)

def showEmotionsTimeline():
    st.header("Mood Journey")
    st.line_chart(readUser(name), x="Date", y="Emotions")

def checkEmotion(image):
    img_classification = pipeline(task="image-classification", model="kdhht2334/autotrain-diffusion-emotion-facial-expression-recognition-40429105179")


    #Stock Photo : https://st2.depositphotos.com/4431055/7434/i/950/depositphotos_74340667-stock-photo-smiling-human-face-women.jpg
    preds = img_classification(images=image)
    preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
    emotions = []
    acc = []
    for i, pred in enumerate(preds) :
        emotions.append(preds[i]["label"])
        acc.append(preds[i]["score"])
    
    preds_df = pd.DataFrame({"Emotions":emotions, "Accuracy":acc})
    major_emotion = preds_df.loc[0][0]  #major emotion is the first row, label of emotion is the first column
    writeUser(name, major_emotion)  #save major emotion data
    st.header(f"You're {major_emotion}")
    
    if major_emotion == "happy" :
        st.write(getQuotes("happiness"))
    elif major_emotion == "fear" :
        st.write(getQuotes(major_emotion))
    elif major_emotion == "angry" :
        st.write(getQuotes("anger"))
    elif major_emotion == "disgust" or "neutral" or "sad" or "surprise" :
        st.write(getQuotes("happiness"))

    col1, col2 = st.columns([0.5,0.5], gap="small")
    with col1 :
        st.dataframe(preds_df, use_container_width=True)

    # fig1, ax1 = plt.subplots()
    # ax1.pie(acc, labels=emotions, autopct='%1.1f%%', shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax1.axis.set_major_locator(plt.AutoLocator())

    fig = px.line_polar(preds_df, r='Accuracy', theta='Emotions', line_close=True, width=350, height=350)

    
    with col2 :
        st.write(fig)
    
    if countUser(name) > 1 :
        showEmotionsTimeline()


def initCam():
    img_file_buffer = st.camera_input("Take a picture")
    img = None

    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        st.image(img)
        checkEmotion(img)


    st.write('or')
    uploaded_file = st.file_uploader("Upload your own image")

    if uploaded_file is not None :
        img = Image.open(uploaded_file)
        checkEmotion(img)


st.set_page_config(page_title="MoodJourney", page_icon=Image.open("logo/10.png"))
st.sidebar.empty()

co1, co2, co3 = st.columns([1,1,1])
with co2 :
    st.image(Image.open("logo\9-tp.png"), width=300)
name = st.text_input(label="What is your name?")
if name != "" :
    initCam()

#"angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"
#-disgust, neutral, sad, surprise