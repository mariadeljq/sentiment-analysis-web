from flask import Flask, render_template, request, url_for, redirect, url_for
import pandas as pd
from static.generateimage import *
from static.functions import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    global error_text, extra_text
    error_text = '' 
    extra_text = ''

    if 'excelFile' in request.files:
        archivo = request.files['excelFile'] # request value related to element with name "excelFile"
        
        if archivo.filename.endswith(('.xlsx', '.xls')): # check excel extensions
            df=pd.read_excel(archivo) # read file
            column_name = request.form['columnHeader'].lower() # column name from html form to lowercase to prevent errors
            df.columns = df.columns.str.lower() # columns name to lowercase to match with the column_name variable 

            if (column_name in df.columns): # check if column specified exists in the file

                model_name = "cardiffnlp/twitter-roberta-base-sentiment"
                model_pipeline = pipeline("sentiment-analysis", model=model_name)
                
                positive, neutral, negative , adjs, text_stats = data_processing(df, column_name, model_pipeline)

                image_from_html(
                    archivo.filename,
                    positive['percentage'],
                    neutral['percentage'],
                    negative['percentage'],
                    positive['counter'],
                    neutral['counter'],
                    negative['counter'],
                    positive['average_score'],
                    neutral['average_score'],
                    negative['average_score'],
                    positive['distribution'],
                    neutral['distribution'],
                    negative['distribution'],
                    adjs,
                    text_stats
                )
                
                return redirect(url_for('results'))

            else:
                error_text = "Column with the specified name does not exit."
                extra_text = "Please, make sure to specify the correct header name of the column to be analyzed. If your file, does not have a header name, paste the text from the first row or add a header name."
        
        else:
            error_text = "Introduced file is not a valid Excel file."
            extra_text = "Please, make sure to introduce a file with the following format: .xlsx o .xls"
    
    return redirect(url_for('error'))

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/error')
def error():
    return render_template('error.html',
                           text=error_text,
                           text2=extra_text)

@app.route('/back_home', methods=['POST'])
def back_home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
