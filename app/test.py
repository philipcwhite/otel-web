import sqlite3

class Data:
    def __init__(self):
        self.con = sqlite3.connect('flask.db')
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def get_metrics(self):
        sql = "SELECT json_extract(json,'$.resourceMetrics[0].resource.attributes[0].value.stringValue') as hostname from metrics;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics2(self):
        sql = "SELECT distinct json_extract(value, '$.value.stringValue') as hostname from metrics, json_tree(metrics.json, '$.resourceMetrics') where type='object' and json_extract(value, '$.key') = 'host.name';" 
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

'''
select json_extract( value, '$.comments' ) as Comments,
       json_extract( value, '$.data' ) as Data,
       json_extract( value, '$.pod' ) as POD
  from datatable, json_tree( datatable.data, '$.ALL' )
 where type = 'object'
   and json_extract( value, '$.pod' ) = 'fb' ;
   '''



D = Data()

print(D.get_metrics2())
