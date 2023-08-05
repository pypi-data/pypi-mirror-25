import os
import logging
import importlib


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_base_loggername(metadata):
    return 'packtivity_logger_{}'.format(metadata['name'])

def get_topic_loggername(metadata,topic):
    return 'packtivity_logger_{}.{}'.format(metadata['name'],topic)

def setup_logging(metadata,state):
    ## prepare logging for the execution of the job. We're ready to handle up to DEBUG
    log = logging.getLogger(get_base_loggername(metadata))
    log.setLevel(logging.DEBUG)

    fh  = logging.StreamHandler()
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ## this is all internal logging, we don't want to escalate to handlers of parent loggers
    ## we will have two handlers, a stream handler logging to stdout at INFO
    log.propagate = False
    setup_logging_topic(metadata,state,'step')

def default_logging_handlers(log,metadata,state,topic):
    if topic == 'step':
        fh  = logging.StreamHandler()
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    # Now that we have  place to store meta information we put a file based logger in place
    # to log at DEBUG
    logname = '{}/{}.{}.log'.format(state.metadir,metadata['name'],topic)
    fh  = logging.FileHandler(logname)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)

def setup_logging_topic(metadata,state,topic,return_logger = False):
    log = logging.getLogger(get_topic_loggername(metadata,topic))
    log.propagate = False

    if log.handlers:
        return log if return_logger else None

    customhandlers = os.environ.get('PACKTIVITY_LOGGING_HANDLER')
    if customhandlers:
        module,func = customhandlers.split(':')
        m = importlib.import_module(module)
        f = getattr(m,func)
        f(log,metadata,state,topic)
    else:
        default_logging_handlers(log,metadata,state,topic)    
    if return_logger:
        return log
