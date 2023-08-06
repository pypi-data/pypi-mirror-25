from urllib.request import urlopen
import xmltodict

def prayer(district):

    base_url = 'http://www2.e-solat.gov.my/xml/today/?zon='
    jakim_xml = xmltodict.parse(urlopen(base_url + district).read())

    prayers = []
    prayer_times = []

    counter = 0
    while(counter < 7):
        prayers.append(
                    jakim_xml['rss']['channel']['item'][counter]['title']
                    )
        prayer_times.append(
                    jakim_xml['rss']['channel']['item'][counter]['description']
                    )
        counter += 1

    a = zip(prayers, prayer_times)
    prayer_tuple = [(k, x) for k, x in a]
    prayer_tuple.insert(0, (jakim_xml['rss']['channel']['description'],
                    jakim_xml['rss']['channel']['dc:date']))

    return (prayer_tuple)
