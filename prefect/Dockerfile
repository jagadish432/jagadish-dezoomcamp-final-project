FROM prefecthq/prefect:2.7.7-python3.9

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows/ /opt/prefect/flows/

ENV project_name=${project_name}

RUN echo $project_name
# ENV PREFECT_API_URL=http://0.0.0.0:4200/api

# RUN prefect config set PREFECT_API_URL="${PREFECT_API_URL}"