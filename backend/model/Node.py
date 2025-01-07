class Node :
    def __init__ (self, create = False, data={}) :
        if create :
            self.create(title=data["title"],content=data["content"] if "content" in data else None)
        else :
            self.importJson(data)

    def create (self, title = "new Node", content = None) :
        from random import choice
        from string import ascii_letters
        self.ID = ''.join(choice(ascii_letters) for i in range(5))
        self.title = title
        self.important_Data = Knowledges()
        self.relate_Data = Knowledges()
        self.other_Data = Knowledges()
        self.Summary = ""
        if content is not None :
            self.important_Data.appendKnowedge("Basic","Content" ,content)
        return

    def exportJson (self) :
        return {
            "ID" : self.ID,
            "title" : self.title,
            "important_Data" : self.important_Data.knowledges,
            "relate_Data" : self.relate_Data.knowledges,
            "other_Data" : self.other_Data.knowledges,
            "Summary" : self.Summary
        }
    def importJson (self, data) :
        self.ID = data["ID"]
        self.title = data["title"]
        self.important_Data.knowledges = data["important_Data"]
        self.relate_Data.knowledges = data["relate_Data"]
        self.other_Data.knowledges = data["other_Data"]
        self.Summary = data["Summary"]
        return
    def insertUrl(self, urlType, data) :
        print(urlType)
        if urlType == "important" :
            self.important_Data.appendKnowedge(data.url, data.title, data.content)
        elif urlType == "relate" :
            self.relate_Data.appendKnowedge(data.url, data.title, data.content)
        elif urlType == "other" :
            self.other_Data.appendKnowedge(data.url, data.title, data.content)
        return

class Knowledges :
    def __init__ (self, knowledges = None):
        if knowledges is None :
            self.knowledges = []
        else :
            self.knowledges = knowledges
        return
    def appendKnowedge(self, url, title, content) :
        self.knowledges.append({
            "url" : url,
            "title" : title,
            "content" : content
        })
        return
