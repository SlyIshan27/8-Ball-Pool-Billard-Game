import math;
import random;

import Physics;

class creationOfIntialTable():

    def nudge(self):
        return random.uniform( -1.5, 1.5 );

    def createIntialTable(self):
        table = Physics.Table()

        # 1 ball
        pos = Physics.Coordinate( 
        Physics.TABLE_WIDTH / 2.0,
        Physics.TABLE_WIDTH / 2.0,
        )

        sb = Physics.StillBall( 1, pos );
        table += sb

        # 2 ball
        pos = Physics.Coordinate(
        Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 +
        self.nudge(),
        Physics.TABLE_WIDTH/2.0 - 
        math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
        self.nudge()
        )
        sb = Physics.StillBall( 2, pos )
        table += sb;

        # 3 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 3, pos );
        table += sb;

        # 4 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0) +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 4, pos );
        table += sb;

        # 5 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 5, pos );
        table += sb;

        # 6 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0) +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 6, pos );
        table += sb;

        # 7 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)*3/2 +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        1.5*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 7, pos );
        table += sb;

        # 8 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2 +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        1.5*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 8, pos );
        table += sb;

        # 9 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2 +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        1.5*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 9, pos );
        table += sb;

        # 10 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)*3/2 +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        1.5*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 10, pos );
        table += sb;

        # 11 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 - 2*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        2*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 11, pos );
        table += sb;

        # 12 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0) +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        2*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 12, pos );
        table += sb;

        # 13 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0,
                        Physics.TABLE_WIDTH/2.0 -
                        2*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 13, pos );
        table += sb;

        # 14 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0) +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        2*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 14, pos );
        table += sb;

        # 15 ball
        pos = Physics.Coordinate(
                        Physics.TABLE_WIDTH/2.0 + 2*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge(),
                        Physics.TABLE_WIDTH/2.0 -
                        2*math.sqrt(3.0)*(Physics.BALL_DIAMETER+4.0) +
                        self.nudge()
                        );
        sb = Physics.StillBall( 15, pos );
        table += sb;

        # cue ball also still
        pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                                Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
        sb  = Physics.StillBall( 0, pos );

        table += sb;


        with open("intialTable.svg", "w") as file:
            file.write(table.svg())

        return table