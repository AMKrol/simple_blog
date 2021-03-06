from blog.forms import LoginForm
from flask import render_template, request, flash, url_for, redirect, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
import functools
import babel

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions

@app.template_filter()
def format_datetime(value):
    format="dd.MM.y"
    return babel.dates.format_datetime(value, format)

@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(
        is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


def edit_post(method, entry_id=None):
    entry = []
    form = []
    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    else:
        form = EntryForm()
    errors = None
    if method == 'POST':
        if form.validate_on_submit():
            if entry_id:
                form.populate_obj(entry)
                flash('Pomyślnie edytowano post')
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
                flash('Pomyślnie dodano post')

            db.session.commit()

            return redirect(url_for('homepage'))
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return edit_post(method=request.method)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return edit_post(entry_id=entry_id, method=request.method)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('homepage'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage'))

@app.route("/drafts", methods=["GET"])
@login_required
def drafts():
    drafts = Entry.query.filter_by(
        is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)

@app.route("/delete", methods=["POST"])
@login_required
def delete_entry():
    entry_id = request.form['post_id']
    print(entry_id)
    action_type = request.form.get("action")
    if Entry.query.get(entry_id):
        if action_type == "delete":
            Entry.query.filter_by(id=entry_id).delete()
            db.session.commit()
        elif action_type == "edit":
            return redirect(url_for('edit_entry', entry_id=entry_id))
    return redirect(url_for("homepage"))