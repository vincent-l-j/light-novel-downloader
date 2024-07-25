import sys
from . import main

exit_status = 1
try:
    main()
    exit_status = 0
except Exception as e:
    print("Error:", e, file=sys.stderr)
sys.exit(exit_status)
