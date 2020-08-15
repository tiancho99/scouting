
from . import crud

@crud.route('/view')
def view(foo):
    return render_template('expression')