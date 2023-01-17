import sqlite3, json


class Data:
    def __init__(self):
        self.con = sqlite3.connect('flask.db')
        #self.con.row_factory = sqlite3.Row
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def get_metrics(self):
        sql = "SELECT json_extract(json,'$.resourceMetrics[0].resource.attributes[0].value.stringValue') as hostname from metrics;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics2(self):
        sql = "SELECT distinct json_extract(value, '$.value.stringValue') as hostname from metrics, json_tree(metrics.data, '$.resourceMetrics') where type='object' and json_extract(value, '$.key') = 'host.name';" 
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics3(self):
        sql = "SELECT DISTINCT json_extract(json,'$.resourceMetrics[0].resource.attributes') as attributes from metrics;" 
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0]

    def get_metrics4(self):
        sql = "SELECT distinct json_extract(value, '$.resource.attributes') as attributes from metrics, json_tree(metrics.data, '$.resourceMetrics') where type='object';" 
        self.cursor.row_factory=sqlite3.Row
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics5(self):
        sql = "SELECT distinct json_extract(value, '$.resource.attributes') as attributes from metrics, json_tree(metrics.data, '$.resourceMetrics') where type='object';" 
        self.cursor.row_factory=sqlite3.Row
        self.cursor.execute(sql)
        for row in self.cursor:
            print(row[0])

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_metrics6(self):
        sql = "SELECT DISTINCT json_extract(value, '$.resource.attributes') as attributes from metrics, json_tree(metrics.data, '$.resourceMetrics') where type='object' and attributes is not NULL;"  
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics7(self):
        sql = "SELECT distinct json_extract(value, '$.metrics') as metric_data, json_extract(value, '$.value.stringValue') as hostname from metrics, json_tree(metrics.data, '$.resourceMetrics') where json_tree.resource.attributes.value.stringValue = 'fedora2';" 
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    '''
    SELECT DISTINCT json_extract(big.json,'$.id')
  FROM big, json_tree(big.json, '$.partlist')
 WHERE json_tree.key='uuid'
   AND json_tree.value='6fa5181e-5721-11e5-a04e-57f3d7b32808';
    '''

'''
select json_extract( value, '$.comments' ) as Comments,
       json_extract( value, '$.data' ) as Data,
       json_extract( value, '$.pod' ) as POD
  from datatable, json_tree( datatable.data, '$.ALL' )
 where type = 'object'
   and json_extract( value, '$.pod' ) = 'fb' ;
   '''



D = Data()

print(D.get_metrics4())

'''
data = json.loads(D.get_metrics4()[0])

for i in data:
    print(i)
    #print(i['key'] + ':' + i['value']['stringValue'])
'''


print("xxxxxxxxxxxxx Metrics Split xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


data = D.get_metrics4()

for i in data:
    print(i[0])

for i in data:
    #print(i)
    if not None in i:
        #print(i)
        #print(i['key'] + ':' + i['value']['stringValue'])
        s = json.loads(i[0])
        for t in s:
            print(t['key'] + ':' + t['value']['stringValue'])



print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(D.get_metrics5())

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

print(D.get_metrics6())

for i in D.get_metrics6():
    print(i)


print("xxxxxxxxxxxxxxxxxx Metrics 7 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

print(D.get_metrics7())

for i in D.get_metrics7():
    print(i)


print("xxxxxxxxxxxxxxxxxx Metrics 8 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

print(D.get_metrics2())



