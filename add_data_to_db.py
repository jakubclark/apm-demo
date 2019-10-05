from apm_demo.app import db, User

if __name__ == '__main__':

    db.create_all()

    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')

    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()

    res = User.query.all()
    print(res)
