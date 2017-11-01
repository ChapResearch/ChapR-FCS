
import globalVariables as globals

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
    # currentTeams() - self.currentTeams
    #
    def currentTeams(self):
        return self.currentTeams

    #
    # getTrash() - self.trash
    #
    def getTrash(self):
        return self.trash

    # addTeam() - called as part of a mechanism to check for incoming
    #             teams joining a match.  Note that a team that is already
    #             part of the current teams (or in the trash) is not added
    #             again.
    #
    def addTeam(self,team):
        if team in self.currentTeams or team in self.trashTeams or team in self.incomingTeams:
            pass
        else:
            self.incomingTeams.append(team)

    #
    # trashTeam() - called to disqualify a particular team from be considered
    #               for the current match.
    #
    def trashTeam(self,team):
        if team in self.currentTeams:
            self.currentTeams.remove(team)
            self.trashTeams.append(team)

    #
    # emptyTrash() - put all teams BACK into the current teams.
    #
    def emptyTrash(self):
        self.currentTeams.extend(self.trashTeams)
        self.trashTeams = []

    #
    # removeTrash() - Removes a team from the trashTeams list
    #
    def removeTrash(self,team):
        self.trashTeams.remove(team)

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
        self.currentTeams.sort()

    #
    # addCurrent() - add's team to currentTeams
    #
    def addCurrent(self,team):
        self.currentTeams.append(team)
    #
    # fakeTeams() - creates a fake set of incoming teams
    #
    def fakeTeams(self):
            self.incomingTeams = [2468,118,5628,148,27,8886,1080,9999]

    #
    # getBLE() - Gets incoming Team from BLE and inserts it into Incoming Teams list
    #
    def getBLE(self):
        newTeam = globals.BLE.getIncomingTeam()
        if newTeam is not None:
            self.incomingTeams.append(newTeam)

    #
    # getBLErobotStatus() - While robots are reporting battery/status info, this will
    #                       get it and put it where it belongs.
    #
    def getBLErobotStats(self):
        # just call it for now - does nothing with return
        self.globals.BLE.getRobotStats()
