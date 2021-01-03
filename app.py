from flask import Flask, render_template, request
import json
import numpy as numpy
from scipy.stats import skew
from scipy.stats import kurtosis
from numpy import median
import statistics
from scipy import stats

app = Flask(__name__)


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
            varianceList, medianList, skewnessList, statisticRangeList, standardDeviationList, arithmeticAverageList, geometricMeanList, kurtosisList = calculateForAllCountries(year, sex, age_range, currency)
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
                                   standardDeviationList=standardDeviationList,
                                   arithmeticAverageList=arithmeticAverageList,
                                   geometricMeanList=geometricMeanList, kurtosisList=kurtosisList)
        else:
            return render_template('index.html')
    except Exception as e:
        return render_template("500error.html", error=str(e))


@app.route('/getCountry/<country_name>', methods=['POST', 'GET'])
def get_sale(country_name):
    try:
        if request.method == 'POST':
            category = request.form['category']
            currency = request.form['currency']
            age18_24List = []
            age25_49List = []
            age50_64List = []
            femaleList = []
            maleList = []
            List2013 = []
            List2014 = []
            List2015 = []
            List2016 = []
            List2017 = []
            List2018 = []
            List2019 = []
            if category == "age":
                age18_24List, age25_49List, age50_64List = getListsAgeClass(country_name, currency)
                print(age18_24List)
                print(age25_49List)
                print(age50_64List)
            elif category == "sex":
                getListsSex(country_name, currency)
            elif category == "year":
                List2013, List2014, List2015, List2016, List2017, List2018, List2019 = getListsYear(country_name, currency)
                print(List2013)
                print(List2014)
                print(List2015)
                print(List2016)
                print(List2017)
                print(List2018)
                print(List2019)
            return render_template("countryInfo.html", country_name=country_name, age18_24List=age18_24List, age25_49List=age25_49List,
                                   age50_64List=age50_64List, femaleList=femaleList, maleList=maleList, List2013=List2013, List2014=List2014,
                                   List2015=List2015, List2016=List2016, List2017=List2017, List2018=List2018, List2019=List2019)
        else:
            return render_template("countryInfo.html", country_name=country_name)
    except Exception as e:
        return render_template("500error.html", error=str(e))


def getListsAgeClass(country_name, currency):
    allJsonFileData = []
    age18_24List = []
    age25_49List = []
    age50_64List = []
    index = 0
    with open('dane/dane.json') as json_file:
        for country in json_file:
            allJsonFileData.append(json.loads(country))
            if allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['age_class'] == "18-24":
                age18_24List.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['age_class'] == "25-49":
                age25_49List.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['age_class'] == "50-64":
                age50_64List.append(allJsonFileData[index][currency])
            index += 1
    return age18_24List, age25_49List, age50_64List


def getListsYear(country_name, currency):
    allJsonFileData = []
    index = 0
    List2013 = []
    List2014 = []
    List2015 = []
    List2016 = []
    List2017 = []
    List2018 = []
    List2019 = []
    with open('dane/dane.json') as json_file:
        for country in json_file:
            allJsonFileData.append(json.loads(country))
            if allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2013":
                List2013.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2014":
                List2014.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2015":
                List2015.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2016":
                List2016.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2017":
                List2017.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2018":
                List2018.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2019":
                List2019.append(allJsonFileData[index][currency])
            index += 1
    return List2013, List2014, List2015, List2016, List2017, List2018, List2019


def getListsSex(country_name, currency):
    allJsonFileData = []
    femaleList = []
    maleList = []
    index = 0
    with open('dane/dane.json') as json_file:
        for country in json_file:
            allJsonFileData.append(json.loads(country))
            if allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['sex'] == "Females":
                femaleList.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['sex'] == "Males":
                maleList.append(allJsonFileData[index][currency])
            index += 1
    return femaleList, maleList


def calculateForAllCountries(year, sex, age_range, currency):
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
    print(kurtosisList)
    return varianceList, medianList, skewnessList, statisticRangeList, standardDeviationList, arithmeticAverageList, geometricMeanList, kurtosisList


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
