import md
import os.path
import sys

print('before')
md.run_md()

print('after rn')
if os.path.isfile('argon.traj'):
    print('FIle exists')
    sys.exit(0)
else:
    sys.exit(1)
