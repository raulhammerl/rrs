import csv 

# home made  
import Database

def read_channel_metadata(self, channel_id):
        with open(self.csv_file, mode='r', encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    name = row[0].replace(" ","")
                    genre = row[1].replace(".","/").replace(":","/")
                    target_group = row[3].replace(" ","")
                    feature = row[4].replace(" ","")
                    array.append(name)
                    channel = (
                        name,
                        "",
                        "de",
                        stream_url,
                        radiodns_url
                    )
                    self.create_channel(channel)
                    line_count += 1
            print(f'Processed {line_count} lines.')




def add_columns():
  addColumn = "ALTER TABLE {} ADD COLUMN {} varchar(32)".format(table, column)