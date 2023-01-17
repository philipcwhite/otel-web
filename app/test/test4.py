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
    
    def get_metrics8(self):
        sql = "SELECT json_extract(scopemetrics, ('$.metrics[0].description')) as name from metrics where id==1;" # and json_extract(value, '$.key') = 'host.name';"
        #self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    def get_metrics9(self):
        sql = "SELECT json_extract(value, '$.name') as name from metrics, json_tree(metrics.scopemetrics, '$.metrics') where type='object' and name is not NULL;" # and metrics.id==19;" 
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics10(self):
        sql = "SELECT json_extract(value, '$.name') as name, json_extract(value, '$.gauge.dataPoints') as datapoints from metrics, json_tree(metrics.scopemetrics, '$.metrics') where type='object' and name=='system.cpu.load_average.1m';" # and metrics.id==19;" 
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics11(self):
        sql = "SELECT json_extract(value, '$.gauge.dataPoints') as datapoints from metrics, json_tree(metrics.scopemetrics, '$.metrics') where type='object' and json_extract(value, '$.name')=='system.cpu.load_average.1m';" # and metrics.id==19;" 
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics12(self):
        sql = "SELECT json_extract(value, '$.gauge.dataPoints[0].asDouble') as metric_value from metrics, json_tree(metrics.scopemetrics, '$.metrics') where type='object' and json_extract(value, '$.name')=='system.cpu.load_average.5m' and hostname=='fedora';" # and metrics.id==19;" 
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_metrics13(self):
        sql = "SELECT json_extract(value, '$.gauge.dataPoints[0].asDouble') as metric_value from metrics, json_tree(metrics.scopemetrics, '$.metrics') where type='object' and json_extract(value, '$.name')=='system.cpu.load_average.5m' and hostname=='fedora' ORDER BY metrics.id DESC LIMIT 10;" # and metrics.id==19;" 
        self.cursor.row_factory = self.dict_factory
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows



D = Data()

print("xxxxxxxxxxxxxxxxxx Metrics 8 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(D.get_metrics8())

print("xxxxxxxxxxxxxxxxxx Metrics 9 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(D.get_metrics9())

print("xxxxxxxxxxxxxxxxxx Metrics 10 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(D.get_metrics10())

print("xxxxxxxxxxxxxxxxxx Metrics 11a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(D.get_metrics11())

print("xxxxxxxxxxxxxxxxxx Metrics 11b xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
datapoints = D.get_metrics11()
for i in datapoints:
    print(i['datapoints'], type(i['datapoints']))

print("xxxxxxxxxxxxxxxxxx Metrics 12 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#hostname==fedora, name=system.cpu.load_average.5m
print(D.get_metrics12())
for i in D.get_metrics12():
    print(i['metric_value'], type(i))

print("xxxxxxxxxxxxxxxxxx Metrics 13 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#hostname==fedora, name=system.cpu.load_average.5m
print(D.get_metrics13())
for i in D.get_metrics13():
    print(i['metric_value'], type(i))




'''
print(D.get_metrics4())
data = json.loads(D.get_metrics4()[0])
for i in data:
    print(i)
    #print(i['key'] + ':' + i['value']['stringValue'])

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
'''

