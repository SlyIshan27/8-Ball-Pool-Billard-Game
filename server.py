#Server py file
#Imports
import sys
import cgi
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import Physics
import phylib
import os
from urllib.parse import urlparse, parse_qsl;
#Handler Class
class handler(BaseHTTPRequestHandler):
    #GET function
    def do_GET(self):
        #print("Hello")
        #Parsing shoot.html
        parsed = urlparse(self.path)
        if parsed.path in [ '/shoot.html']:
	    #reading the file(shoot.html) in binary
            fp = open('.'+ self.path, 'rb')
            #content = fp.read()
            #Send 200 response for OK, and setting content type header
            self.send_response(200)
            self.send_header( "Content-type", "text/html" )
            #self.send_header( "Content-length", len( content ) )
            self.end_headers()
            #writing the file content to the response, indicate get of html website
            self.wfile.write(fp.read())
            fp.close()
        #If parsed parth is a table svg file
        elif parsed.path.startswith("/table-") and parsed.path.endswith('.svg'):
            #Open for reading in binary
            fp = open('.'+ self.path, 'rb')
            #Sending 200 ok response and header content type
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.end_headers()
            #Writing file content to the response, this is used to indicate get of table images
            self.wfile.write(fp.read())
	#Else error response
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ))
    #Post function
    def do_POST(self):
        parsed = urlparse(self.path)
        #Parsing for display.html site where all the content is displayed given information
        if parsed.path in ['/display.html']:
            #This is helping get the information from shoot.html
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={ 'REQUEST_METHOD': 'POST',
                                                                                   'CONTENT_TYPE': self.headers['Content-Type']})
            #Removing old svg files from directory
            for svg in os.listdir('.'):
                if svg.startswith("table-") and svg.endswith(".svg"):
                    os.remove(svg)

            #speed = Physics.Coordinate(0.0, 0.0)
            #Calculating Acceleration by getting informate from the shoot.html website
            velocityCoord = Physics.Coordinate(0.0, 0.0)
            velocityCoord.x =  float(form.getvalue('rb_dx'))
            velocityCoord.y = float(form.getvalue('rb_dy'))
            accelerationCoord = Physics.Coordinate(0.0, 0.0)
            speed = phylib.phylib_length(velocityCoord)
            if(speed > Physics.VEL_EPSILON):
                accelerationCoord.x = (-velocityCoord.x / speed) * Physics.DRAG
                accelerationCoord.y = (-velocityCoord.y / speed) * Physics.DRAG
            
            table = Physics.Table()
            
            #Getting more information to add the balls to the table I just created using the form
            #Getting Still Ball info
            sbNumber = int(form.getvalue('sb_number'))
            sbPos = Physics.Coordinate(0.0, 0.0)
            sbPos.x = float(form.getvalue('sb_x'))
            sbPos.y = float(form.getvalue('sb_y'))

            stillBall = Physics.StillBall(sbNumber, sbPos)

            table += stillBall
            #Getting Rolling Ball Info
            rbNumber = int(form.getvalue('rb_number'))
            rbPos = Physics.Coordinate(0.0, 0.0)
            rbPos.x = float(form.getvalue('rb_x'))
            rbPos.y = float(form.getvalue('rb_y'))

            rollingBall = Physics.RollingBall(rbNumber, rbPos, velocityCoord, accelerationCoord)
            table += rollingBall
            index = 0
            # with open("table-%d.svg" % index, "w") as file:
            #     file.write(table.svg())
            # index += 1
            #Generating new svg images for the tables, by applying segment to update the table
            while table:
                with open("table-%d.svg" % index, "w") as file:
                    file.write(table.svg())
                index += 1
                table = table.segment()
                

            #Some HTML strings I used to show the original stats of the balls, later gets prepended to another string
            contentHTML = "<h3>Rolling Ball Original Stats: Pos x: %.2f, Pos y: %.2f, Velocity x: %.2f, Velocity y: %.2f</h4>\n" % (rbPos.x, rbPos.y, velocityCoord.x, velocityCoord.y)
            contentHTML += "<h3>Still Ball Original Stats: Pos x: %.2f, Pos y: %.2f</h4>\n" % (sbPos.x, sbPos.y)
            #altText = ""
            index = 0
            iterate = True
            #While loop to get the html strings of the new svg files
            while(iterate):
                svgCode = "table-%d.svg" % index
                if svgCode in os.listdir('.'):
                    contentHTML += '<h3>Segment %d:</h3> \n' % index
                    contentHTML += '<img src="'
                    contentHTML += svgCode
                    contentHTML += '" alt="table-picture">\n'
                    index += 1
                else:
                    break 
            # for svgCode in os.listdir('.'):
            #     if(svgCode.startswith("table-%d" % index)):
            #         imgHTML += '<img src="'
            #         imgHTML += svgCode
            #         imgHTML += '" alt="table-picture">\n'
            #         index += 1
            #print(imgHTML)
            #Rest of the htmlCode strings, to display the image and website, and its contents
            htmlCode = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Display Tables</title>
                <style>
                    #content{
                        background-color: lightblue;
                        border: 4px solid lightgrey;
                        border-radius:4px;
                        text-align: center;
                        align-items: center;
                        font-family: 'Calibri', 'Sans-Serif'
                    }

                    #endContent{
                        background-color: skyblue;
                        border: 4px solid lightgrey;
                        border-radius:4px;
                        align-items: center;
                        text-align:center;
                        margin-top: 5px;
                    }
                
                </style>
            </head> """
            body = """
            <body>
                <div id="content">
                    <h1 style="font-family: 'Calibri', 'Sans-Serif'">Pool Table Segments</h1>
                     """
            body2 = """
                    <h3>End Of Segments</h3>
                    <button onclick="history.back()" style="width: 100px; height:40px; border: 1px solid lightgrey; border-radius: 2px"; margin-bottom: 100px;><a href="/shoot.html" style="text-decoration: none">Back to Shoot</a></button>
                </div>
            </body>
            </html>
            """
            #Appending everything
            htmlCode += body
            htmlCode += contentHTML
            #htmlCode += "</div>"
            htmlCode += body2

            #print(htmlCode)

            # Sending response to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(htmlCode.encode('utf-8'))

#Local host code for custom port, stays open forever until someone terminantes it.
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), handler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
