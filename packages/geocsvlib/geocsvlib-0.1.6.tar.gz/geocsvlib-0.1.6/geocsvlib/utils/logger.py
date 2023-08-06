"""
Application wide logger, could have used module based but making it trivial to re-implement



Logger module uses static programming language type syntax i.e. camelCase,
don't know why they decided on that
but to keep the variables consistent naming convention follows
the camelCase antecedent

Logging will be stored in a log server eventually where all logs
can be viewed as required, this is why
the name of the application is important
"""
import os
import logging

#: Get the environmental configuration or currently configured config
currentConfig = "Development"

#: Necessary to differentiate these logs from logs from other micro services
#: especially when used by the service monitor to trace request path
applicationName = "Parsito"
logLevel = logging.INFO


logger = logging.getLogger(applicationName)
logger.setLevel(logLevel)

#: This can be redirected elsewhere for log recording
loggerHandler = logging.FileHandler(filename='application.log')
loggerHandler.setLevel(logLevel)

format_schema = '%(asctime)s -:::- %(name)s -:::- %(levelname)s -:::- %(message)s'
loggerFormatter = logging.Formatter(format_schema)
loggerHandler.setFormatter(loggerFormatter)


logger.addHandler(loggerHandler)


def message_logger(message, cause, reason=None):
    """
    Formats the message to a consistent format by logging the error and the causing client

    :param message:     The message to be formatted and worked upon
                        :type <type, 'str'>

    :param cause:       The cause of the message being logged, it can for instance be The ip address
                        of the client or transaction ID or operation description.
                        :type <type, 'str'>

    :param reason:      Short string prepositions that tie the relationship of the cause to the message
                        could be limited to any of the following values ['by', 'when', 'in']
                        :type <type, 'str'>

    :return message:    Properly formatted message consistent with the type necessary to provide best
                        information when inspected from a log file or log server whichever is used
                        :type <type, 'str'>
    """
    if not reason:
        reason = 'Error BY'

    message = '{0} : {2} {1}'.format(message, cause, reason)
    return message
