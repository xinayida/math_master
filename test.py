import os
from ai import get_mathpix_response, get_ai_response

# fromUser = "oJEm4weaNqNQXNClh05lzMJ4K0S4"

#获取图片解析数据
# code, result = get_mathpix_response("http://mmbiz.qpic.cn/mmbiz_jpg/QUTmRqDPFQRSNLDOQlgVnSichbEl9To7fs2icEn8depw6dGhE5KwsriaRp5hibIVAZcGicWSCKzkdbXrbjIoCJleazw/0")
# if(code == 200):
#     print(result)
# else:
#     print(f"~err~ ${result}")

#获取AI回答
get_ai_response("\begin{aligned}P\left(X=x \mid Y=c_{k}\right) & =P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} \mid Y=c_{k}\right) \\& =\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} \mid Y=c_{k}\right)\end{aligned}")

