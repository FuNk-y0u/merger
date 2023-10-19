# Terminal colors 
class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLACK = '\033[30m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_info(msg):
	print(f"{Colors.BLUE}[INFO]: {Colors.DEFAULT}{msg}")

def log_sucess(msg):
	print(f"{Colors.GREEN}[SUCESS]: {Colors.DEFAULT}{msg}")

def log_error(msg):
	print(f"{Colors.RED}[ERROR]: {Colors.DEFAULT}{msg}")
	exit(1)

def log_warning(msg):
	print(f"{Colors.YELLOW}[WARNING]: {Colors.DEFAULT}{msg}")
