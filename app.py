from flask import Flask, render_template,request

import cv2
from PIL import Image
import requests


from numpy import asarray

import requests
import json
import pytesseract


import pytesseract
import numpy as np
from pytesseract import Output
import re
from datetime import datetime


app = Flask(__name__)




def card(img):
    
    # considering we have a pan card uploaded...

    pnum=""
    dob=""
    ptn1 = re.compile("[A-Z]")
    ptn2=re.compile("[0-9]")

    #img_array=asarray(img)
   
    data =pytesseract.image_to_string(img, lang='eng',config=r'-l eng --oem 3 --psm 6')

    ctr="!()@-*`>+-/,©'—|#%$&^_~="
    
    for c in ctr:
        data=data.replace(c,"")
    
    data=data.replace("\n"," ")
    
    strs=data.split(" ")
    
  
    for st in strs:
        if len(st)==10:
              # for pan number
            if ptn1.match(st[0:5]) and ptn2.match(st[5:9]) and ptn1.match(st[9]):
                pnum=st
            # for dob
        if len(st)==8 and ptn2.match(st):
            dob=st[0:2]+"/"+st[2:4]+"/"+st[4:8]
            dob= datetime.strptime(dob, "%d/%m/%Y").strftime("%d-%m-%Y")
    
   
    return pnum,dob



@app.route('/', methods =['GET','POST'])
def hello_world():
    details=""
   
    if request.method=='POST':
        # print(request.form['title'])
        
        in_img=request.files['pncard']
        in_img = Image.open(in_img).resize((500,300))
        
        
        in_img=asarray(in_img)
        in_img=cv2.cvtColor(in_img,cv2.COLOR_BGR2GRAY)
        in_img=cv2.threshold(in_img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        custom_config=r'-l eng --oem 3 --psm 6'
        
        pnum,dob=card(in_img)
        
        
        
        headers = {"clientId": "1a48309b9de36bedf551a2cb32d44a5f:9ab9c13ce5346d63fe95f3751af390b3",
           "secretKey":"a1LUoUR2zdh4JYBZXyhsz5TZkYy5BMpBf4SCOhXBk7gqj6r2hYoWXrc4e3GnCsMNE",
           "Content-Type": "application/json"}
        url='https://api.emptra.com/panCard/V3'
        data = {"panNumber":pnum}
        
        
        rsp = requests.request("POST", url, headers=headers, json=data)
        data = rsp.text
        details = json.loads(data)
        
        
        details["pnum"]=pnum
        details["dob"]=dob
    return render_template("index.html",details=details)
    
        
    


if __name__== "__main__":      
    app.run(debug=True)