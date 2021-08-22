from flask import render_template, request, flash, url_for, redirect
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(
        is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

def edit_post(method, entry_id = None):
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
def create_entry():
    return edit_post(method = request.method)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return edit_post(entry_id=entry_id,method = request.method)