# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from proto import plant_pb2 as proto_dot_plant__pb2


class PlantDataStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePlant = channel.unary_unary(
                '/PlantData/CreatePlant',
                request_serializer=proto_dot_plant__pb2.Plant.SerializeToString,
                response_deserializer=proto_dot_plant__pb2.PlantResponse.FromString,
                )
        self.UpdatePlant = channel.unary_unary(
                '/PlantData/UpdatePlant',
                request_serializer=proto_dot_plant__pb2.UpdatePlantRequest.SerializeToString,
                response_deserializer=proto_dot_plant__pb2.PlantResponse.FromString,
                )
        self.GetPlants = channel.unary_unary(
                '/PlantData/GetPlants',
                request_serializer=proto_dot_plant__pb2.EmptyRequest.SerializeToString,
                response_deserializer=proto_dot_plant__pb2.PlantArrayResponse.FromString,
                )


class PlantDataServicer(object):
    """Missing associated documentation comment in .proto file"""

    def CreatePlant(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePlant(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPlants(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PlantDataServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreatePlant': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePlant,
                    request_deserializer=proto_dot_plant__pb2.Plant.FromString,
                    response_serializer=proto_dot_plant__pb2.PlantResponse.SerializeToString,
            ),
            'UpdatePlant': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePlant,
                    request_deserializer=proto_dot_plant__pb2.UpdatePlantRequest.FromString,
                    response_serializer=proto_dot_plant__pb2.PlantResponse.SerializeToString,
            ),
            'GetPlants': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPlants,
                    request_deserializer=proto_dot_plant__pb2.EmptyRequest.FromString,
                    response_serializer=proto_dot_plant__pb2.PlantArrayResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PlantData', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PlantData(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def CreatePlant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PlantData/CreatePlant',
            proto_dot_plant__pb2.Plant.SerializeToString,
            proto_dot_plant__pb2.PlantResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdatePlant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PlantData/UpdatePlant',
            proto_dot_plant__pb2.UpdatePlantRequest.SerializeToString,
            proto_dot_plant__pb2.PlantResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPlants(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PlantData/GetPlants',
            proto_dot_plant__pb2.EmptyRequest.SerializeToString,
            proto_dot_plant__pb2.PlantArrayResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)