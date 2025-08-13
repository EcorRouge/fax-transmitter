from logging import Logger
from rococo.config import BaseConfig
from rococo.messaging import BaseServiceProcessor

from .faxing.base import FaxService
from .faxing.factory import fax_service_factory

logger = Logger(__name__)

class FaxServiceProcessor(BaseServiceProcessor):
    """
    Service processor that processes faxes
    """
    fax_service: FaxService

    def __init__(self):
        super().__init__()

        config = BaseConfig()
        self.fax_service = fax_service_factory.get(**config.get_env_vars())
        assert self.fax_service is not None

    def process(self, message):
        logger.info("Received message: %s to the fax transmitter service!", message)
        self.fax_service.send_fax(message)
