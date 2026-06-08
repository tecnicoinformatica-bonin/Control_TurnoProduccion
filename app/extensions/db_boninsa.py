from flask import current_app


def get_boninsa_connection():
    import pyodbc
    return pyodbc.connect(
        (
            "DRIVER={SQL Server Native Client 11.0};"
            f"SERVER={current_app.config['BONINSA_HOST']};"
            f"DATABASE={current_app.config['BONINSA_DB']};"
            f"UID={current_app.config['BONINSA_USER']};"
            f"PWD={current_app.config['BONINSA_PASSWORD']};"
            "TrustServerCertificate=yes;"
        )
    )