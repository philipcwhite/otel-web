from google.protobuf.json_format import MessageToJson
from concurrent import futures
import grpc, logging, sqlite3, time, json

from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceResponse
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2_grpc
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceResponse
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2_grpc
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceResponse
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2_grpc


class Data:
    def __init__(self):
        self.con = sqlite3.connect('flask.db')
        self.cursor = self.con.cursor()
        self.timestamp = int(str(time.time()).split('.')[0])
    def __del__(self):
        self.con.close()
    def insert_metrics_json(self, hostname, resource, scopemetrics):
        sql = "insert into metrics (timestamp, hostname, resource, scopemetrics) values (?, ?, ?, ?);"
        self.cursor.execute(sql, (self.timestamp, hostname, resource, scopemetrics))
        self.con.commit()
    def insert_logs_json(self, packet):
        sql = "insert into logs (timestamp, data) values(?, ?)"
        self.cursor.execute(sql, (self.timestamp, packet))
        self.con.commit()
    def insert_trace_json(self, packet):
        sql = "insert into traces (timestamp, data) values(?, ?)"
        self.cursor.execute(sql, (self.timestamp, packet))
        self.con.commit()


class MetricsServiceServicer(metrics_service_pb2_grpc.MetricsServiceServicer):
    def Export(self, request, context):
        packet=MessageToJson(request)
        jdata = json.loads(str(packet))
        '''for i in jdata["resourceMetrics"]:
            hostname = None
            attributes = i["resource"]["attributes"]
            scopemetrics = i["scopeMetrics"]
            for i in attributes:
                if i["key"] == "host.name":
                    hostname = i["value"]["stringValue"]
            for i in scopemetrics:
                attributes = json.dumps(attributes)
                metrics = json.dumps(i["metrics"])
                print(hostname, attributes, metrics, "\n")'''

        for i in jdata["resourceMetrics"]:
            hostname = None
            resource = i["resource"]
            scopemetrics = i["scopeMetrics"]
            for i in resource["attributes"]:
                if i["key"] == "host.name":
                    hostname = i["value"]["stringValue"]
            for i in scopemetrics:
                resource = json.dumps(resource)
                scopemetrics = json.dumps(i)
                print(hostname, resource, scopemetrics, "\n")
                #D = Data()
                #D.insert_metrics_json(hostname, resource, scopemetrics)
            D=Data()
            D.insert_metrics_json(hostname, "", packet)
        
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return ExportMetricsServiceResponse()

class LogsServiceServicer(logs_service_pb2_grpc.LogsServiceServicer):
    def Export(self, request, context):
        packet=MessageToJson(request)
        print(packet)
        D = Data()
        D.insert_logs_json(packet)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return ExportLogsServiceResponse()

class TraceServiceServicer(trace_service_pb2_grpc.TraceServiceServicer):
    def Export(self, request, context):
        packet=MessageToJson(request)
        print(packet)
        D = Data()
        D.insert_trace_json(packet)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return ExportTraceServiceResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metrics_service_pb2_grpc.add_MetricsServiceServicer_to_server(MetricsServiceServicer(), server)
    logs_service_pb2_grpc.add_LogsServiceServicer_to_server(LogsServiceServicer(), server)
    trace_service_pb2_grpc.add_TraceServiceServicer_to_server(TraceServiceServicer(), server)
    server.add_insecure_port('[::]:7777')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
