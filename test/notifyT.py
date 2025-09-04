import sys, os
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from notify.wechat_bot import  wechat_push
wechat_push('wechat_push 已接入')