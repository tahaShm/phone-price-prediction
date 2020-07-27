def getProcessedWords(context) : 
    context = lowerAllCharacters(context)
    context = normalizeContext(context)
#     wordList = []
    wordList = removeStopWordsAndPunctuations(context)
    wordList = lemmatizeWords(wordList)
    return wordList
    
    
    
def getProcessedTextData(data, rowName) : 
    totalWords = {}
    wordLists = []
    for row in data :
        wordList = getProcessedWords(row[rowName])
        wordLists.append(wordList)
        for word in wordList : 
            if word in totalWords : 
                totalWords[word] += 1
            else :
                totalWords[word] = 1
#         print(i)
#         print(row['title'])
#         print(wordList)
#         print("_____________________________________________________")
    return [wordLists, totalWords]



[titleWordLists, totalTitleWords] = getProcessedTextData(data, 'title')



[descWordLists, totalDescWords] = getProcessedTextData(data, 'desc')



sortedTitleWords = sorted(totalTitleWords.items(),key=operator.itemgetter(1),reverse=True)
sortedDescWords = sorted(totalDescWords.items(),key=operator.itemgetter(1),reverse=True)

def getImpWords(wordList, amount) : 
    words = set()
    i = 0
    for word in wordList :
        if (i >= amount) : 
            break
        words.add(word[0])
        i += 1
    return words



titleImpWords = getImpWords(sortedTitleWords, 100)
descImpWords = getImpWords(sortedDescWords, 100)



# print(titleImpWords)
# print(descImpWords)
def checkFeature(i, feature, wordList) : 
    if (feature in wordList[i]) : 
        return 1
    return 0



def rowIndex(row):
    return row.name
def addFeatures(prefix, df, impWords, wordLists) :
    i = 0
    totalSize = len(impWords)
    df["rowIndex"] = list(range(len(df)))
    for feature in impWords : 
        df[prefix + feature] = df.apply(lambda row : checkFeature(row['rowIndex'], feature, wordLists), axis = 1) 
        i += 1
        showProgressPercentage(i, totalSize)
    return df



df2 = addFeatures("title_", df, titleImpWords, titleWordLists)



df2 = addFeatures("desc_", df, descImpWords, descWordLists)



def getDatas(df) :
    data = []
    targetData = []
    brands = df.brand.unique()
    avgPrices = getAveragePricesPerBrands(df, brands)
    
    for index, dfRow in df.iterrows() :
        price = dfRow['price']
        if (price == -1) : 
            price = avgPrices[dfRow['brand']]
        targetData.append(price)
#         print(dfRow["desc_lla"])
        del dfRow['price']
        del dfRow['brand']
        del dfRow['city']
        del dfRow['title']
        del dfRow['desc']
        data.append(dfRow)
    
    labels = list(df)
    labels.remove('price')
    labels.remove('brand')
    labels.remove('city')
    labels.remove('title')
    labels.remove('desc')
    print("preprocessing done.")
    return [df, data, targetData, labels]