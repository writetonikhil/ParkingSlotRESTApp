# Spcify a base image
FROM python:3

# Copy build files
COPY ./ /usr/parking

# Sepcify working directory of the app
WORKDIR /usr/parking

# Install dependencies
RUN pip install -r requirements.txt
#RUN pip install flask
#RUN pip install flask_jwt_extended
#RUN pip install flask_restful
#RUN pip install flask_pymongo
#RUN pip install pymongo
#RUN pip install pytest
#RUN pip install requests

# Default command
CMD ["python", "main.py"]