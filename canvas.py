import json
import math
import os
from io import BytesIO
import base64
from PIL import Image
import plotly.io as pio
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import streamlit as st

def update_drawing_mode():
    st.session_state["drawing_mode"] = st.session_state["drawing_mode_select"]

def calculate_rectangle_length(rect):
    x1, y1 = rect["left"], rect["top"]
    x2, y2 = x1 + rect["width"], y1 + rect["height"]
    length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return length

def create_screenshot(fig):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Convert the figure to an HTML string
    html_str = pio.to_html(fig, full_html=False)
    
    # Save the HTML string to a temporary file with UTF-8 encoding
    temp_file_path = os.path.abspath("temp_plot.html")
    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    
    # Load the HTML file in the browser
    driver.get("file://" + temp_file_path)
    
    # Take a screenshot and get it as base64
    screenshot_base64 = driver.get_screenshot_as_base64()
    driver.quit()
    
    return screenshot_base64

def set_canvas_background(screenshot_base64):
    background_image = Image.open(BytesIO(base64.b64decode(screenshot_base64)))
    return background_image

def save_canvas_data(canvas_data):
    file_path = "canvas_data.json"
    with open(file_path, "w") as f:
        json.dump(canvas_data, f)
    return file_path
