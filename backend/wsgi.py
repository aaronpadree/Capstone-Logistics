from app import app, db
from dotenv import load_dotenv


if __name__ == "__main__":
    app.run()

load_dotenv()  # Ensures .env variables are loaded

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')



