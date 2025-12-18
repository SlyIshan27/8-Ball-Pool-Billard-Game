import sys
import cgi
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import Physics
from Physics import StillBall, Coordinate
import phylib
import os
from urllib.parse import urlparse, parse_qs;
import intialTable
import json
import SVGCreator
import shutil
import xml.etree.ElementTree as ET
import time
import random


initaltable = intialTable.creationOfIntialTable()
initaltable.createIntialTable()
table = Physics.Table()
table = initaltable.createIntialTable()
lastRowCount = 0
player1Name = None
player2Name = None
GameName = None
Game = Physics.Game(gameName="NULL", player1Name="NULL", player2Name="NULL")
if not os.path.isdir("SVGS"):
    os.mkdir("SVGS")
else:
    shutil.rmtree("SVGS")



def intialization():
    initaltable = intialTable.creationOfIntialTable()
    initaltable.createIntialTable()
    table = Physics.Table()
    table = initaltable.createIntialTable()
    return table

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    request_processed = False
    gameInfo_processed = False
    def __init__(self, request, client_address, server):
        # Call the superclass constructor with the required arguments
        super().__init__(request, client_address, server)
        # Initialize the table attribute
        self.table = intialization()
        self.firstShot = True
    def do_GET(self):
        parsed_path = urlparse(self.path)
        # Check if the requested path is for the HTML file
        if parsed_path.path == '/webpage.html':
            file_path = 'webpage.html'
        # Check if the requested path is for the SVG file
        elif parsed_path.path == '/intialTable.svg':
            file_path = 'intialTable.svg'
        # Check if the requested path is for the JavaScript file
        elif parsed_path.path == '/webpage.js':
            file_path = 'webpage.js'
        elif parsed_path.path == '/webpage.css':
            file_path = 'webpage.css'
        elif parsed_path.path == '/menu.html':
            file_path = 'menu.html'
        elif parsed_path.path == '/menu.css':
            file_path = 'menu.css'
        else:
            # If the requested path is not recognized, return a 404 Not Found response
            # self.send_response(404)
            # self.end_headers()
            # self.wfile.write(b'404 Not Found')
            # return
            file_path = 'menu.html'

        try:
            # Open the file in binary mode
            with open(file_path, 'rb') as file:
                # Send a response with a 200 OK status
                self.send_response(200)
                # Set the appropriate Content-Type header based on the file type
                if file_path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif file_path.endswith('.svg'):
                    self.send_header('Content-type', 'image/svg+xml')
                elif file_path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                # End headers
                self.end_headers()
                # Send the contents of the file
                self.wfile.write(file.read())
        except FileNotFoundError:
            # If the file is not found, send a 404 Not Found response
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    def do_POST(self):
        global GameName
        global player1Name
        global player2Name
        global table
        global Game
        global lastRowCount
        if self.path == '/initial-velocity':
            if not SimpleHTTPRequestHandler.request_processed:
                print("Hit")
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                initial_velocities = json.loads(post_data.decode('utf-8'))
                print(post_data)
                initialVelX = initial_velocities['initialVelX']
                initialVelY = initial_velocities['initialVelY']
                turn = initial_velocities['turn']
                print("Initial Velocity X:", initialVelX)
                print("Initial Velocity Y:", initialVelY)
                velocityCoord = Physics.Coordinate(initialVelX, initialVelY)
                velocityCoord.x = velocityCoord.x * 1
                velocityCoord.y = velocityCoord.y * 1
                accelerationCoord = Physics.Coordinate(0.0, 0.0)
                speed = phylib.phylib_length(velocityCoord)
                if(speed > Physics.VEL_EPSILON):
                    accelerationCoord.x = (-velocityCoord.x / speed) * Physics.DRAG
                    accelerationCoord.y = (-velocityCoord.y / speed) * Physics.DRAG
                print("Acceleration X: ", accelerationCoord.x)
                print("Acceleration Y: ", accelerationCoord.y)
                # Further processing of initial velocities can be done here
                # print(table)
                # print(player1Name)
                # print(player2Name)
                # print(GameName)
                name = None
                if(turn == 1):
                    name = player1Name
                else:
                    name = player2Name
                cueBallCheck = False
                for item in table:
                    if isinstance(item, StillBall) and item.obj.still_ball.number == 0:
                        cueBallCheck = True
                if not cueBallCheck:
                    table += StillBall(0, Coordinate(677.0, 2025.0))
                shotID = Game.shoot(GameName, name, table, velocityCoord.x, velocityCoord.y)
                oldRowCount = lastRowCount
                db = Physics.Database()
                svgFiles = SVGCreator.SVGWriter(db)
                svgDirectory = "SVGS"
                svgFiles.writeSVGS(lastRowCount)
                newRowCount = Game.checkCount()
                lastRowCount = newRowCount
                # db = Physics.Database()
                # svgFiles = SVGCreator.SVGWriter(db)
                # svgDirectory = "SVGS"
                # if not os.path.isdir(svgDirectory):
                #     os.mkdir(svgDirectory)
                # else:
                #     for f in os.listdir(svgDirectory):
                #         if f.endswith(".svg"):
                #             os.remove(os.path.join(svgDirectory, f))
                # svgFiles.writeAllSVGS()
                # print("Row Count: ", rowCount)
                table = db.readTable(newRowCount - 1)
                
                db.close()

                svgDirectory = "SVGS"
                svgList = []
                svgFilenames = [filename for filename in os.listdir(svgDirectory) if filename.endswith(".svg")]
                sortedfilenames = sorted(svgFilenames, key=lambda x: int(x.split('.')[0]))
                for i in range(oldRowCount, newRowCount):
                    filename = f"{i}.svg"
                    path = os.path.join(svgDirectory, filename)
                    print(filename)
                    if os.path.exists(path):
                        with open(path) as fp:
                            svgList.append(fp.read())
                # for filename in (sortedfilenames):
                #     if filename.endswith(".svg"):
                #         index = int(filename.split('.')[0])
                #         file_path = os.path.join(svgDirectory, filename)
                #         print(filename)
                #         if index >=0:
                #             with open(file_path, "r") as fp:
                #                 svgContent = fp.read()
                #                 # print("SVG Content for", filename, ": ", svgContent)
                #                 svgList.append(svgContent)
                
                # print(svgList[len(svgList) - 2])
                # svgList.pop()
                # rowCount = Game.checkCount()
                # for f in os.listdir(svgDirectory):
                #         if f.endswith(".svg"):
                #             os.remove(os.path.join(svgDirectory, f))
                
                    
                delimiter = "---"
                if not svgList:
                    path = os.path.join(svgDirectory, f"{newRowCount - 1}.svg")
                    with open(path) as fp:
                        svgList.append(fp.read())
                combinedSVGS = delimiter.join(svgList)
                # print(svgJSON)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(combinedSVGS.encode('utf-8'))
                # SimpleHTTPRequestHandler.request_processed = True
        elif self.path == '/process-shot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            svgString = json.loads(post_data.decode('utf-8'))
            # print(post_data)
            result = svgString['result']
            lastShot = ""
            for filename in os.listdir("SVGS"):
                if filename.endswith("0.svg"):
                    file_path = os.path.join("SVGS", filename)
                    with open(file_path, "r") as fp:
                        lastShot = fp.read()
            

            coloursLow = ["YELLOW", "BLUE", "RED", "PURPLE", "ORANGE", "GREEN", "BROWN"]
            coloursHigh = ["LIGHTYELLOW", "LIGHTBLUE", "PINK", "MEDIUMPURPLE", "LIGHTSALMON", "LIGHTGREEN", "SANDYBROWN"]
            foundLow = 0
            foundHigh = 0
            missing_balls = []
            returnStatement = ""
            
            for cL in coloursLow:
                if cL not in result:
                    foundLow = 1
            for cH in coloursHigh:
                if cH not in result:
                    foundHigh = 1

            
            if foundLow == 1 and foundHigh == 0:
                returnStatement = "LOW"
            elif foundHigh == 1 and foundLow == 0:
                returnStatement = "HIGH"
            elif foundHigh == 1 and foundLow == 1:
                randInt = random.randint(1,2)
                if randInt == 1:
                    returnStatement = "LOW"
                else:
                    returnStatement = "HIGH"
            else:
                returnStatement = "NONE"

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(returnStatement.encode('utf-8'))
            # print(result)
        elif self.path == '/submit-player-names':
            # Handling player names submission
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            GameName = form_data.get('gameName', [''])[0]
            player_one_name = form_data.get('player_one', [''])[0]
            player_two_name = form_data.get('player_two', [''])[0]
            print("Game Name: ", GameName)
            print("Player One:", player_one_name)
            print("Player Two:", player_two_name)
            #gameInfo = []
            player1Name = player_one_name
            player2Name = player_two_name
            Game = Physics.Game(gameName= GameName, player1Name=player1Name, player2Name=player2Name)
            # Redirect to the game page

            redirect_url = f'/webpage.html?player1Name={player1Name}&player2Name={player2Name}'
            self.send_response(303)  # Redirect status code
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            # If the requested path is not recognized, return a 404 Not Found response
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')


if __name__ == "__main__":
    intialization()
    httpd = HTTPServer(('localhost', int(sys.argv[1])), SimpleHTTPRequestHandler);
    print( "Server listing in port:  ", int(sys.argv[1]));
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()