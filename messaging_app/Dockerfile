# 1. Use a base Python image
FROM python:3.10

# 2. Set working directory in the container
WORKDIR /app

# 3. Copy requirements into the container
COPY requirements.txt /app/

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the app code
COPY . /app/

# 6. Expose the Django default port
EXPOSE 8000  
# Run with: docker run -p 8000:8000 messaging_app


# 7. Environment variables 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 8. Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
