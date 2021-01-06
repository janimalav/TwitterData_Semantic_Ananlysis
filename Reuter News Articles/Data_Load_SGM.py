import re
from pymongo import MongoClient


def main():
	client = MongoClient("mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/raw_db?retryWrites=true&w=majority")
	db = client.reuter_data
	file = open("reut2-009.sgm","r")
	file2 = open("reut2-014.sgm","r")
	newfilelines = ''
	for line in file:
		newfilelines += line
	content_text=re.compile(r'<BODY>(.*?)</BODY>',re.DOTALL).findall(newfilelines)
	dateline_text=re.compile(r'<DATELINE>(.*?)</DATELINE>',re.DOTALL).findall(newfilelines)
	title_text=re.compile(r'<TITLE.*?>(.*?)</TITLE>').findall(newfilelines)

	for line in file2:
    		newfilelines += line
	content_text=re.compile(r'<BODY>(.*?)</BODY>',re.DOTALL).findall(newfilelines)
	dateline_text=re.compile(r'<DATELINE>(.*?)</DATELINE>',re.DOTALL).findall(newfilelines)
	title_text=re.compile(r'<TITLE.*?>(.*?)</TITLE>').findall(newfilelines)

	for text,title,date in zip(content_text,title_text,dateline_text):
		row={"title":process(title),"dateline":process(date),"body":process(text)}
		db.reuter.insert_one(row).inserted_id
		print(title)
		print(text)
		print(date)

def process(text):
    try:
        text=" ".join(text.split())
        text=re.sub(r"[^\w\s]",'',text)            
    except:
        pass
    return text
if __name__ == "__main__":
    main()