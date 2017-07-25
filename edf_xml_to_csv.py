import xml.etree.ElementTree as ET



def getCsv(path, tree, groupChilds=False, skipTagName = None):
    parentTag = path[path.rfind('/')+1:]
    parentsTagsPath = path.replace('/', '.')

    if skipTagName:
        parentsTagsPath += '.' + skipTagName

    csvOutput = ''
    if groupChilds:
        csvOutput = '['
        for parent in tree.iterfind(path):
            for child in parent.iter():
                if groupChilds and (child.tag == parentTag or child.tag == skipTagName):
                    continue
                # Display tags when we are grouping childs only
                if groupChilds:
                    csvOutput += parentsTagsPath + '.' + child.tag + ':' + child.text.replace(',', ' ').replace(';', ' ') + ','
                else:
                    csvOutput += child.text.replace(',', ' ').replace(';', ' ') + ','
    else:
        for child in tree.iterfind(path):
            #for child in elem.iter():
            if groupChilds and (child.tag == parentTag or child.tag == skipTagName):
                continue
            # Display tags when we are grouping childs only
            if groupChilds:
                csvOutput += parentsTagsPath + '.' + child.tag + ':' + child.text.replace(',', ' ').replace(';', ' ') + ','
            else:
                csvOutput += child.text.replace(',', ' ').replace(';', ' ') + ','

    if groupChilds:
        csvOutput = csvOutput.replace(',', '|').strip('|')
    else:
        csvOutput = csvOutput.strip(',')
    if groupChilds:
        csvOutput += ']'

    return csvOutput


def getCurrentStory(xmlStrArray):
    res = ''
    storyTagFound = False
    for line in xmlStrArray:
        if line.find('<Story ContentType=\"Current\">') != -1:
            res += line
            storyTagFound = True
        elif line.find('</Story>') != -1:
            res += line
            return res
        elif storyTagFound:
            res += line



print('StoryContent/Id/SUID,StoryContent/Story/Version,StoryContent/Event,StoryContent/Story/LanguageString,StoryContent/Story/LanguageId,' +
      'StoryContent/Story/BodyTextType,StoryContent/Story/Slug,StoryContent/Story/TopicClusterId,StoryContent/Story/TextEncoding,StoryContent/Story/HotLevel,' +
      'StoryContent/Story/TimeOfUpdate,StoryContent/Story/HeadlineClusterId,StoryContent/Story/Metadata/WireId,' +
      'StoryContent/Story/Metadata/WireName,StoryContent/Story/Metadata/ClassNum,StoryContent/Story/Metadata/StoryGroupId,' +
      'StoryContent/Story/Metadata/TimeOfArrival,StoryContent/Story/Metadata/Headline,' +
      'StoryContent/Story/Metadata/AssignedTickers,StoryContent/Story/Metadata/AssignedTopics,' +
      'StoryContent/Story/Metadata/AssignedPeople,StoryContent/Story/Metadata/DerivedTickers,' +
     'StoryContent/Story/Metadata/DerivedTopics,StoryContent/Story/Metadata/DerivedPeople')

with open("/Users/guillaumetorche/Downloads/EID56899_20170611.xml") as infile:
    contentXmlStr = ''
    contentArray = []
    for line in infile:
        finalCsv = ''
        if line.find('<?xml') != -1 or line.find('<Archive') != -1 or line.find('</Archive') != -1 or line.find('EndTime=') != -1:
            continue
        if line.find('<ContentT>') != -1:
            contentXmlStr = line
            contentArray.append(line)
        elif line.find('</ContentT>') != -1:
            contentXmlStr += line
            contentArray.append(line)
            tree = ET.fromstring(contentXmlStr)
            storyStr = getCurrentStory(contentArray)
            treeStory = ET.fromstring(storyStr)

            finalCsv += getCsv('StoryContent/Id/SUID', tree) + ','
            finalCsv += getCsv('Version', treeStory) + ','
            finalCsv += getCsv('StoryContent/Event', tree) + ','

            finalCsv += getCsv('LanguageString', treeStory) + ','
            finalCsv += getCsv('LanguageId', treeStory) + ','
            finalCsv += getCsv('BodyTextType', treeStory) + ','
            finalCsv += getCsv('Slug', treeStory) + ','
            finalCsv += getCsv('TopicClusterId', treeStory) + ','
            finalCsv += getCsv('TextEncoding', treeStory) + ','
            finalCsv += getCsv('HotLevel', treeStory) + ','
            finalCsv += getCsv('TimeOfUpdate', treeStory) + ','
            finalCsv += getCsv('HeadlineClusterId', treeStory) + ','

            finalCsv += getCsv('Metadata/WireId', treeStory) + ','
            finalCsv += getCsv('Metadata/WireName', treeStory) + ','
            finalCsv += getCsv('Metadata/ClassNum', treeStory) + ','
            finalCsv += getCsv('Metadata/StoryGroupId', treeStory) + ','
            finalCsv += getCsv('Metadata/TimeOfArrival', treeStory) + ','
            finalCsv += getCsv('Metadata/Headline', treeStory) + ','

            finalCsv += getCsv('AssignedTickers', treeStory, True, 'ScoredEntity') + ','
            finalCsv += getCsv('AssignedTopics', treeStory, True, 'ScoredEntity') + ','
            finalCsv += getCsv('AssignedPeople', treeStory, True, 'ScoredEntity') + ','
            finalCsv += getCsv('DerivedTickers', treeStory, True, 'ScoredEntity') + ','
            finalCsv += getCsv('DerivedTopics', treeStory, True, 'ScoredEntity') + ','
            finalCsv += getCsv('DerivedPeople', treeStory, True, 'ScoredEntity')

            contentXmlStr = ''
            contentArray = []
            print(finalCsv)

        else:
            contentArray.append(line)
            contentXmlStr += line




