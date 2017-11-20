"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.forms import EditUserForm
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect
from wiki.web.forms import CreateUserForm
from wiki.web.user import UserManager
import config
import pypandoc
import webbrowser
import config
import os

bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)

    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.tags.data = cleanTags(form)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)

@bp.route('/pdf/<path:url>/', methods=['GET'])
@protect
def pdf(url):
    page = current_wiki.get(url)
    path = page.get_path()
    pypandoc.convert_file(path, 'pdf', outputfile="content/pdf/" + url + ".pdf")
    abspath = os.path.abspath("content/pdf/" + url + ".pdf")
    webbrowser.get(config.BROWSER_PATH).open_new_tab(abspath)
    return render_template('page.html', page=page)

def cleanTags(form):
    tags = form.tags.data.encode('utf-8').split(',')
    cleantags = tags
    for item in cleantags:
        if cleantags.count(item) > 1:
            redundantTags = cleantags.count(item) - 1
            while (redundantTags > 0):
                cleantags.remove(item)
                redundantTags -= 1
    cleantags = sorted(cleantags, key=str.upper)
    inputstring = ""
    for item in cleantags:
        inputstring += item + ','
    return inputstring[:-1]

@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']

@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    if current_user.is_active:
        return redirect(request.args.get("next") or url_for('wiki.home'))

    form = LoginForm()
    if form.is_submitted():
        if not form.validate_name(form.name):
            flash("That user does not exist.", 'error')
        else:
            if not form.validate_password(form.password):
                flash("Incorrect password.",'error')
            else:
                user = current_users.get_user(form.name.data)
                login_user(user)
                user.set('authenticated', True)
                user.set('active', True)
                flash('Login successful.', 'success')
                return redirect(request.args.get("next") or url_for('wiki.home'))
    return render_template('login.html', form=form)

@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    current_user.set('active', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.user_login'))

@bp.route('/admin/', methods=['GET', 'POST'])
def admin_page():
    form = EditUserForm()
    if form.validate_on_submit():
        if current_users.get_user(form.user_edit.data):   #todo: !=None maybe
            if current_users.get_user(form.user_edit.data).name == 'name':
                flash('cannot delete the original user', 'error')
            else:
                current_users.delete_user(form.user_edit.data)
        else:
            flash('User not found.', 'error')
    form.user_edit.data = ''
    users = {}
    x = current_users.read()    #returns a dict object with unicode values
    for key, values in x.items():
        name = key.encode('ascii', 'ignore')
        current_data = (values[u'password']).encode('ascii', 'ignore')
        users[name] = current_data


    return render_template('admin_page.html', users=users, form=form)



@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/', methods=['GET', 'POST'])
def user_create():
    form = CreateUserForm()
    if form.is_submitted():
        if form.username.data == '':
            flash('You must enter a username!', 'error')
            return render_template('createuser.html', form=form)
        if form.password.data == '':
            flash('You must enter a password!','error')
            return render_template('createuser.html', form=form)
        um = UserManager(config.USER_DIR)
        um = UserManager(config.USER_DIR)
        user = um.add_user(form.username.data, form.password.data)
        if user == False:
            flash('That username is already in use!')
            return render_template('createuser.html', form=form)
        login_user(user)
        user.set('authenticated', True)
        user.set('active', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.home'))

    return render_template('createuser.html', form=form)


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

