from controller import app, db

def init_db():
    '''
    erstellt Datenbank
    '''
    with app.app_context():
        db.create_all()

def delete_db():
    '''
    löscht Datenbank
    '''
    with app.app_context():
        db.drop_all()
        db.engine.dispose()
