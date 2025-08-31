#!/bin/bash

# 启动SSH服务
/usr/sbin/sshd -D &

# 启动Jupyter Notebook
jupyter notebook \
  --notebook-dir=${JUPYTER_DIR} \
  --ip=0.0.0.0 \
  --port=${JUPYTER_PORT} \
  --no-browser \
  --allow-root \
  --NotebookApp.token='' \
  --NotebookApp.password=''

# 保持容器运行
wait
