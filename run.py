#!env/Scripts/python

import sys
import asyncio
from concurrent.futures import ProcessPoolExecutor

from reverse.bot import Bot

# Create instance of Bot implementing Reverse
_reverse = Bot(description="The Reverse", command_prefix="-", pm_help = False)
_reverse.run(sys.argv[1])