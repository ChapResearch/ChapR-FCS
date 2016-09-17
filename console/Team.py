#
# Team is an Object used to store the data of a team including:
#
class Team(object):

    def __init__(self,number):        # Number: int to hold number of team, Battery: int to store battery percentage
        self.teamN = number
    
    def getNumber(self):
        return self.teamN

#
# The Match object stores information about the upcoming match.
#   this includes accumulating the list of teams who are "trying to join the match"
#   and those who have been trashed from joining the match.  Note that
#   addTeam() should be called during the process loop by all relevent
#   routines so that incoming teams joinging aren't missed.

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
        self.clearTeams()

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
        if self.positions[position] is not None:
            return self.positions[position]
        else:
            return None

    def getPosition(self, teamN):
        for team in self.positions:
            if self.positions[team].getNumber() == teamN:
                return self.positions[team]
        return None
        
    #
    # addTeam() - called as part of a mechanism to check for incoming
    #             teams joining a match.  Note that a team that is already
    #             part of the current teams (or in the trash) is not added
    #             again.
    #
    def addTeam(self,team):
        if team in self.currentTeams or team in self.trash or team in self.incomingTeams:
            pass
        else:
            self.incomingTeams.append(team)

    #
    # trashTeam() - called to disqualify a particular team from be considered
    #               for the current match.
    #
    def trashTeam(self,team):
        if team in self.currentTeams:
            currentTeams.remove(team)
            trashTeams.append(team)

    #
    # emptyTrash() - put all teams BACK into the current teams.
    #
    def emptyTrash(self):
        self.currentTeams.extend(self.trashTeams)
        self.trashTeams = []

    #
    # clearTeams() - clear all teams and all trash.
    #
    def clearTeams(self):
        self.currentTeams = []     # the list of teams thar are considered "current" (not trash)
        self.trashTeams = []       # teams in the trash
        self.incomingTeams = []    # incoming teams that need to be added when convenient

    #
    # ackIncoming() - take the incoming teams, and add them to the currentTeams
    #                         
    def ackIncoming(self):
        self.currentTeams.extend(self.incomingTeams)
        self.incomingTeams = []
