import os
from ai import get_mathpix_response, get_ai_explain, get_ai_title
import pickle
import notion
import logging
from app import postToNotion, sideTask
import time
import concurrent.futures

image_url = "http://mmbiz.qpic.cn/mmbiz_jpg/QUTmRqDPFQRSNLDOQlgVnSichbEl9To7fs2icEn8depw6dGhE5KwsriaRp5hibIVAZcGicWSCKzkdbXrbjIoCJleazw/0"

explain = r"""
 这个公式表示在给定条件 $Y=c_k$ 下，随机变量 $X$ 取值为 $x$ 的概率可以被分解为每个维度 
 $X^{(j)}$ 取值为 $x^{(j)}$ 的概率的乘积。其中，$X^{(j)}$
 表示 $X$ 在第 $j$ 个维度上的取值，$x^{(j)}$ 表示 $X^{(j)}$ 取值为 $x^{(j)}$ 的情况，
 $P(X=x \mid Y=c_k)$ 表示在给定条件 $Y=c_k$ 下，$X$ 取值为 $x$ 的概率，$P(X^{(j)}=x^{(j)} \mid Y=c_k)$ 
 表示在给定条件 $Y=c_k$ 下，$X^{(j)}$ 取值为 $x^{(j)}$ 的概率。
"""

# formula = r"\begin{aligned}P\left(X=x \mid Y=c_{k}\right) & =P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} \mid Y=c_{k}\right) \\& =\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} \mid Y=c_{k}\right)\end{aligned}"

formula = r"""
\begin{aligned}
P\left(X=x \mid Y=c_{k}\right) & =P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} \mid Y=c_{k}\right) \\
& =\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} \mid Y=c_{k}\right)
\end{aligned}
""".replace("\\", "\\\\").strip('\"\"\"')

formula2 = "\begin{aligned}P\left(X=x \mid Y=c_{k}\right) & =P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} \mid Y=c_{k}\right) \\& =\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} \mid Y=c_{k}\right)\end{aligned}"

# notion.createPage(image_url, "朴素贝叶斯公式", formula, explain)

# postToNotion(image_url, formula)

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# logging.info('This is an info log.')
# logging.warning('This is a warning log.')

# Query result
# success: {"object":"list","results":[{"object":"page","id":"7365a5fe-a8b8-44f3-ada7-973639ae1f2a","created_time":"2023-05-29T15:43:00.000Z","last_edited_time":"2023-05-30T07:34:00.000Z","created_by":{"object":"user","id":"778b85ee-1f43-48bc-b545-43c8b7582afa"},"last_edited_by":{"object":"user","id":"7f78ec91-6bbf-4aa0-ae82-f25121828ed4"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"72c8dc93-6632-419d-ac50-2e5625d45805"},"archived":false,"properties":{"Pic":{"id":"Bd%5Ed","type":"url","url":null},"Latex":{"id":"I%3FMN","type":"rich_text","rich_text":[{"type":"text","text":{"content":"\\begin{aligned}P\\left(X=x \\mid Y=c_{k}\\right) & =P\\left(X^{(1)}=x^{(1)}, \\cdots, X^{(n)}=x^{(n)} \\mid Y=c_{k}\\right) \\\\& =\\prod_{j=1}^{n} P\\left(X^{(j)}=x^{(j)} \\mid Y=c_{k}\\right)\\end{aligned}","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"\\begin{aligned}P\\left(X=x \\mid Y=c_{k}\\right) & =P\\left(X^{(1)}=x^{(1)}, \\cdots, X^{(n)}=x^{(n)} \\mid Y=c_{k}\\right) \\\\& =\\prod_{j=1}^{n} P\\left(X^{(j)}=x^{(j)} \\mid Y=c_{k}\\right)\\end{aligned}","href":null}]},"Explain":{"id":"gd%3C%5C","type":"rich_text","rich_text":[{"type":"text","text":{"content":"这个LaTeX公式是条件概率的定义，其中$P(X=x|Y=c_k)$表示当$Y=c_k$时$X=x$的概率，$X$和$Y$是两个随机变量，$x$是$X$的取值，$c_k$是$Y$的取值。公式中的$n$表示$X$有$n$个分量，$x^{(j)}$表示$X$的第$j$个分量的取值，$P(X^{(j)}=x^{(j)}|Y=c_k)$表示当$Y=c_k$时$X^{(j)}=x^{(j)}$的概率，这个概率是条件概率$P(X=x|Y=c_k)$的一部分。整个公式的含义是，当给定$Y=c_k$时，$X$的各个分量的取值$x^{(j)}$独立同分布，且每个分量取值的概率是$P(X^{(j)}=x^{(j)}|Y=c_k)$，因此$X$的取值$x$的概率就是各个分量取值概率的乘积。","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"这个LaTeX公式是条件概率的定义，其中$P(X=x|Y=c_k)$表示当$Y=c_k$时$X=x$的概率，$X$和$Y$是两个随机变量，$x$是$X$的取值，$c_k$是$Y$的取值。公式中的$n$表示$X$有$n$个分量，$x^{(j)}$表示$X$的第$j$个分量的取值，$P(X^{(j)}=x^{(j)}|Y=c_k)$表示当$Y=c_k$时$X^{(j)}=x^{(j)}$的概率，这个概率是条件概率$P(X=x|Y=c_k)$的一部分。整个公式的含义是，当给定$Y=c_k$时，$X$的各个分量的取值$x^{(j)}$独立同分布，且每个分量取值的概率是$P(X^{(j)}=x^{(j)}|Y=c_k)$，因此$X$的取值$x$的概率就是各个分量取值概率的乘积。","href":null}]},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"条件概率","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"条件概率","href":null}]}},"url":"https://www.notion.so/7365a5fea8b844f3ada7973639ae1f2a"}],"next_cursor":null,"has_more":false,"type":"page_or_database","page_or_database":{}}   
# fail: {"object":"list","results":[],"next_cursor":null,"has_more":false,"type":"page_or_database","page_or_database":{}}

# postToNotion("img url","\begin{aligned}P\left(X=x \mid Y=c_{k}\right) & =P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} \mid Y=c_{k}\right) \\& =\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} \mid Y=c_{k}\right)\end{aligned}")

# fromUser = "oJEm4weaNqNQXNClh05lzMJ4K0S4"

#获取图片解析数据
# code, result = get_mathpix_response("http://mmbiz.qpic.cn/mmbiz_jpg/QUTmRqDPFQRSNLDOQlgVnSichbEl9To7fs2icEn8depw6dGhE5KwsriaRp5hibIVAZcGicWSCKzkdbXrbjIoCJleazw/0")
# if(code == 200):
#     print(result)
# else:
#     print(f"~err~ ${result}")

#获取公式标题
get_ai_title(formula)
# get_ai_title("\begin{aligned}P\left(X=x \mid Y=c_{k}\right) & =P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} \mid Y=c_{k}\right) \\& =\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} \mid Y=c_{k}\right)\end{aligned}")
# get_ai_title(formula)
# print(formula)
