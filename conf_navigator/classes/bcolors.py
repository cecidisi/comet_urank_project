class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def print_blue(text):
	print bcolors.OKBLUE + text + bcolors.ENDC


def print_red(text):
	print bcolors.FAIL + text + bcolors.ENDC
