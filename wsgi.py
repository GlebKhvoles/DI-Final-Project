from app import create_app, db

if __name__ == "__main__":
    app = create_app()
    for rule in app.url_map.iter_rules():
        print(rule)
    
    with app.app_context():
        db.create_all()
        app.run(debug=True)