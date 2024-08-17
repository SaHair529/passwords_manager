from db_manager import DBManager


def main():
    db = DBManager()

    db.add_password('example.com', 'username', 'password')

    results = db.search_password('example')
    for site, user, passw in results:
        print(f"Website: {site}, Username: {user}, Password: {passw}")

    db.close()


if __name__ == '__main__':
    main()
