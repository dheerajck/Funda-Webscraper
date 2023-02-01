import sqlite3


def create_new_table():
    connection = sqlite3.connect('fundanew.db')

    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        status text,
        link text,
        thumbnail_link text,
        name text,
        address text,
        price int,
        living_space int,
        plot_area int,
        rooms int,
        broker_name text,
        broker_link text,
        is_processed boolean DEFAULT FALSE,
        added_on timestamp,
        type text,
        latitude text,
        longitude text,
        error_link text,
        UNIQUE(link)

        )"""
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        ad_id INTEGER NOT NULL,

        image_link text,
        type_of_image text,

        is_processed boolean DEFAULT FALSE,
        added_on timestamp DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (ad_id) REFERENCES ads(id),

        UNIQUE (ad_id, image_link)
        )"""
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ad_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        ad_id INTEGER NOT NULL,

        ad_body text,

        is_processed boolean DEFAULT FALSE,
        added_on timestamp DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (ad_id) REFERENCES ads(id),

        UNIQUE (ad_id)
        )"""
    )

    connection.close()


# PRAGMA foreign_keys;
# Code language: SQL (Structured Query Language) (sql)
# The command returns an integer value: 1: enable, 0: disabled. If the command returns nothing, it means that your SQLite version doesn’t support foreign key constraints.

# If the SQLite library is compiled with foreign key constraint support, the application can use the PRAGMA foreign_keys command to enable or disable foreign key constraints at runtime.

# To disable foreign key constraint:

# PRAGMA foreign_keys = OFF;
# Code language: SQL (Structured Query Language) (sql)
# To enable foreign key constraint:

# PRAGMA foreign_keys = ON;

if __name__ == "__main__":
    create_new_table()
