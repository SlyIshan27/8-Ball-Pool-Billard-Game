import phylib;
import sqlite3;
import os;
import math;

# ################################################################################
# import constants from phylib to global varaibles
#Constansts
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
DRAG = phylib.PHYLIB_DRAG;
FRAME_INTERVAL = 0.01;
#Header and Footer of svg files
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="poolTable" width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";
#define PHYLIB_DRAG (150) // mm/s^2

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/
#Colours
BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
#Coordinate Class
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
#Still Ball class
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """
    #Constructuor Function
    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    #svg file/image method for a still ball
    def svg( self ):
        svgString = ""
        if self.obj.still_ball.number == 0:
            svgString = """ <circle id="cueBall" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        else:
            svgString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return svgString
#Rolling Ball Class
class RollingBall( phylib.phylib_object):
    #Constructor for a rolling ball and converting it into a class
    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0);

        self.__class__ = RollingBall
    #SVG image mfunction to create svg image for a rolling ball
    def svg( self ):
        svgString = ""
        if self.obj.rolling_ball.number == 0:
            svgString = """ <circle id="cueBall" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        else:
            svgString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return svgString
#Hole Class
class Hole( phylib.phylib_object):
    #Constructor for the hole
    def __init__(self, pos):

        phylib.phylib_object.__init__( self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0);

        self.__class__= Hole
    #SVG function to create a image for a hole
    def svg( self ):
        svgString = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return svgString
#HCushion Class
class HCushion( phylib.phylib_object):
    #Constructor for HCushion
    def __init__(self, y):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y);
        self.y = y
        
        self.__class__= HCushion
    #SVG method function to create svg image of hcushions
    def svg( self ):
        if self.obj.hcushion.y == 0:
            svgString = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        else: 
            svgString = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (2700)
        return svgString
#VCushion Class
class VCushion ( phylib.phylib_object):
    #VCushion Constructor to intialize a v cushion
    def __init__(self, x):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0);

        self.__class__ = VCushion
    #SVG function to generate images of v cushions
    def svg( self ):
        if(self.obj.vcushion.x == 0):
            svgString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        else:
            svgString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (1350)
        return svgString
        

################################################################################
#Table Class
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;


    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                            Coordinate(0,0),
                            Coordinate(0,0),
                            Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                            Coordinate( ball.obj.still_ball.pos.x,
                                        ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;
    #Not Being used as of right now, as it was giving some issues
    def cueBall( self ):
        for item in self:
            if isinstance(item, RollingBall):
                if item.obj.rolling_ball.number == 0:
                    return item
            elif isinstance(item, StillBall):
                if item.obj.still_ball.number == 0:
                    return item
                    
        

    # add svg method here
    #SVG Method
    def svg( self ):
        #print("Check")
        #Appending Header, each obj's svg, and footer.
        svgString = HEADER
        # svgString = ""
        for obj in self:
            if hasattr(obj, 'svg'):
                svgString += obj.svg()
            else:
                svgString += ""
        svgString += FOOTER

        return svgString
    
    def webSvg( self ):
        #print("Check")
        #Appending Header, each obj's svg, and footer.
        # svgString = HEADER
        svgString = ""
        for obj in self:
            if hasattr(obj, 'svg'):
                svgString += obj.svg()
            else:
                svgString += ""
        # svgString += FOOTER

        return svgString

#Creating tables    
class createTables():
    #Getting Cursor and method to check if table exists
    def checkTable(tableName, cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tableName,))
        return cursor.fetchone()
    #Creating Ball Table if it doesn't exist already
    def ball(cursor, connection):
        if not (createTables.checkTable("Ball", cursor)):
            cursor.execute('''CREATE TABLE Ball(
                            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO INTEGER NOT NULL,
                            XPOS FLOAT NOT NULL,
                            YPOS FLOAT NOT NULL,
                            XVEL FLOAT,
                            YVEL FLOAT                                
                        )''')
            # connection.commit()
            # connection.close()
        else:
            pass
            # print("Ball Table exists")
    #Creating TTable if it doesn't exist already
    def tTable(cursor, connection):
        if not(createTables.checkTable("TTable", cursor)):
            cursor.execute('''CREATE TABLE TTable(
                        TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        TIME FLOAT NOT NULL
            ) ''')
            # connection.commit()
            # connection.close()
        else:
            pass
            # print("TTable already exists")
    #Creating a different type of Ball Table if it doesn't exist already
    def ballTable(cursor, connection):
        # connection = sqlite3.connect("phylib.db")
        # cursor = connection.cursor()
        if not(createTables.checkTable("BallTable", cursor)):
            cursor.execute('''CREATE TABLE BallTable(
                        BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
            ) ''')
        else:
            pass
            # print("BallTable Already Exists")
    #Creating Shot Table if it doesn't exist already
    def shot(cursor, connection):
        # connection = sqlite3.connect("phylib.db")
        # cursor = connection.cursor()
        if not(createTables.checkTable("Shot", cursor)):
            cursor.execute('''CREATE TABLE Shot(
                        SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID INTEGER NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)                       
            ) ''')
        else:
            pass
            # print("Shot Table already exists")
    #Creating Table Shot Table if it doesn't exist already
    def tableShot(cursor, connection):
        # connection = sqlite3.connect("phylib.db")
        # cursor = connection.cursor()
        if not (createTables.checkTable("TableShot", cursor)):
            cursor.execute('''CREATE TABLE TableShot(
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
            ) ''')
        else:
            pass
            # print("TableShot Table does not exist")
    #Creating Game Table if it doesn't exist already
    def game(cursor, connection):
        # connection = sqlite3.connect("phylib.db")
        # cursor = connection.cursor()
        if not(createTables.checkTable("Game", cursor)):
            cursor.execute('''CREATE TABLE Game(
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL
            ) ''')
        else:
            pass
            # print("Game Table already exists")
    #Creating Player Table if it doesn't exist already
    def player(cursor, connection):
        # connection = sqlite3.connect("phylib.db")
        # cursor = connection.cursor()
        if not(createTables.checkTable("Player", cursor)):
            cursor.execute('''CREATE TABLE Player(
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            ) ''')
        else:
            # print("Player Table already exists")
            pass

#Databse Class
class Database():
    #Constructor
    def __init__( self, reset=False):
        #If Rest is true remove the .db file
        if reset:
            for db in os.listdir('.'):
                if db.endswith(".db"):
                    #print("Removing DB")
                    os.remove(db)
        #Establishing a connection and a cursor
        self.connection = sqlite3.connect("phylib.db")
        self.cursor = self.connection.cursor()
    #Creating the tables in the database
    def createDB(self):
        self.cursor = self.connection.cursor()
        createTables.ball(self.cursor, self.connection)
        createTables.tTable(self.cursor, self.connection)
        createTables.ballTable(self.cursor, self.connection)
        createTables.shot(self.cursor, self.connection)
        createTables.tableShot(self.cursor, self.connection)
        createTables.game(self.cursor, self.connection)
        createTables.player(self.cursor, self.connection)
        self.connection.commit()
        self.cursor.close()
        # self.connection.close()
    #Reading  tables specificallly BallTable, TTable and Ball, to get the data of the balls to append to a table obj.
    #Then returning the table after updated with ball data.   
    def readTable( self, tableID ):
        self.cursor = self.connection.cursor()
        table = Table()
        self.cursor.execute('''SELECT  * FROM BallTable WHERE TABLEID = ?''', (tableID + 1,))

        result = self.cursor.fetchone()

        if result == None:
            return None
        
        #Getting Time
        self.cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,))

        fetchedTime = self.cursor.fetchone()
        table.time = int(fetchedTime[0])

        #Inner Join needed to get all data of the respective ball
        self.cursor.execute("SELECT * FROM Ball INNER JOIN BallTable ON (Ball.BALLID = BallTable.BALLID) WHERE BallTable.TABLEID = ?", (tableID + 1,))
        poolBalls = self.cursor.fetchall()

        #Fetchall will return a list of tuples. For loop needed to access the different tuples

        #For loop to assign data to a ball object, from the retireved ball data, then appending to table
        for ballInfo in poolBalls:
            ballID = ballInfo[0]
            ballNumber = ballInfo[1]
            ballPos = Coordinate(float(ballInfo[2]), float(ballInfo[3]))
            if ballInfo[4] is None and ballInfo[5] is None:
                ball = StillBall(ballNumber, ballPos)
            else:
                ballVelocity = Coordinate(float(ballInfo[4]), float(ballInfo[5]))
                speed = phylib.phylib_length(ballVelocity)
                if(speed > VEL_EPSILON):
                    accel = Coordinate((-ballVelocity.x / speed) * DRAG, (-ballVelocity.y / speed) * DRAG)
                else:
                    accel = Coordinate(0.0, 0.0)
                ball = RollingBall(ballNumber, ballPos, ballVelocity, accel)
            table += ball

        self.connection.commit()
        self.cursor.close()
        # self.connection.commit()
        # self.connection.close()
        return table
    #Write table, writing the time into TTABLE and inserting ball data into Ball and BallTable
    def writeTable( self, table ):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))

            tableID = self.cursor.lastrowid - 1
            for object in table:
                if isinstance(object, StillBall):
                    self.cursor.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)", (object.obj.still_ball.number, object.obj.still_ball.pos.x, object.obj.still_ball.pos.y))    
                    self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (self.cursor.lastrowid, tableID + 1))
                elif isinstance(object, RollingBall):
                    self.cursor.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (object.obj.rolling_ball.number, object.obj.rolling_ball.pos.x, object.obj.rolling_ball.pos.y, object.obj.rolling_ball.vel.x, object.obj.rolling_ball.vel.y))
                    self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (self.cursor.lastrowid, tableID + 1))
                

            self.connection.commit()
            #self.cursor.close()
            #self.connection.commit()
            # self.connection.close()
            return tableID
        except Exception as e:
            self.connection.rollback()
        finally:
            self.cursor.close()

    #Close Method
    def close( self ):
        self.connection.commit()
        self.connection.close()
    #Get Game, by retrieving players and gamename from the gameID
    def getGame( self, gameID ):
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT GAMENAME FROM Game WHERE GAMEID = (?)", (gameID,))
            gameName = self.cursor.fetchone()

            self.cursor.execute("SELECT PLAYERNAME FROM Player WHERE GAMEID = (?)", (gameID,))
            players = self.cursor.fetchall()

            self.connection.commit()
            self.cursor.close()
            
            return gameName, players
    #Setting Game, by inserting the game name and player names
    def setGame( self, gameName, player1Name, player2Name ):
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player1Name, gameID))
        self.cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player2Name, gameID))

        self.connection.commit()
        self.cursor.close()
        return gameID
    #Get the playerID of the certain player who is shooting
    def getPlayerID( self, playerName, gameID):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = (?) AND GAMEID = (?)", (playerName, gameID))
        playerID = self.cursor.fetchone()
        if playerID is not None:
            self.connection.commit()
            self.cursor.close()
            return playerID[0]
        else:
            raise ValueError("Player was not found.")
    #Inserting data as this represents of a shot being taken
    def newShot( self, playerID, gameID ):
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID, gameID))
        shotID = self.cursor.lastrowid
        self.connection.commit()
        self.cursor.close()
        return shotID
    #Inserting the ShotID and more data on the shot in the TableShot table
    def tableShotInsert( self, shotID, tableID):
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO TableShot (SHOTID, TABLEID) VALUES (?, ?)", (shotID, tableID))
        self.connection.commit()
        self.cursor.close()
#Game Class
class Game():
    #Getter for retrieving data
    def retrieveData(self, gameID):
        gameID += 1
        gameName, players = self.db.getGame(gameID)
        if gameName and players is not None:
            return gameName, players
        else:
            raise TypeError("The Game was not found in the database")
    #Constructor
    def __init__( self, gameID = None, gameName = None, player1Name = None, player2Name = None ):
        #Scenario One, where game ID is given, get the data and then set it to the self variables.
        if(gameID is not None and gameName is None and player1Name is None and player2Name is None):
            self.db = Database()
            self.db.createDB()
            retrievedGameName, players = self.retrieveData(gameID)
            gameName = retrievedGameName
            player1Name = players[0]
            player2Name = players[1]
        #Scenario 2 Where a new game needs to be set
        elif(gameID is None and gameName is not None and player1Name is not None and player2Name is not None):
            self.db = Database(reset=True)
            self.db.createDB()
            gameID = self.db.setGame( gameName=gameName, player1Name=player1Name, player2Name=player2Name) - 1
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
        else:
            raise TypeError("Invalid Constructor Arguments")
        self.gameID = gameID
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name
    
    def getTableID( self, shotID):
        connection = sqlite3.connect("phylib.db")
        cursor = connection.cursor()

        cursor.execute('''SELECT TABLEID FROM TableShot WHERE SHOTID = (?)''', (shotID,))
        tableID = cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()
        return tableID
    
    def checkCount(self):
        conn = sqlite3.connect('phylib.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM TTable")

        row_count = cursor.fetchone()[0]

        return row_count


    #Shoot Method
    def shoot( self, gameName, playerName, table, xvel, yvel):
        #Getting PlayerID for the player that is shooting
        playerID = self.db.getPlayerID(playerName=playerName, gameID=self.gameID + 1)
        shotID = self.db.newShot(playerID, self.gameID)
        cue_ball = None
        iteration = 0
        #Loop to find the cueBall
        for item in table:
            #print(item)
            if isinstance(item, RollingBall) and item.obj.rolling_ball.number == 0:
                cue_ball = item
                
            elif isinstance(item, StillBall) and item.obj.still_ball.number == 0:
                cue_ball = item
                
            else:
                continue
        #Setting Cue Ball Stats/Data
        if cue_ball is not None:    
            cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        
            xpos = cue_ball.obj.still_ball.pos.x
            ypos = cue_ball.obj.still_ball.pos.y

            cue_ball.obj.rolling_ball.pos.x = xpos
            cue_ball.obj.rolling_ball.pos.y = ypos


            cue_ball.obj.rolling_ball.vel.x = xvel
            cue_ball.obj.rolling_ball.vel.y = yvel
            cue_ball.obj.rolling_ball.number = 0
            velocityCoord = Coordinate(xvel, yvel)
            speed = phylib.phylib_length(velocityCoord)
            if speed > VEL_EPSILON:
                cue_ball.obj.rolling_ball.acc.x = (-cue_ball.obj.rolling_ball.vel.x / speed) * DRAG
                cue_ball.obj.rolling_ball.acc.y = (-cue_ball.obj.rolling_ball.vel.y / speed) * DRAG
            else:
                cue_ball.obj.rolling_ball.acc.x = 0.0
                cue_ball.obj.rolling_ball.acc.y = 0.0
            #Setting cueBall in the table with the new data
            for item in table:
                if isinstance(item, RollingBall):
                    if(item.obj.rolling_ball.number == 0):
                        item = cue_ball
                        
                elif isinstance(item, StillBall):
                    if(item.obj.still_ball.number == 0):
                        item = cue_ball
		# First, let's start the segment loop:
			# Run the segment

			# Get the time difference the time difference between tables

			# Decide how many frames

			# Loop over frames
				# Get time since start of segment (frame number * interval)
				# Create a new table using roll() with this time, using the table from the prev. segment
				# Set new table's time to the time in this frame
				# Write this new table to the database (dont forget to record in TableShot)
            totalFrames = 0
            table2 = table
            # count = 0
            #Loops to simulate the rolling of the ball when it shoots.
            while table is not None and table2 is not None:
                count = 0
                #First do a segment
                table2 = table.segment()
                #Find Time between the segments
                try:
                    deltaTime = table2.time - table.time
                except Exception as e:
                    break

                #Frames calculations
                frames = deltaTime / FRAME_INTERVAL
                frames = math.floor(frames)
                totalFrames = frames + totalFrames
                #print("Total Frames: ", totalFrames)
                #Apply roll from the frames that happended in the segment
                for i in range(frames):
                    #Apply roll with rollTime on the previous table and set it equal to frameTable
                    rollTime = i * FRAME_INTERVAL
                    frameTable = table.roll(rollTime)
                    frameTable.time = rollTime + table.time
                    #Write and save the data to resepective tables
                    tableID = self.db.writeTable(frameTable)
                    self.db.tableShotInsert(shotID, tableID)
                #Set table to table2
                tableID = self.db.writeTable(table2)
                self.db.tableShotInsert(shotID, tableID)
                table = table2
                for object in table:
                    if isinstance(object, RollingBall):
                        count += 1
                if count == 0:
                    break
                # rowCount = self.checkCount()
                iteration += 1
                if iteration > 8000:
                    return shotID
                # if(rowCount > 2000):
                #     return shotID

                # if iterate == 2:
                #     break
        # table = table.segment()
        return shotID

# if __name__ == "__main__":
#     print("Welcome.")
#     # createTables.ball()
#     # createTables.tTable()
#     # createTables.ballTable()
#     # createTables.shot()
#     # createTables.tableShot()
#     # createTables.game()
#     # createTables.player()
#     data = Database(True)
#     data.createDB()
#     #data.readTable(1)
