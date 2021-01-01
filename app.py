from flask import Flask, render_template, request
import json
import numpy as numpy
from scipy.stats import skew
from scipy.stats import kurtosis
from numpy import median
import statistics
from scipy import stats

app = Flask(__name__)

"""@app.route('/')
def hello_world():
   return render_template('index.html')"""

countriesList = ["Belgium", "Bulgaria", "Czechia", "Denmark", "Germany", "Estonia", "Ireland", "Greece", "Spain", \
                 "France", "Croatia", "Italy", "Cyprus", "Latvia", "Lithuania", "Luxembourg", "Hungary", "Malta", \
                 "Netherlands", "Austria", "Poland", "Portugal", "Romania", "Slovenia", "Slovakia", "Finland", \
                 "Sweden", "United Kingdom", "Iceland", "Norway", "Switzerland", "Montenegro", "North Macedonia", \
                 "Serbia", "Turkey"]


@app.route('/', methods=['POST', 'GET'])
def result():
    try:
        if request.method == 'POST':
            year = request.form['year']
            sex = request.form['sex']
            age_range = request.form['age_range']
            currency = request.form['currency']
            # wariancja
            varianceList = []
            # mediana
            medianList = []
            # skośność
            skewnessList = []
            # rozstęp
            statisticRangeList = []
            # odchylenie standarodwe
            standardDeviationList = []
            # średnia arytmetyczna
            arithmeticAverageList = []
            # średnia geometryczna
            geometricMeanList = []
            # kurtoza
            kurtosisList = []
            for country in countriesList:
                varianceList.append(numpy.round(numpy.var(getDataCountry(year, sex, age_range, currency, country)), 2))
                medianList.append(median(getDataCountry(year, sex, age_range, currency, country)))
                skewnessList.append(
                    numpy.round(skew(getDataCountry(year, sex, age_range, currency, country), bias=False), 2))
                statisticRangeList.append(max(getDataCountry(year, sex, age_range, currency, country)) - min(
                    getDataCountry(year, sex, age_range, currency, country)))
                standardDeviationList.append(
                    numpy.round(statistics.stdev(getDataCountry(year, sex, age_range, currency, country)), 2))
                arithmeticAverageList.append(
                    numpy.round(numpy.mean(getDataCountry(year, sex, age_range, currency, country)), 2))
                geometricMeanList.append(
                    numpy.round(stats.gmean(getDataCountry(year, sex, age_range, currency, country)), 2))
                kurtosisList.append(
                    numpy.round(kurtosis(getDataCountry(year, sex, age_range, currency, country), bias=False), 2))
            print(year, sex, age_range, currency)
            print(varianceList)
            print(medianList)
            print(skewnessList)
            print(statisticRangeList)
            print(standardDeviationList)
            print(arithmeticAverageList)
            print(geometricMeanList)
            print(kurtosisList)
            return render_template('index.html', year=year, sex=sex, age_range=age_range, currency=currency,
                                   countriesList=countriesList, varianceList=varianceList, medianList=medianList,
                                   skewnessList=skewnessList, statisticRangeList=statisticRangeList,
                                   standardDeviationList=standardDeviationList, arithmeticAverageList=arithmeticAverageList,
                                   geometricMeanList=geometricMeanList, kurtosisList=kurtosisList)
        else:
            return render_template('index.html')
    except Exception as e:
        return render_template("500error.html", error=str(e))

@app.route('/getCountry/<country_name>', methods=['POST', 'GET'])
def get_sale(country_name):
    print(country_name)
    return render_template("new.html")




'''def calculateForAllCountries(year, sex, age_range, currency):
    #wariancja
    varianceList = []
    #mediana
    medianList = []
    #skośność
    skewnessList = []
    #rozstęp
    statisticRangeList = []
    #odchylenie standarodwe
    standardDeviationList = []
    #średnia arytmetyczna
    arithmeticAverageList = []
    #średnia geometryczna
    geometricMeanList = []
    #kurtoza
    kurtosisList = []
    for country in countriesList:
        varianceList.append(numpy.round(numpy.var(getDataCountry(year, sex, age_range, currency, country)), 2))
        medianList.append(median(getDataCountry(year, sex, age_range, currency, country)))
        skewnessList.append(numpy.round(skew(getDataCountry(year, sex, age_range, currency, country), bias=False), 2))
        statisticRangeList.append(max(getDataCountry(year, sex, age_range, currency, country)) - min(getDataCountry(year, sex, age_range, currency, country)))
        standardDeviationList.append(numpy.round(statistics.stdev(getDataCountry(year, sex, age_range, currency, country)), 2))
        arithmeticAverageList.append(numpy.round(numpy.mean(getDataCountry(year, sex, age_range, currency, country)), 2))
        geometricMeanList.append(numpy.round(stats.gmean(getDataCountry(year, sex, age_range, currency, country)), 2))
        kurtosisList.append(numpy.round(kurtosis(getDataCountry(year, sex, age_range, currency, country), bias=False), 2))
    print(varianceList)
    print(medianList)
    print(skewnessList)
    print(statisticRangeList)
    print(standardDeviationList)
    print(arithmeticAverageList)
    print(geometricMeanList)
    print(kurtosisList)'''

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
                index += 1
    elif year == "2013-2019" and sex == "FemalesMales":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and \
                        allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    elif year == "2013-2019" and age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['sex'] == sex:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    elif sex == "FemalesMales" and age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    elif year == "2013-2019":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['sex'] == sex and \
                        allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    elif sex == "FemalesMales":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year and \
                        allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    elif age_range == "18-64":
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year and \
                        allJsonFileData[index]['sex'] == sex:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    else:
        with open('dane/dane.json') as json_file:
            for country in json_file:
                allJsonFileData.append(json.loads(country))
                if allJsonFileData[index]['country'] == countryName and allJsonFileData[index]['year'] == year and \
                        allJsonFileData[index]['sex'] == sex and allJsonFileData[index]['age_class'] == age_range:
                    finalData.append(allJsonFileData[index][currency])
                index += 1
    json_file.close()
    '''print("Dane")
    print(finalData)'''
    return finalData


if __name__ == '__main__':
    app.run(debug=True)
