paddle ocr 安装还挺烦的,我现在的conda 默认的python是3.11是没法正常安装的,专门要为它建立一个python 3.7的环境

conda create -n paddle37 python=3.7

conda activate paddle37

conda install ipython

pip install paddleocr

