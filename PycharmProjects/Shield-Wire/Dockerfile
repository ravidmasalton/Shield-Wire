# משתמשים בגרסה רשמית של פייתון
FROM python:3.9-slim

# קובעים את תיקיית העבודה בתוך המכולה (Container)
WORKDIR /app

# מעתיקים את קובץ הדרישות ומתקינים אותן
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# מעתיקים את כל שאר הקוד שלנו מהתיקייה המקומית לתוך המכולה
COPY app/ .

# הפקודה שתריץ את האפליקציה כשהמכולה עולה
CMD ["python", "main.py"]