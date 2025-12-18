import Physics;
import os;

class SVGWriter:
    def __init__(self, database):
        self.db = database
        
    def write_svg( self, table_id, table ):
        folderPath = "SVGS"
        if not os.path.isdir(folderPath):
            try:
                os.mkdir(folderPath)
            except FileNotFoundError:
                os.makedirs(folderPath)

        filePath = os.path.join(folderPath, "%d.svg" % table_id)
        with open( filePath, "w" ) as fp:
            fp.write( table.svg() );

    # db = Physics.Database();

    def writeAllSVGS(self):
        table_id = 0;
        table = self.db.readTable( table_id );

        self.write_svg( table_id, table );

        while table:
            table_id += 1;
            table = self.db.readTable( table_id );
            if not table:
                break;
            self.write_svg( table_id, table );

    def writeSVGS(self, tableID):
        table = self.db.readTable(tableID)
        # self.write_svg( tableID, table );
        while table:
            table = self.db.readTable(tableID)
            if table is None:
                break
            self.write_svg(tableID, table);
            tableID += 1
        # self.db.close();
