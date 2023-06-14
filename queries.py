import data_manager


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    status = data_manager.execute_select(
        """
        SELECT * FROM statuses s
        WHERE s.id = %(status_id)s
        ;
        """
        , {"status_id": status_id})

    return status


def get_boards():
    """
    Gather all boards
    :return:
    """
    # remove this code once you implement the database
    return [{"title": "board1", "id": 1}, {"title": "board2", "id": 2}]

    return data_manager.execute_select(
        """
        SELECT * FROM boards
        ;
        """
    )


def get_cards_for_board(board_id):
    # remove this code once you implement the database
    return [{"title": "title1", "id": 1}, {"title": "board2", "id": 2}]

    matching_cards = data_manager.execute_select(
        """
        SELECT * FROM cards
        WHERE cards.board_id = %(board_id)s
        ;
        """
        , {"board_id": board_id})

    return matching_cards

def create_board(title):
    """
    Creat a new board
    :param title: title of the new board
    :return: dict of the new board
    """
    new_board_id = data_manager.execute_select_statement(
        """
        INSERT INTO boards (title) VALUES (%(title)s)
        RETURNING id
        ;
        """,
        {"title": title}
    )
    
    return {"id": new_board_id, "title": title}

def rename_board(board_id, new_title):
    """
    Rename an existing board
    :param board_id: id of the board to rename
    :param new_title: new title for the board
    :return: dict of the updated board
    """
    data_manager.execute_dml_statement(
        """
        UPDATE boards
        SET title = %(new_title)s
        WHERE id = %(board_id)s
        ;
        """,
        {"board_id": board_id, "new_title": new_title}
    )
    
    return {"id": board_id, "title": new_title}