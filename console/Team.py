#
# Team is an Object used to store the data of a team including:
#
class Team(object):

    def __init__(self,number):        # Number: int to hold number of team, Battery: int to store battery percentage
        self.teamN = number
    
    def getNumber(self):
        return self.teamN

class Match(object):

    R1 = 1
    R2 = 2
    B1 = 3
    B2 = 4
    
    def __init__(self):
        self.positions = dict()
        self.positions[Match.R1] = None
        self.positions[Match.R2] = None
        self.positions[Match.B1] = None
        self.positions[Match.B2] = None

    def add(self,position,teamN):        
        self.positions[position] = Team(teamN)

    def delete(self,teamN):
        for team in self.positions:
            if self.positions[team].getNumber() == teamN:
                self.positions[team] = None
                break
    
    def clear(self):
        for team in self.positions:
            self.positions[team] = None
    
    def getTeam(self, position):
        return self.positions[position]

    def getPosition(self, teamN):
        for team in self.positions:
            if self.positions[team].getNumber() == teamN:
                return self.positions[team]
        return None
        
    
