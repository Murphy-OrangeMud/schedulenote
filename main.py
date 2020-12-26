import backend

if __name__ == "__main__":
    app = backend.create_app()
    with app.app_context():
        app.run(debug=True)