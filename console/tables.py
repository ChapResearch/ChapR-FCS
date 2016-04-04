#
# tables.py
#
#    This object implements a table much like HTML tables.  Current
#    functionality includes:
#
#      - alignment
#      - buttons
#      - text and images
#
#    Tables are specified in a tuple array.
#

import pygame
import numbers

# TEMPORARY
#pygame.init()
# TEMPORARY

class Table(object):

    # here is the list of tables that are in this class (or cloned class)
    tableList = []

    flashSpeed = 350

    defaults = {}
    defaults["align"] = "left"                  # alignment can be "left", "right", "center", "number"
    defaults["valign"] = "middle"               # alignment can be "top", "bottom", "middle"
    defaults["bold"] = False                    # true or false for bold (only effective for sysfont)
    defaults["italic"] = False                  # true or false for italics (only effective for sysfont)
    defaults["flashing"] = False                # True to blink the data
    defaults["callback"] = None                 # if callback is given, the data is turned into a button
    defaults["rock"] = None                     # the rock to be passed to the button/callback
    defaults["name"] = None                     # the name is used to update the data in a table
    defaults["borders"] = (None,None,None,None) # given as a tuple (N,E,S,W) of colors for the given borders
    defaults["sysfont"] = None                  # font for the data - sysfont will take presedence over just "font"
    defaults["font"] = "roboto"                 # font for the data
    defaults["fontsize"] = 25                   # size for the font
    defaults["color"] = (255,255,255)           # color for the data
    defaults["bgcolor"] = None                  # background color for the data
    defaults["height"] = None                   # prescribed height of the given piece of data (in pixels)
    defaults["width"] = None                    # prescribed width of the given piece of data (in pixels)
    defaults["cellHeight"] = None               # prescribed height of the given piece of data cell (in pixels)
    defaults["cellWidth"] = None                # prescribed width of the given piece of data cell (in pixels)
    defaults["image"] = None                    # normally filled in during table computation
                    
    #
    # Tables try to optimize the computation to draw the tables, doing it only
    # when necessary.  And once it is drawn, only update it when necessary - like
    # when data is changed.

    def __init__(self,**args):
        self.tableImage = None
        self.computed = False      # true if data has been computed recently
        self.newRow = True         # when True, the next data starts on a new row
        self.tableData = list()    # just indicating that this is where the data is stored
        self.currentRow = -1       # first row will be index 0
        self.currentCol = -1
        self.width = None          # used to store user-specified dimensions of table
        self.height = None
        self.mydefaults = self._getCharacteristics(args,Table.defaults)
        self.__class__.tableList.append(self)
        self.position = (0,0)

    #
    # addSpacer() - just a convenience routine to add a column with a certain amount of
    #               space.
    #
    def addSpacer(self,space):
        self.addData(None,width=space,height=0)     # note that the None ensures width not recomputed

    #
    # addDataImage() - just a convenience routine for easily adding graphics as opposed
    #                    to text.
    #
    def addDataImage(self,filename,angle,scale,**args):
        self.addData(pygame.transform.rotozoom(pygame.image.load(filename).convert(),angle,scale),**args)

    #
    # addData() - adds a new data element to the table.  The "current row" is where the
    #             data is added.  Note that if this is the first data item of a row,
    #             the row data structures are created.  See the "defaults" in the class
    #             (above) to see what arguments are accepted.  Others are quietly ignored.
    #
    #    IMPORTANT - self.mydefaults are set when the object is instantiated - from the the
    #                class defaults.  This means that you can "change" the normal defaults by
    #                supplying arguments to the __init__().
    #
    def addData(self,data,**args):
        self.computed = False
        chars = self._getCharacteristics(args,self.mydefaults)

        # get things setup for a new row if necessary

        if self.newRow:
            self.currentRow += 1
            self.newRow = False
            self.currentCol = -1
            self.tableData.append(list())

        # then add this data as column data

        self.currentCol += 1
        self.tableData[self.currentRow].append([data,chars])

    #
    # changeData() - change a named piece of data in the previously supplied data.
    #                If characteristics are given, they will replace the previous.
    #
    def changeData(self,name,**args):
        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                data,chars = col
                if "name" in chars and chars["name"] == name:
                    changed = False
                    if "data" in args:
                        col[0] = args["data"]
                        changed = True
                    for key,value in args.iteritems():
                        chars[key] = value
                        changed = True
                    if changed:
                        self._compute()

    def setFlash(self,name,flashing):
        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                data,chars = col
                if "name" in chars and chars["name"] == name:
                    chars["flashstate"] = True
                    chars["flashing"] = flashing
                    self._compute()

    #
    # getCellLocation() - given a name, find the target cell and return its location
    #                     in the table.
    #
    def getCellLocation(self,name):
        cell = self._getCell(name)
        if cell is not None:
            return (cell[1]["x"],cell[1]["y"])
        return None

    #
    # getCellSize() - given a name, find the target cell and return its size
    #                     in the table.
    #
    def getCellSize(self,name):
        cell = self._getCell(name)
        if cell is not None:
            return (cell[1]["cellWidth"],cell[1]["cellHeight"])
        return None

    #
    # getCellData() - given a name, find the target cell and return its data
    #                     in the table.
    #
    def getCellData(self,name):
        cell = self._getCell(name)
        if cell is not None:
            return cell[0]
        return None

    #
    # getCellImage() - given a name, find the target cell and return its image
    #                     in the table.
    #
    def getCellImage(self,name):
        cell = self._getCell(name)
        if cell is not None:
            return cell[1]["image"]
        return None

    #
    # _getCell() - given an name, find the target cell and return its characteristics.
    #
    def _getCell(self,name):
        self.compute()
        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                if "name" in col[1] and col[1]["name"] == name:
                    return col
        return None

    #
    # print() - print out a representation of the table
    #
    def pprint(self):
        print self.tableData

    #
    # _getCharacteristics() - given the characteristics that are passed for the given data,
    #                         process any defaults and data substitution, and return the
    #                         standard characteristics dictionary.  If an argument was given
    #                         that doesn't have a default, then it is not a valid argument
    #                         and will be quietly ignored.
    #
    def _getCharacteristics(self,args,defaults):
        chars = {}

        # loop through the defaults, because those are the only args we care about

        for characteristic in defaults:
            chars[characteristic] = defaults[characteristic]
            if characteristic in args and args[characteristic] is not None:
                chars[characteristic] = args[characteristic]

        return chars


    #
    # size() - specifies the desired size of the table.  The font will be selected to
    #          make that size possible.  Either or both dimensions may be specified.
    #
    def size(self,width=None,height=None):
        self.width = width
        self.height = height

    #
    # _compute() - given the data in the current table, compute all of the meta-data about the
    #              data in the table.  NOTE about buttons - when a cell has a callback() in it,
    #              then it is taken as a button. The entire button machinery is used (including
    #              drawing and flashing) by translating the table attributes to button attributes
    #              before the button is drawn.  NOTE, too, that the cell height and width are
    #              calculated normally as if a button wasn't there, then the button is drawn
    #              within that space.  FINAL NOTE, a Screen object must be set in the table for
    #              buttons to work.  The drawn buttons are added to the screen button list.
    #
    def _compute(self):
        self.computed = True           # just planning ahead

        #
        # TODO - self.width and self.height are ignored for now, in the future they should
        #        allow the font sizes to be reset to meet the given height/width

        # first, calculate the sizes of the cells in the table - no rendering is done at this point

        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                (data,chars) = col

                if type(data) is pygame.Surface:              # this is an image
                    width = data.get_width()
                    height = data.get_height()
                    pass
                elif data is not None:                        # otherwise we have text or number
                    data = str(data)
                    if chars["sysfont"] is not None:
                        workingFont = pygame.font.SysFont(chars["sysfont"],chars["fontsize"],bold=chars["bold"],italic=chars["italic"])
                        print "setting sysfont to " + chars["sysfont"]
                        print chars["bold"]
                    else:
                        fontpath = pygame.font.match_font(chars["font"],bold=chars["bold"],italic=chars["italic"])
                        workingFont = pygame.font.Font(fontpath,chars["fontsize"])
                    width,height = workingFont.size(data)

                # note that the cellWidth,cellHeight are set to make _colwidth()
                # work - think of this setting as the "initial" setting the cell size

                if chars["width"] is None:
                    chars["width"] = width
                if chars["height"] is None:
                    chars["height"] = height
                if chars["cellWidth"] is None:
                    chars["cellWidth"] = width
                if chars["cellHeight"] is None:
                    chars["cellHeight"] = height

        # OK, now we have the heights and widths for cells, time to calculate the appropriate
        # origins of the cells based upon the heights and widths of the cells AND the maximum
        # size of the different rows and columns.
        # the table is organized by row, so the max height cell in a row determines the
        # row height AND the size of each cell - this goes for columns too.

        y = 0
        for r, row in enumerate(self.tableData):
            x = 0
            rowHeight = self._rowHeight(r)      # the max height of the current row
            for c, col in enumerate(row):
                colWidth = self._colWidth(c)          # the max width of the current column
                col[1]["x"] = x
                col[1]["y"] = y
                col[1]["cellWidth"] = colWidth
                col[1]["cellHeight"] = rowHeight
                col[1]["inCellX"] = self._align(col[1]["width"],colWidth,col[1]["align"])
                col[1]["inCellY"] = self._align(col[1]["height"],rowHeight,col[1]["valign"])
                x += colWidth
            y+= rowHeight

        #
        # check for and prepare flashing cells
        #
        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                data,chars = col
                chars["flashState"] = True
                if chars["flashing"]:
                    chars["flashTarget"] = pygame.time.get_ticks() + self.__class__.flashSpeed

    #
    # compute() - a user-level interface to the _compute() function.
    #
    def compute(self):
        if not self.computed:
            self._compute()

    #
    # _draw() - draws the current table on the given surface.
    #           It takes the tabledata structure and makes it happen.
    #
    def _draw(self,surface):
        self.compute()

        #
        # now render the individual cell images
        #
        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                data,chars = col

                # otherwise, it is not a button and the image must be calculated

                cellImage = pygame.Surface((chars["cellWidth"],chars["cellHeight"]),pygame.SRCALPHA,self.tableImage)
                if chars["bgcolor"] is not None:
                    cellImage.fill(chars["bgcolor"])

                if chars["flashState"] and type(data) is pygame.Surface:              # this is an image
                    dataImage = data
                    cellImage.blit(dataImage,(chars["inCellX"],chars["inCellY"]))

                elif chars["flashState"] and data is not None:                        # otherwise string or number
                    data = str(data)
                    font = pygame.font.Font(pygame.font.match_font(chars["font"]),chars["fontsize"])
                    dataImage = font.render(data,True,chars["color"])
                    cellImage.blit(dataImage,(chars["inCellX"],chars["inCellY"]))

                chars["image"] = cellImage

        # create the image surface that we will render individual cells to
        # (obviously, this replaces any previous image)

        self.tableImage = pygame.Surface((self._width(),self._height()),pygame.SRCALPHA)

        for r, row in enumerate(self.tableData):
            for c, col in enumerate(row):
                data,chars = col
                self.tableImage.blit(chars["image"],(chars["x"],chars["y"]))

        surface.blit(self.tableImage,self.position)
                    
    #
    # _align() - given the horizontal/vertical dimensions, return the X/Y for alignment
    #
    def _align(self,actual,outer,alignment):
        diff = outer - actual
        if alignment == "center" or alignment == "middle":
            return diff/2
        elif alignment == "right" or alignment == "bottom":
            return diff
        else:
            return 0

    #
    # _rows() - return the number of rows in a table, which could be zero
    #
    def _rows(self):
        return len(self.tableData)

    #
    # _cols() - return the MAXIMUM number of columns in a table.  Not all rows may have
    #           this number of columns.
    #
    def _cols(self):
        max = 0
        for row in self.tableData:
            if len(row) > max:
                max = len(row)
        return max

    #
    # _height() - returns the total height of the table based upon JUST totaling up the
    #             heights of the rows (which is the MAX height of the rows)
    #             TODO - borders aren't yet taken into account
    #
    def _height(self):
        height = 0
        for r in range(0,self._rows()):
            rowMax = self._rowHeight(r)
            height += rowMax
        return height

    #
    # _width() - returns the total width of the table based upon JUST totaling up the
    #            widths of the columns (which is the MAX width of the columns)
    #            TODO - borders aren't yet taken into account
    #
    def _width(self):
        width = 0
        for c in range(0,self._cols()):
            colMax = self._colWidth(c)
            width += colMax
        return width

    #
    # _rowHeight() - returns the maximum height of the given row in the table data
    #                Note that the row is given as an index
    #
    def _rowHeight(self,r):
        max = 0
        for col in self.tableData[r]:
            if col[1]["cellHeight"] > max:
                max = col[1]["cellHeight"]
        return max

    #
    # _colWidth() - returns the maximum width of the given column in the table data
    #               Note that column is given as an index.
    #
    def _colWidth(self,c):
        max = 0
        for row in self.tableData:
            if len(row) > c:
                if row[c][1]["cellWidth"] > max:
                    max = row[c][1]["cellWidth"]
        return max

    #
    # endRow() - marks the current row as ended, so that the next data will start a new
    #            row.  No big deal if a table isn't ended with endRow() because it is
    #            implied.
    #
    def endRow(self):
        self.newRow = True          # note that ending a row doesn't make a table dirty

    @classmethod
    def draw(cls,surface):
        for table in cls.tableList:
            table._draw(surface)

    #
    # clone() - ok, this is somewhat obscure (but the same as in Button)
    #           By calling Table.clone("name") this routine will create a NEW class
    #           called "nameTables" that inherits from Button, but has a different
    #           table list.  This makes it possible to easily have different sets of
    #           tables for different screens.
    #
    @classmethod
    def clone(cls,name):
        return(type(name + "Tables",(Table,object),{'tableList':[]}))

    @classmethod
    def update(cls,surface):
        madeAChange = False
        for table in cls.tableList:
            for r, row in enumerate(table.tableData):
                for c, col in enumerate(row):
                    data,chars = col
                    if chars["flashing"] and pygame.time.get_ticks() > chars["flashTarget"]:
                        chars["flashState"] = not(chars["flashState"])
                        chars["flashTarget"] = pygame.time.get_ticks() + cls.flashSpeed
                        madeAChange = True
        return madeAChange

    #
    # processEvent() - (just like Button.processEvent) Map click events to the appropriate
    #                  callbacks. NOTE that this routine has been streamlined by ensuring
    #                  that only mouse down events cause any action at all.  NOTE too that
    #                  it is assumed that only one cell has the click "inside".
    #
    @classmethod
    def processEvent(cls,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for table in cls.tableList:
                for r, row in enumerate(table.tableData):
                    for c, col in enumerate(row):
                        data,chars = col
                        if table.inside(event.pos,chars):
                            return table._callit(chars)
        return False

    #
    # _callit() - a routine to make the code prettier - this calls the given callback
    #             with the rock if given, otherwise with no arguments.
    #
    def _callit(self,chars):
        if chars["callback"] is not None:
            if chars["rock"] is not None:
                return chars["callback"](chars["rock"])
            else:
                return chars["callback"]()

    #
    # inside() - returns True if the given position (x,y) is within the bounds
    #            of the table cell given.  Used for figuring out clicks.  This works
    #            just like Button.inside() works, just checking for clicks inside
    #            one of the cells for the table.
    #
    def inside(self,pos,chars):
        x,y = pos;

        myx = chars["x"] + self.position[0]
        myy = chars["y"] + self.position[1]
        width = chars["cellWidth"]
        height = chars["cellHeight"]
        return(x >= myx and 
               x <= myx + width and
               y >= myy and
               y <= myy + height)
