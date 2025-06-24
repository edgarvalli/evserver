import sys
from pathlib import Path

cwd = Path(__file__).parent.parent
sys.path.append(str(cwd))

from utils.dbtool import rebuild

rebuild()