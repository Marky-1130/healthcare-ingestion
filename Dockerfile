#Base Image
FROM python:3.12-slim

#Working Directory
WORKDIR /app

#Copy Dependecies
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of the application
COPY . /app

#Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]