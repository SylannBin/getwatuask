from psycopg2 import Error, connect


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        with open('connection_string', 'rt') as f:
            connection_string = f.read()
        conn = connect(connection_string)
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


def get_id_client_by_client_name(client_name):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute(
                "SELECT client_id FROM client WHERE c_name = %s", (client_name,))
        except Error as e:
            print("get_user_by_id : ", e)
            return None

        client_id = cur.fetchall()[0]

    print(client_id[0])
    return client_id[0]


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
            'label_st': row[3],
            'need_id': row[4],
            'creation_date': row[5]} for row in datalist]
    return needs


def get_filters(args):
    filters = ""
    if args is None:
        return filters
    if args['states']:
        states = [arg for arg in args['states'] if arg is not None]
        if len(states) != 0:
            filters += " AND need.status_id IN ({})".format(", ".join(states))
    if args.get('min_date'):
        filters += " AND creation_date >= '{}'".format(args['min_date'])
    if args.get('max_date'):
        filters += " AND latest_date <= '{}'".format(args['max_date'])
    if args.get('client_name'):
        filters += " AND c_name = '{}'".format(args['client_name'])
    if args.get('title'):
        filters += " AND title ILIKE '%{}%'".format(args['title'])
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
            return []
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


def update_need(need_id, description, latest_date, month_duration,
                day_duration, price_ht, consultant_name, status_id, key_factors):
    with create_connection() as conn:
        cur = conn.cursor()
        print("PASSE PAR LE UPDATE")
        try:
            cur.execute("UPDATE need SET "
                        "description = %s ,"
                        "latest_date = %s,"
                        "month_duration = %s, "
                        "day_duration = %s, "
                        "price_ht = %s, "
                        "consultant_name = %s, "
                        "status_id = %s, "
                        "key_factors = %s "
                        "WHERE need_id = %s",
                        (description, latest_date, month_duration,
                         day_duration, price_ht, consultant_name, status_id, key_factors, need_id))
        except Error as e:
            print("update_need : ", e)

    return None


def delete_need(need_id):
    """ Requête permettant de passer un need en inactif (= supprimer).
    :param id_need: id du need à rendre inactif
    """
    print("PASSE PAR DELETE NEED")
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE need SET active = FALSE where need_id = %s", (need_id,))
        except Error as e:
            print("delete_need_query : ", e)

    return None


if __name__ == "__main__":
    pass
