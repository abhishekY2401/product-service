FROM python:3.8-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Copy the run.sh script into the container
COPY run.sh .

# Set the command to run the script
CMD ["sh", "run.sh"]