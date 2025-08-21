import re
import string

DEFAULT_SHORT_LENGTH = 6
FORBIDDEN_SHORTS = ('files',)
MAX_GENERATION_ATTEMPTS = 100
MAX_ORIGINAL_LINK_LENGTH = 2048
MAX_SHORT_LENGTH = 16
SHORT_CHARS = string.ascii_letters + string.digits
SHORT_REGEX = re.compile(f'^[{re.escape(SHORT_CHARS)}]+$')
