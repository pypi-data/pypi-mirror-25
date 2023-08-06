expressions = [
    """
    CREATE TABLE _user (
        id bigserial primary key,
        username varchar(20) UNIQUE NOT NULL,
        password varchar NOT NULL,
        salt varchar NOT NULL,
        last_login timestamptz,
        email varchar(50) UNIQUE,
        phone varchar(20),
        is_active boolean DEFAULT true,
        first_name varchar(30),
        last_name varchar(30),
        date_joined timestamptz DEFAULT now(),
        is_superuser boolean DEFAULT false
    );
    """,
    """
    CREATE EXTENSION cube;
    """,
    """
    CREATE EXTENSION earthdistance;
    """,
    """
    CREATE EXTENSION hstore;
    """
]
