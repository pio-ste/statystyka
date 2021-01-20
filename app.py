from flask import Flask, render_template, request
import json
import numpy as numpy
from scipy.stats import skew
from scipy.stats import kurtosis
from numpy import median
import statistics
from scipy import stats

app = Flask(__name__)


countriesList = ["Belgium", "Bulgaria", "Czechia", "Denmark", "Germany", "Estonia", "Ireland", "Greece", "Spain",
                 "France", "Croatia", "Italy", "Cyprus", "Latvia", "Lithuania", "Luxembourg", "Hungary", "Malta",
                 "Netherlands", "Austria", "Poland", "Portugal", "Romania", "Slovenia", "Slovakia", "Finland",
                 "Sweden", "United Kingdom", "Iceland", "Norway", "Switzerland", "Montenegro", "North Macedonia",
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
            # kurtoza
            kurtosisList = []
            varianceList, medianList, skewnessList, statisticRangeList, standardDeviationList, arithmeticAverageList, kurtosisList = calculateForAllCountries(year, sex, age_range, currency)
            """print(year, sex, age_range, currency)
            print(varianceList)
            print(medianList)
            print(skewnessList)
            print(statisticRangeList)
            print(standardDeviationList)
            print(arithmeticAverageList)
            print(kurtosisList)"""
            skinList = getCountrySkin(year, sex, age_range)
            print(skinList)
            return render_template('index.html', year=year, sex=sex, age_range=age_range, currency=currency,
                                   countriesList=countriesList, varianceList=varianceList, medianList=medianList,
                                   skewnessList=skewnessList, statisticRangeList=statisticRangeList,
                                   standardDeviationList=standardDeviationList, arithmeticAverageList=arithmeticAverageList,
                                   kurtosisList=kurtosisList, skinList=skinList)
        else:
            arithmeticAverageList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            year = "2013-2019"
            sex = "Females"
            age_range = "18-24"
            currency = "mean_equivalised_net_income_euro"
            skinList = getCountrySkin(year, sex, age_range)

            print(skinList)
            return render_template('index.html', year=year, sex=sex, age_range=age_range, currency=currency, arithmeticAverageList=arithmeticAverageList, skinList=skinList)
    except Exception as e:
        return render_template("500error.html", error=str(e))


@app.route('/getCountry/<country_name>', methods=['POST', 'GET'])
def get_country(country_name):
    try:
        if request.method == 'POST':
            category = request.form['category']
            currency = request.form['currency']
            age18_24List = []
            age25_49List = []
            age50_64List = []
            femaleList = []
            maleList = []
            averageYearList = []
            if category == "age":
                age18_24List, age25_49List, age50_64List = getListsAgeClass(country_name, currency)
                print(age18_24List)
                print(age25_49List)
                print(age50_64List)
            elif category == "sex":
                femaleList, maleList = getListsSex(country_name, currency)
                print(femaleList)
                print(maleList)
            elif category == "year":
                averageYearList = getListsYear(country_name, currency)
                print(averageYearList)
            return render_template("countryInfo.html", category=category, country_name=country_name, age18_24List=age18_24List, age25_49List=age25_49List,
                                   age50_64List=age50_64List, femaleList=femaleList, maleList=maleList, averageYearList=averageYearList)
        else:
            return render_template("countryInfo.html", country_name=country_name)
    except Exception as e:
        return render_template("500error.html", error=str(e))


def getListsAgeClass(country_name, currency):
    allJsonFileData = []
    index = 0
    age18_24List = []
    age25_49List = []
    age50_64List = []
    List2013_18_24 = []
    List2013_25_49 = []
    List2013_50_64 = []
    List2014_18_24 = []
    List2014_25_49 = []
    List2014_50_64 = []
    List2015_18_24 = []
    List2015_25_49 = []
    List2015_50_64 = []
    List2016_18_24 = []
    List2016_25_49 = []
    List2016_50_64 = []
    List2017_18_24 = []
    List2017_25_49 = []
    List2017_50_64 = []
    List2018_18_24 = []
    List2018_25_49 = []
    List2018_50_64 = []
    List2019_18_24 = []
    List2019_25_49 = []
    List2019_50_64 = []
    with open('dane/dane.json') as json_file:
        for country in json_file:
            allJsonFileData.append(json.loads(country))
            if allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2013" and allJsonFileData[index]['age_class'] == "18-24":
                List2013_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2013" and allJsonFileData[index]['age_class'] == "25-49":
                List2013_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2013" and allJsonFileData[index]['age_class'] == "50-64":
                List2013_50_64.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2014" and allJsonFileData[index]['age_class'] == "18-24":
                List2014_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2014" and allJsonFileData[index]['age_class'] == "25-49":
                List2014_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2014" and allJsonFileData[index]['age_class'] == "50-64":
                List2014_50_64.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2015" and allJsonFileData[index]['age_class'] == "18-24":
                List2015_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2015" and allJsonFileData[index]['age_class'] == "25-49":
                List2015_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2015" and allJsonFileData[index]['age_class'] == "50-64":
                List2015_50_64.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2016" and allJsonFileData[index]['age_class'] == "18-24":
                List2016_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2016" and allJsonFileData[index]['age_class'] == "25-49":
                List2016_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2016" and allJsonFileData[index]['age_class'] == "50-64":
                List2016_50_64.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2017" and allJsonFileData[index]['age_class'] == "18-24":
                List2017_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2017" and allJsonFileData[index]['age_class'] == "25-49":
                List2017_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2017" and allJsonFileData[index]['age_class'] == "50-64":
                List2017_50_64.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2018" and allJsonFileData[index]['age_class'] == "18-24":
                List2018_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2018" and allJsonFileData[index]['age_class'] == "25-49":
                List2018_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2018" and allJsonFileData[index]['age_class'] == "50-64":
                List2018_50_64.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2019" and allJsonFileData[index]['age_class'] == "18-24":
                List2019_18_24.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2019" and allJsonFileData[index]['age_class'] == "25-49":
                List2019_25_49.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2019" and allJsonFileData[index]['age_class'] == "50-64":
                List2019_50_64.append(allJsonFileData[index][currency])
            index += 1

    age18_24List.append(numpy.round(numpy.mean(List2013_18_24), 2))
    age25_49List.append(numpy.round(numpy.mean(List2013_25_49), 2))
    age50_64List.append(numpy.round(numpy.mean(List2013_50_64), 2))
    age18_24List.append(numpy.round(numpy.mean(List2014_18_24), 2))
    age25_49List.append(numpy.round(numpy.mean(List2014_25_49), 2))
    age50_64List.append(numpy.round(numpy.mean(List2014_50_64), 2))
    age18_24List.append(numpy.round(numpy.mean(List2015_18_24), 2))
    age25_49List.append(numpy.round(numpy.mean(List2015_25_49), 2))
    age50_64List.append(numpy.round(numpy.mean(List2015_50_64), 2))
    age18_24List.append(numpy.round(numpy.mean(List2016_18_24), 2))
    age25_49List.append(numpy.round(numpy.mean(List2016_25_49), 2))
    age50_64List.append(numpy.round(numpy.mean(List2016_50_64), 2))
    age18_24List.append(numpy.round(numpy.mean(List2017_18_24), 2))
    age25_49List.append(numpy.round(numpy.mean(List2017_25_49), 2))
    age50_64List.append(numpy.round(numpy.mean(List2017_50_64), 2))
    age18_24List.append(numpy.round(numpy.mean(List2018_18_24), 2))
    age25_49List.append(numpy.round(numpy.mean(List2018_25_49), 2))
    age50_64List.append(numpy.round(numpy.mean(List2018_50_64), 2))
    if not List2019_18_24:
        age18_24List.append(0)
    else:
        age18_24List.append(numpy.round(numpy.mean(List2019_18_24), 2))
    if not List2019_25_49:
        age25_49List.append(0)
    else:
        age25_49List.append(numpy.round(numpy.mean(List2019_25_49), 2))
    if not List2019_50_64:
        age50_64List.append(0)
    else:
        age50_64List.append(numpy.round(numpy.mean(List2019_50_64), 2))
    print(age18_24List)
    print(age25_49List)
    print(age50_64List)
    return age18_24List, age25_49List, age50_64List


def getListsYear(country_name, currency):
    allJsonFileData = []
    index = 0
    averageYearList = []
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

    averageYearList.append(numpy.round(numpy.mean(List2013), 2))
    averageYearList.append(numpy.round(numpy.mean(List2014), 2))
    averageYearList.append(numpy.round(numpy.mean(List2015), 2))
    averageYearList.append(numpy.round(numpy.mean(List2016), 2))
    averageYearList.append(numpy.round(numpy.mean(List2017), 2))
    averageYearList.append(numpy.round(numpy.mean(List2018), 2))
    if not List2019:
        averageYearList.append(0)
    else:
        averageYearList.append(numpy.round(numpy.mean(List2019), 2))
    return averageYearList


def getListsSex(country_name, currency):
    allJsonFileData = []
    femaleList = []
    maleList = []
    List2013_Females = []
    List2013_Males = []
    List2014_Females = []
    List2014_Males = []
    List2015_Females = []
    List2015_Males = []
    List2016_Females = []
    List2016_Males = []
    List2017_Females = []
    List2017_Males = []
    List2018_Females = []
    List2018_Males = []
    List2019_Females = []
    List2019_Males = []
    index = 0
    with open('dane/dane.json') as json_file:
        for country in json_file:
            allJsonFileData.append(json.loads(country))
            if allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2013" and allJsonFileData[index]['sex'] == "Females":
                List2013_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2013" and allJsonFileData[index]['sex'] == "Males":
                List2013_Males.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2014" and allJsonFileData[index]['sex'] == "Females":
                List2014_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2014" and allJsonFileData[index]['sex'] == "Males":
                List2014_Males.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2015" and allJsonFileData[index]['sex'] == "Females":
                List2015_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2015" and allJsonFileData[index]['sex'] == "Males":
                List2015_Males.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2016" and allJsonFileData[index]['sex'] == "Females":
                List2016_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2016" and allJsonFileData[index]['sex'] == "Males":
                List2016_Males.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2017" and allJsonFileData[index]['sex'] == "Females":
                List2017_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2017" and allJsonFileData[index]['sex'] == "Males":
                List2017_Males.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2018" and allJsonFileData[index]['sex'] == "Females":
                List2018_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2018" and allJsonFileData[index]['sex'] == "Males":
                List2018_Males.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2019" and allJsonFileData[index]['sex'] == "Females":
                List2019_Females.append(allJsonFileData[index][currency])
            elif allJsonFileData[index]['country'] == country_name and allJsonFileData[index]['year'] == "2019" and allJsonFileData[index]['sex'] == "Males":
                List2019_Males.append(allJsonFileData[index][currency])
            index += 1
    femaleList.append(numpy.round(numpy.mean(List2013_Females), 2))
    femaleList.append(numpy.round(numpy.mean(List2014_Females), 2))
    femaleList.append(numpy.round(numpy.mean(List2015_Females), 2))
    femaleList.append(numpy.round(numpy.mean(List2016_Females), 2))
    femaleList.append(numpy.round(numpy.mean(List2017_Females), 2))
    femaleList.append(numpy.round(numpy.mean(List2018_Females), 2))
    if not List2019_Females:
        femaleList.append(0)
    else:
        femaleList.append(numpy.round(numpy.mean(List2019_Females), 2))
    maleList.append(numpy.round(numpy.mean(List2013_Males), 2))
    maleList.append(numpy.round(numpy.mean(List2014_Males), 2))
    maleList.append(numpy.round(numpy.mean(List2015_Males), 2))
    maleList.append(numpy.round(numpy.mean(List2016_Males), 2))
    maleList.append(numpy.round(numpy.mean(List2017_Males), 2))
    maleList.append(numpy.round(numpy.mean(List2018_Males), 2))
    if not List2019_Males:
        maleList.append(0)
    else:
        maleList.append(numpy.round(numpy.mean(List2019_Males), 2))
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
    #kurtoza
    kurtosisList = []
    for country in countriesList:
        varianceList.append(numpy.round(numpy.var(getDataCountry(year, sex, age_range, currency, country)), 2))
        medianList.append(median(getDataCountry(year, sex, age_range, currency, country)))
        skewnessList.append(numpy.round(skew(getDataCountry(year, sex, age_range, currency, country), bias=False), 2))
        statisticRangeList.append(max(getDataCountry(year, sex, age_range, currency, country)) - min(getDataCountry(year, sex, age_range, currency, country)))
        standardDeviationList.append(numpy.round(statistics.stdev(getDataCountry(year, sex, age_range, currency, country)), 2))
        arithmeticAverageList.append(numpy.round(numpy.mean(getDataCountry(year, sex, age_range, currency, country)), 2))
        kurtosisList.append(numpy.round(kurtosis(getDataCountry(year, sex, age_range, currency, country), bias=False), 2))
    """print(varianceList)
    print(medianList)
    print(skewnessList)
    print(statisticRangeList)
    print(standardDeviationList)
    print(arithmeticAverageList)
    print(kurtosisList)"""
    return varianceList, medianList, skewnessList, statisticRangeList, standardDeviationList, arithmeticAverageList, kurtosisList


def getCountrySkin(year, sex, age_range):
    skinList = []
    for country in countriesList:
        skinList.append(getDataCountry(year, sex, age_range, "skin_level", country)[0])
    return skinList


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
