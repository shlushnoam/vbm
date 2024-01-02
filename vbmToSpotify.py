import requests, json
from datetime import date


def add_new_data(lesson, mediaPath, dataFile):
    now = date.now()
    day = now.strftime("%B %m %Y %H:%M:%S")

    item = f'''    <item>
      <title>{lesson["title"] + " | " + lesson["author_name"]}</title>
      <description>{lesson["summery"]}</description>
      <pubDate>{day}</pubDate> 
      <enclosure url="{mediaPath}" length="123456789" type="audio/mpeg" />
      <guid isPermaLink="false">unique-episode-id-1</guid>
      <itunes:duration>{lesson["field_reading_time"]}</itunes:duration>
    </item>
'''
    newData = dataFile.split("    <!-- Add individual episode items below -->")
    dataFile = newData[0] + "    <!-- Add individual episode items below -->\n" + item + newData[1]
    return dataFile

'''
input: url
output: title; description; author name; link to the MP3 file
'''
def get_media_path(path_id):
    path = "https://etzion.org.il/he/node/"
    r = requests.get(path + path_id)
    text = r.text
    for line in text.split("\n"):
        #mp3
        if "audio src" in line:
            x = line.split(' ')
            return x[3][4:]
    return "eror"



'''
input: id of the week; number of desired lessons; minnimum lenght of the lesson; maximum lenght of the lesson
output: array with the URLs
'''
def get_lessons(week, numOfLessons, minLen, maxLen):
    dictList = []
    ulrList = []
    counter =  i = 0
    path = "https://etzion.org.il/he/node/"
    params = {"operationName": 0,
        "variables": {},
        "query": "{\n  getSearch(search: {from: 0, size: 24, subjects: [\"" + str(week) + "\"], contentTypes: [\"33\"], lang: [\"he\"]}) {\n    results {\n      nid\n      title\n      summery\n      body\n      field_lesson_date\n      field_banner_image\n      field_reading_time\n      field_id\n      field_series_id\n      parentUrl\n      organization_image\n      media_image\n      parent\n      field_series\n      field_weight\n      field_navigation_subject\n      arr_author_image\n      arr_author_name\n      field_authors\n      field_tag\n      author_name\n      lang\n      tid_parent\n      tag_name\n      highlight\n      arr_navigation_subject\n      field_organization_id\n      organization_name\n      __typename\n    }\n    total\n    __typename\n  }\n}\n"
    }
    r = requests.post("https://etzion.org.il/graphql", json=params)
    a = json.loads(r.content)
    listOfLessons = a["data"]["getSearch"]["results"]

    while counter < numOfLessons and i < len(listOfLessons):
        time = listOfLessons[i]["field_reading_time"].split(":")
        if time[0] == "00" and int(time[1]) > minLen and int(time[1]) < maxLen:
            if not any(d['author_name'] == listOfLessons[i]["author_name"] for d in dictList):
                if listOfLessons[i]["author_name"] != "הרב הראל ברגר" and listOfLessons[i]["author_name"] != "הרב איתיאל גולד":
                    dictList.append(listOfLessons[i])
                    ulrList.append(path + listOfLessons[i]["nid"])
                    counter += 1
        i += 1

    return dictList


def main():
    week = 5951 # שמות
    ans = []
    dataList = get_lessons(week, 6, 20, 40)
    url = 'https://raw.githubusercontent.com/HalelFisherman/tanah/main/rss.xml'
    dataFile = requests.get(url)

    for lesson in dataList:
        mediaPath = get_media_path(lesson["nid"])
        x = [lesson["title"] + " | " + lesson["author_name"], lesson["summery"], mediaPath, lesson["field_reading_time"]]
        ans.append(x)
        #dataFile = add_new_data(lesson, mediaPath, dataFile)
    print(ans)




if __name__ == "__main__":
    main()
