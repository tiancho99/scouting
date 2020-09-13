from flask import redirect, url_for
import unittest

from app import create_app

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/static/uploads')
def upload():
    return app.config[UPLOAD_FOLDER]

def main():
    app.config['DEBUG'] = 1
    app.config['ENV'] = 'development'
    app.run()

if __name__ == "__main__":

    import cProfile
    cProfile.run("main()", "output.dat")

    import pstats
    from pstats import SortKey

    with open("output_time.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("output_calls.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats()
