#!env/Scripts/python

import sys
import asyncio
from concurrent.futures import ProcessPoolExecutor

from reverse.bot import Bot

_reverse = Bot(description="The Reverse", command_prefix="!", pm_help = False)
_reverse.run(*sys.argv[1:])
