import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd


# instancia del objeto Flask
app = Flask(__name__)
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './Archivos'

@app.route("/subir")
def upload_file():
 # renderiamos la plantilla "formulario.html"
 return render_template('formulario.html')

@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Archivos PDF"
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Retornamos una respuesta satisfactoria
  return "<h1>Archivo subido exitosamente</h1>"



@app.route("/data",methods=['GET'])
def show():
  if request.method == 'GET':
    results = []
    read = pd.read_csv("./Archivos/Sistema_de_stock.csv", encoding="ISO-8859-1")
    read = read.loc[:,"CODIGO INT":"CANTIDADES"]
    read = read.loc[read['CANTIDADES']>=3]
    read = read.to_dict(orient='record')
    for row in read:
      results.append(dict(row))
    fieldnames = [key for key in results[0].keys()]

    return render_template('home.html', results=results, fieldnames=fieldnames, len=len)


 

if __name__ == '__main__':
 # Iniciamos la aplicación
 app.run(debug=True)