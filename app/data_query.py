from psycopg2 import Error, connect


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = connect("dbname='snapat' user='kiminonaha'"
                       "password='md5745db04ffd8f2d15e2a3682b496f747b'")
        print("Conn : ", conn)
        return conn
    except Error as e:
        print(e)

    return None


def login(umail):
    """ Requête permettant l'identification d'un utilisateur. On vient comparer le PW de la db avec
    celui qu'il a saisi.
    :param user_mail: mail saisi dans le formulaire.
    :return data: mot de passe associé au mail dans la db
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute("SELECT * FROM utilisateur WHERE umail = %s", (umail,))
        except Error as e:
            print("login_query : ", e)
            return None

        data = cur.fetchall()[0]
        user = {'user_id': data[0], 'lastname': data[1], 'firstname': data[2],
                'mail': data[3], 'password': data[4]}

    print(user)
    return user


def get_user_by_id(user_id):
    """ Requête permettant l'identification d'un utilisateur. On vient comparer le PW de la db avec
    celui qu'il a saisi.
    :param user_mail: mail saisi dans le formulaire.
    :return data: mot de passe associé au mail dans la db
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute(
                "SELECT * FROM utilisateur WHERE user_id = %s", (user_id,))
        except Error as e:
            print("login_query : ", e)
            return None

        data = cur.fetchall()[0]
        user = {'user_id': data[0], 'lastname': data[1], 'firstname': data[2],
                'mail': data[3], 'password': data[4]}

    print(user)
    return user


def get_client_by_id(client_id):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute(
                "SELECT * FROM client WHERE client_id = %s", (client_id,))
        except Error as e:
            print("get_user_by_id : ", e)
            return None

        data = cur.fetchall()[0]
        client = {'client_id': data[0], 'name': data[1], 'address': data[2],
                  'cp': data[3], 'city': data[4], 'country': data[5],
                  'phone': data[6], 'mail': data[7], 'id_user': data[8]}

    print(client)
    return client


def get_needs_from_client(client_id):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT need_id FROM need "
                        "JOIN client ON (client.client_id = need.client_id) "
                        "WHERE need.client_id = %s "
                        "AND active = TRUE "
                        "ORDER BY need.status_id ASC, latest_date DESC", (client_id,))
        except Error as e:
            print("get_all_needs_query : ", e)

        data = cur.fetchall()[0]
        need = {'need_id': data[0]}

    print(need)
    return need


def get_needs_from_user(id_user, args=None):
    """ Requête permettant de récupérer tous les besoins d'un utilisateur sans filtre particuliers.
    Ils sont triés par OPEN et date au plus tard
    :return need_list: Liste de tous les needs actifs
    """
    filters = get_filters(args)

    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT c_name, title, latest_date, label_st, need_id, creation_date FROM need "
                        "JOIN status ON (need.status_id = status.status_id) "
                        "JOIN client ON (client.client_id = need.client_id) "
                        "JOIN utilisateur ON (utilisateur.user_id = need.user_id) "
                        "WHERE need.user_id = %s" + filters + " AND active = TRUE "
                        "ORDER BY need.status_id ASC, latest_date DESC", (id_user,))
            datalist = cur.fetchall()
        except Error as e:
            print("get_all_needs_query : ", e)
            return None
        finally:
            cur.close()

        needs = [{
            'client_name': row[0],
            'title': row[1],
            'latest_date': row[2],
            'label_status': row[3],
            'need_id': row[4],
            'creation_date': row[5]} for row in datalist]
    return needs


def get_filters(args):
    filters = ""
    if args is None:
        return filters
    if args['states']:
        filters += " AND need.status_id IN ({})".format(
            ", ".join(args['states']))
    if args.get('create_date'):
        filters += " AND creation_date = '{}'".format(args['create_date'])
    if args.get('latest_date'):
        filters += " AND latest_date = '{}'".format(args['latest_date'])
    if args.get('client_name'):
        filters += " AND c_name ILIKE '%{}%'".format(args['client_name'])
    if args.get('title_need'):
        filters += " AND title ILIKE '%{}%'".format(args['title_need'])
    return filters


def get_need_by_id(need_id):
    """ Select un besoin spécifique pour l'affiche
    :return need: need """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM need WHERE need_id = %s", (need_id,))
        except Error as e:
            print("select_need_query : ", e)

        data = cur.fetchall()[0]
        need = {'need_id': data[0], 'title': data[1], 'description': data[2],
                'creation_date': data[3], 'latest_date': data[4], 'month_duration': data[5],
                'day_duration': data[6], 'price_ht': data[7],
                'consultant_name': data[8], 'client_id': data[9],
                'status_id': data[10], 'active': data[11], 'user_id': data[12], 'key_factors': data[13]}
    print(need)
    return need


def get_clients():
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT client_id, c_name FROM client")
            clients = cur.fetchall()
        except Error as e:
            print("select_clients : ", e)
            return None
        return clients


def insert_need(new_need):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT need_id FROM need ORDER BY need_id DESC LIMIT 1")
            max_id = [int(record[0]) for record in cur.fetchall()][0] + 1
            new_need['need_id'] = max_id
            new_need['active'] = True
            print("MAX : ", max_id)
            inserter = [(str(k), '%s', str(v)) for k, v in new_need.items()]
            fields, place_holders, values = zip(*inserter)
            cur.execute("INSERT INTO need (" +
                        ", ".join(fields) +
                        ") VALUES (" +
                        ", ".join(place_holders) +
                        ")", tuple(values))
        except Error as e:
            print("insert_need_query : ", e)
            return None

    return max_id


def update_need(need_id, title, description, creation_date, latest_date, month_duration,
                day_duration, price_ht, consultant_name, client_id, status_id, user_id, key_factors):
    with create_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute("UPDATE need SET title = %s, "
                        "description = %s ,"
                        "date = %s, "
                        "latest_date = %s,"
                        "month_duration = %s, "
                        "day_duration = %s, "
                        "price_ht = %s, "
                        "consultant_name = %s, "
                        "id_client = %s, "
                        "id_status = %s, "
                        "id_user = %s "
                        "key_factors = %s "
                        "WHERE need_id = %s",
                        (title, description, creation_date, latest_date, month_duration,
                         day_duration, price_ht, consultant_name, client_id, status_id, user_id, key_factors, need_id))
        except Error as e:
            print("update_need : ", e)

    return None


def delete_need(need_id):
    """ Requête permettant de passer un need en inactif (= supprimer).
    :param id_need: id du need à rendre inactif
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE need SET active = FALSE where id_need = %s", (need_id,))
        except Error as e:
            print("delete_need_query : ", e)

    return None


if __name__ == "__main__":
    pass
    login("valentinmele@gfi.com")
    # get_user_by_id(1)
    # get_client_by_id(1)
    # get_needs_from_client(1)
    # get_needs_from_user(1)
    # get_filter_needs()
    # get_need_by_id(2)
    # insert_need("TEST INSERT", "CECI EST UN TEST", "2017-10-21", "2017-11-02",
    # 2, 1, 5157.25, "CONSULTANT NAME TESTI", 1, 1, 1, "JOLIE, BLEU, RAPIDE")
    # update_need()
    # delete_need()
