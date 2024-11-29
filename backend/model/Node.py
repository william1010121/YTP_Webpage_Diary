class Node :
    def __init__ (self, create = False) :
        if create :
            self.create()
    def create (self) :
        from randm import choice
        from string import ascii_letters
        self.ID = ''.join(choice(ascii_letters) for i in range(20)) 
        self.important_Data = Knowledge()
        self.relate_Data = Knowledge()
        self.other_Data = Knowledge()
        self.Summary = ""
        return
        
    def exportJson (self) :
        return {
            "ID" : self.ID,
            "important_Data" : self.important_Data.knowledges,
            "relate_Data" : self.relate_Data.knowledges,
            "other_Data" : self.other_Data.knowledges,
            "Summary" : self.Summary
        }
    def importJson (self, data) :
        self.ID = data["ID"]
        self.important_Data.knowledges = data["important_Data"]
        self.relate_Data.knowledges = data["relate_Data"]
        self.other_Data.knowledges = data["other_Data"]
        self.Summary = data["Summary"]
        return
        
        
class Knowledge :
    def __init__ (self, knowledges = []): :
        self.knowledges = knowledges
