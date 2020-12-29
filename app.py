from flask import Flask, render_template, request
import json

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#   return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        year = request.form['year']
        sex = request.form['sex']
        age_range = request.form['age_range']
        currency = request.form['currency']
        print(year, sex, age_range, currency)
        getDataCountry(year, sex, age_range, currency, "Belgium")
        return render_template('index.html', year=year, sex=sex, age_range=age_range, currency=currency)
    else:
        return render_template('index.html')


def getData(countryName):
    finalData = []
    allJsonFileData = []
    index = 0
    with open('dane/dane.json') as json_file:
        for country in json_file:
            allJsonFileData.append(json.loads(country))
            if allJsonFileData[index]['country'] == countryName:
                finalData.append(allJsonFileData[index]['mean_equivalised_net_income_euro'])
                print(allJsonFileData[index]['mean_equivalised_net_income_euro'])
            index += 1
    print(allJsonFileData)
    print(finalData)
    json_file.close()


"""def calculateAverage(year, sex, age_range, currency):
    allJsonFileData = []
    index = 0
    dataBelgium = []
    dataBulgaria = []
    dataCzechia = []
    dataDenmark = []
    dataGermany = []
    dataEstonia = []
    dataIreland = []
    dataGreece = []
    dataSpain = []
    dataFrance = []
    dataCroatia = []
    dataItaly = []
    dataCyprus = []
    dataLatvia = []
    dataLithuania = []
    dataLuxembourg = []
    dataHungary = []
    dataMalta = []
    dataNetherlands = []
    dataAustria = []
    dataPoland = []
    dataPortugal = []
    dataRomania = []
    dataSlovenia = []
    dataSlovakia = []
    dataFinland = []
    dataSweden = []
    dataUnitedKingdom = []
    dataIceland = []
    dataNorway = []
    dataSwitzerland = []
    dataMontenegro = []
    dataNorthMacedonia = []
    dataSerbia = []
    dataTurkey = []"""


def getDataCountry(year, sex, age_range, currency, countryName):
    finalData = []
    allJsonFileData = []
    index = 0
    if year == "2013-2019" and sex == "FemalesMales" and age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    elif year == "2013-2019" and sex == "FemalesMales":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and \
                        allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    elif year == "2013-2019" and age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['sex'] == sex:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    elif sex == "FemalesMales" and age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    elif year == "2013-2019":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['sex'] == sex and \
                        allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    elif sex == "FemalesMales":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year and \
                        allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    elif age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year and \
                        allJsonFileData[index]['sex'] == sex:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    else:
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year and \
                        allJsonFileData[index]['sex'] == sex and allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                    print(allJsonFileData[index][currency])
                index += 1
    json_file.close()
    print(finalData)
    return finalData


"""def getDataBulgaria():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataCzechia():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataDenmark():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataGermany():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataEstonia():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataIreland():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataGreece():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataSpain():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataFrance():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataCroatia():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataItaly():
    finalData = []
    allJsonFileData = []
    index = 0

def getDataCyprus():

def getDataLatvia():

def getDataLithuania():

def getDataLuxembourg():

def getDataHungary():

def getDataMalta():

def getDataNetherlands():

def getDataAustria():

def getDataPoland():

def getDataPortugal():

def getDataRomania():

def getDataSlovenia():

def getDataSlovakia():

def getDataFinland():

def getDataSweden():

def getDataUnitedKingdom():

def getDataIceland():

def getDataNorway():

def getDataSwitzerland():

def getDataMontenegro():

def getDataNorthMacedonia():

def getDataSerbia():

def getDataTurkey():"""

if __name__ == '__main__':
    app.run(debug=True)
