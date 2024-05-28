import ping_pb2, ping_pb2_grpc, grpc
from concurrent import futures
import interceptor

class PingServicer(ping_pb2_grpc.PingServicer):
    def __init__(self):
        return None

    def Ping(self, request, context):
        print(context.peer())
        return ping_pb2.Message(args="Pong")

    def Bang(self, request, context):
        return ping_pb2.Message(args="Bong")

interceptors = (
    interceptor.MyInterceptor(),
    )

server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10),
    interceptors=interceptors
    )

ping_pb2_grpc.add_PingServicer_to_server(PingServicer(), server)

server.add_insecure_port("127.0.0.1:50051")
server.start()
server.wait_for_termination()
