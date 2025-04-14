import dash_bootstrap_components as dbc


def render_delete_modal(title: str, button_id: str, modal_id: str) -> dbc.Modal:
    """Функция для отрисовки модального окна для удаления записей

    Args:
        title (str): заголовок модального окна
        button_id (str): идентификатор кнопки
        modal_id (str): идентификатор модального окна

    Returns:
        dbc.Modal: модальное окно
    """
    return dbc.Modal(
        children=[
            dbc.ModalHeader(dbc.ModalTitle(title)),
            dbc.ModalBody(
                children=[
                    dbc.Button(
                        "Удалить",
                        color="danger",
                        id=button_id,
                    )
                ],
            ),
        ],
        id=modal_id,
        is_open=False,
        centered=True,
    )
