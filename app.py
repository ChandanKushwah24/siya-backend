from api_server import create_app, db
app = create_app()

# main driver function
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)