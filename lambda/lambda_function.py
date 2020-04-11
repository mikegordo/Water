# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import json
import logging
from os import path
from typing import Union

import requests
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

SKILL_NAME = "Irrigation system"
WATERING_MESSAGE = "Okay, watering your plants."
HELP_MESSAGE = "You can say water my plants, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Irrigation System skill can't help you with that. It can help you water your plants. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."
FAILURE_MESSAGE = "Please check your configuration."
SERVER_ACCESS_MESSAGE = "It seems like I cannot access your server."
SUCCESS_MESSAGE = "Okay, watering your plants."

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class WaterMyPlantsHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    CONFIGURATION_FILENAME = "auth.json"
    POTS = [1, 2]

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("WaterMyPlantsHandler")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        config = self.get_configuration()
        if not config:
            logger.info('Config is empty')
            speech = FAILURE_MESSAGE
        elif 'endpoint' not in config or 'token' not in config:
            logger.info('Config incomplete')
            speech = FAILURE_MESSAGE
        else:
            speech = self.apicall(config, self.POTS)

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response

    def get_configuration(self, filename=None) -> Union[dict, None]:
        if not filename:
            filename = self.CONFIGURATION_FILENAME
        if not path.exists(filename):
            logger.info(f'File {filename} cannot be found.')
            return
        try:
            with open(filename, 'r') as f:
                content = json.load(f)
                return content
        except Exception as e:
            logger.error(e)
            return

    def apicall(self, config, pots):
        if not config or 'endpoint' not in config or 'token' not in config:
            return FAILURE_MESSAGE
        if not pots:
            return FAILURE_MESSAGE

        msgs = []
        for p in pots:
            logger.info(f'pot {p} in line')
            endpoint = config['endpoint']
            endpoint = endpoint.replace('{pot}', str(p))
            logger.info(f'got endpoint {endpoint}')
            r = None
            try:
                r = requests.post(url=endpoint, headers={'Authorization': 'Token {}'.format(config['token'])})
                if not r:
                    return SERVER_ACCESS_MESSAGE
            except Exception as e:
                logger.error(e)
                return SERVER_ACCESS_MESSAGE

            logger.info(r)
            msgs.append(f'pot {p}')

        logger.info(msgs)
        return SUCCESS_MESSAGE


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input) or \
               is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
            SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(WaterMyPlantsHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
