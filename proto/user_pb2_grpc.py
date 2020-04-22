# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from proto import user_pb2 as proto_dot_user__pb2


class UserDataStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateUser = channel.unary_unary(
                '/UserData/CreateUser',
                request_serializer=proto_dot_user__pb2.BasicUser.SerializeToString,
                response_deserializer=proto_dot_user__pb2.UserResponse.FromString,
                )
        self.UpdateUser = channel.unary_unary(
                '/UserData/UpdateUser',
                request_serializer=proto_dot_user__pb2.UpdateUserRequest.SerializeToString,
                response_deserializer=proto_dot_user__pb2.UserResponse.FromString,
                )
        self.AuthenticateUser = channel.unary_unary(
                '/UserData/AuthenticateUser',
                request_serializer=proto_dot_user__pb2.BasicUser.SerializeToString,
                response_deserializer=proto_dot_user__pb2.UserResponse.FromString,
                )
        self.GetUser = channel.unary_unary(
                '/UserData/GetUser',
                request_serializer=proto_dot_user__pb2.TokenRequest.SerializeToString,
                response_deserializer=proto_dot_user__pb2.UserResponse.FromString,
                )


class UserDataServicer(object):
    """Missing associated documentation comment in .proto file"""

    def CreateUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AuthenticateUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserDataServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateUser,
                    request_deserializer=proto_dot_user__pb2.BasicUser.FromString,
                    response_serializer=proto_dot_user__pb2.UserResponse.SerializeToString,
            ),
            'UpdateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateUser,
                    request_deserializer=proto_dot_user__pb2.UpdateUserRequest.FromString,
                    response_serializer=proto_dot_user__pb2.UserResponse.SerializeToString,
            ),
            'AuthenticateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AuthenticateUser,
                    request_deserializer=proto_dot_user__pb2.BasicUser.FromString,
                    response_serializer=proto_dot_user__pb2.UserResponse.SerializeToString,
            ),
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=proto_dot_user__pb2.TokenRequest.FromString,
                    response_serializer=proto_dot_user__pb2.UserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'UserData', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserData(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def CreateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserData/CreateUser',
            proto_dot_user__pb2.BasicUser.SerializeToString,
            proto_dot_user__pb2.UserResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserData/UpdateUser',
            proto_dot_user__pb2.UpdateUserRequest.SerializeToString,
            proto_dot_user__pb2.UserResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AuthenticateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserData/AuthenticateUser',
            proto_dot_user__pb2.BasicUser.SerializeToString,
            proto_dot_user__pb2.UserResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserData/GetUser',
            proto_dot_user__pb2.TokenRequest.SerializeToString,
            proto_dot_user__pb2.UserResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)