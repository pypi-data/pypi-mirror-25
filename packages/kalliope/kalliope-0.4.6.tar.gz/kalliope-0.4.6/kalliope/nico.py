# coding: utf8
import logging

from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core.ConfigurationManager import BrainLoader, SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

brain = BrainLoader().get_brain()
settings = SettingLoader().settings

# order = "say hello to Bruno"
order = "je veux que tu dis bonjour à nico"
SynapseLauncher.run_matching_synapse_from_order(order_to_process=order,
                                                brain=brain,
                                                settings=settings)





