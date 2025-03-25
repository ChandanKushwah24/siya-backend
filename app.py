from api_server import create_app, db
app = create_app()

# main driver function
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(host='localhost', port=5001, debug=True)