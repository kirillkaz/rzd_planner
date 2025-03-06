from rzd_planner.app import app
from rzd_planner.layouts.main_layout import render_main_layout

app.layout = render_main_layout()
srv = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
