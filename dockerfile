# 1. Use an official lightweight Python image
# 1. Use full Python image (needed for some AI compile tools)
FROM python:3.9

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependencies first (caching mechanism)
# Docker checks if this file changed. If not, it skips the install step!
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]