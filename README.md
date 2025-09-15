find . -type d -name "__pycache__" -exec rm -rf {} +


docker build -t codefuseapp -f docker/Dockerfile .


docker run -d -p 8080:8080 codefuseapp:latest