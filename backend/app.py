from app import create_app

app = create_app()

app.config['JWT_SECRET_KEY'] = 'your_secret_key' 

if __name__ == '__main__':
    app.run(debug=True)
