# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# COPY requirements.txt /tmp/
# COPY ./Cloud-Computations /app
# RUN pip install -r /tmp/requirements.txt
#
#
# EXPOSE 80
# WORKDIR "/app/src/models"
# #RUN cd /app/src/models
# #CMD ["python", "train_model.py", "Montreal.csv", "Montreal"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#
# FROM python:3.7
# COPY requirements.txt /tmp/
# COPY ./Cloud-Computations /app
# RUN pip install -r /tmp/requirements.txt
# RUN pip install fastapi uvicorn
# WORKDIR "/app/src/models"
# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]

FROM python:3.7
RUN apt-get update
RUN apt-get install -y git
# Create a directory and clone git code
RUN git clone -b Docker https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations.git

COPY requirements.txt /tmp/
COPY ./Cloud-Computations /app
RUN pip install -r /tmp/requirements.txt
RUN pip install fastapi uvicorn
WORKDIR "/app/src/models"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]

#
# FROM ubuntu:latest AS ml_code
# # Install git
# RUN apt-get update
# RUN apt-get install -y git
# # Create a directory and clone git code
# RUN mkdir /app
# RUN cd /app
# COPY ./ .
# #RUN git clone -b Docker https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations.git
#
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as base_image
# FROM base_image AS train
# COPY --from=ml_code ./app/Cloud-Computations/requirements.txt .
#

#RUN pip install -r ./app/Cloud-Computations/requirements.txt
#CMD ["python", "/app/Cloud-Computations/Cloud-Computations/src/models/train_model.py","Montreal.csv","Montreal"]

#RUN pip install -r requirements.txt
#COPY --from=ml_code ./app/Cloud-Computations/Makefile .
# COPY --from=ml_code /app/Cloud-Computations/Cloud-Computations/src/models/Montreal.pkl .
# COPY --from=ml_code /app/Cloud-Computations/Cloud-Computations/src/models/Montrealtransformer.pkl .
# COPY --from=ml_code /app/Cloud-Computations/Cloud-Computations/src/models/main.py .
#

#
#
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as base_image
# FROM base_image AS train
# RUN pip install -r requirements.txt
# #RUN python /app/src/train_model.py "Montreal.csv" "Montreal"
# #CMD ["python", "/app/Cloud-Computations/src/train_model.py","Montreal.csv","Montreal"]
# COPY --from=ml_code /app/Cloud-Computations/models/predict_model.py .
# COPY --from=ml_code /app/Cloud-Computations/models/Montreal.pkl .
# COPY --from=ml_code /app/Cloud-Computations/models/Montrealtransformer.pkl .
# COPY --from=ml_code /app/Cloud-Computations/models/main.py .

# COPY --from=models predictions.pkl .




