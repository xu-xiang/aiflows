# 使用官方 Python 运行时作为父镜像
FROM python:3.11-slim

# 设置工作目录为 /app
WORKDIR /app

# 首先复制 requirements.txt 并安装依赖项
COPY ./github_api/requirements.txt /app/github_api/requirements.txt
RUN pip install --no-build-isolation --upgrade pip
RUN pip install --no-build-isolation --no-cache-dir -r /app/github_api/requirements.txt

# 然后复制剩余的项目文件
COPY . /app

# 使端口 9000 可供此容器外的环境使用
EXPOSE 9000

# 运行 app/main.py 时启动 Python 应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
