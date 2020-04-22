# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from proto import water_pb2 as proto_dot_water__pb2


class WaterDataStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetWater = channel.unary_unary(
                '/WaterData/SetWater',
                request_serializer=proto_dot_water__pb2.WateringRequest.SerializeToString,
                response_deserializer=proto_dot_water__pb2.EmptyResponse.FromString,
                )
        self.GetWater = channel.unary_unary(
                '/WaterData/GetWater',
                request_serializer=proto_dot_water__pb2.GetWaterRequest.SerializeToString,
                response_deserializer=proto_dot_water__pb2.WaterResponse.FromString,
                )


class WaterDataServicer(object):
    """Missing associated documentation comment in .proto file"""

    def SetWater(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWater(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WaterDataServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetWater': grpc.unary_unary_rpc_method_handler(
                    servicer.SetWater,
                    request_deserializer=proto_dot_water__pb2.WateringRequest.FromString,
                    response_serializer=proto_dot_water__pb2.EmptyResponse.SerializeToString,
            ),
            'GetWater': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWater,
                    request_deserializer=proto_dot_water__pb2.GetWaterRequest.FromString,
                    response_serializer=proto_dot_water__pb2.WaterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'WaterData', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WaterData(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def SetWater(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WaterData/SetWater',
            proto_dot_water__pb2.WateringRequest.SerializeToString,
            proto_dot_water__pb2.EmptyResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetWater(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WaterData/GetWater',
            proto_dot_water__pb2.GetWaterRequest.SerializeToString,
            proto_dot_water__pb2.WaterResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
