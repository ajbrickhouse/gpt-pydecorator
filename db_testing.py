import datetime 
import sqlite3

database = "chatbot.db"  # Replace with your database file or connection details

def get_messages(table: str = "messages", limit: int = 10) -> dict:
    """
    Fetches a limited number of messages from the database and categorizes them into a dictionary.
    @param table: The table to fetch messages from.
    @param limit: The maximum number of messages to fetch.
    """
    print(f"Fetching messages from table {table}")
    # Connect to your database
    conn = sqlite3.connect(database)  # Replace with your database file or connection details
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    result = cursor.fetchone()

    if result is None:
        # Table does not exist, return the available tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        return f"Table '{table}' does not exist. Available tables: {', '.join([t[0] for t in tables])}"

    # Execute a query to fetch a limited number of messages
    # Modify the query as per your database schema and requirements
    query = "SELECT id, content, author, timestamp FROM {} LIMIT ?".format(table)  # Fix the query to include the table name
    cursor.execute(query, (limit,))  # Remove the 'table' parameter from the execute method
    fetched_messages = cursor.fetchall()

    conn.close()

    # Categorize messages
    categorized_messages = {}

    for id, content, author, timestamp in fetched_messages:
        if id not in categorized_messages:
            categorized_messages[id] = []

        categorized_messages[id].append(timestamp)
        categorized_messages[id].append(author)
        categorized_messages[id].append(content)

    if not categorized_messages:
        return "No messages found."
    
    print(categorized_messages)

    return categorized_messages

def add_to_table(content: str, author: str, table: str = "messages") -> str:
    """
    Adds a message to the database
    @param content: The content of the message
    @param author: The author of the message
    @param table: The table to add the message to
    """
    print(f"Adding message to table {table}")
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Check if the table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    result = c.fetchone()

    if result is None:
        # Table does not exist, return the available tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        conn.close()
        return f"Table '{table}' does not exist. Available tables: {', '.join([t[0] for t in tables])}"

    # Insert the message into the database
    c.execute(f"INSERT INTO {table} (content, author, timestamp) VALUES (?, ?, ?)", (content, author, str(datetime.datetime.now())))

    conn.commit()
    conn.close()

    return "Message added to database."

def remove_from_table(ids: list[int], table: str = "messages") -> str:
    """
    Removes messages from the database based on a list of IDs
    @param ids: The list of IDs of the messages to remove
    @param table: The table to remove the messages from
    """
    print(f"Removing messages with IDs {ids} from table {table}")
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Check if the table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    result = c.fetchone()

    if result is None:
        # Table does not exist, return the available tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        conn.close()
        return f"Table '{table}' does not exist. Available tables: {', '.join([t[0] for t in tables])}"

    # Delete the messages from the database
    for id in ids:
        c.execute(f"DELETE FROM {table} WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return "Messages removed from database."

# call the function for testing
# messages = get_messages('notes')



print(add_to_table('level marked', 'testbenchcc', 'notes'))

# print(remove_from_table([1, 2, 3, 4, 5, 6], 'notes'))
