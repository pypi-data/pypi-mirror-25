from urllib.parse import urlparse, urljoin
from flask import render_template, request, redirect, flash, url_for
from flask_modular_auth import privilege_required, RolePrivilege, current_authenticated_entity
from example.config import app, db
from example.models import create_sample_data_on_first_start, user_loader, BlogPost


def _is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', blogposts=BlogPost.query.order_by(BlogPost.date.desc()))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = user_loader(username=request.form['username'], password=request.form['password'])
        if user:
            app.session_provider.login_entity(user)
            flash('You have been successfully logged in!', 'success')
            if 'next' in request.args and _is_safe_url(request.args['next']):
                return redirect(request.args['next'])
            else:
                return redirect(url_for('index'))
    else:
        next_url = ''
        if 'next' in request.args and _is_safe_url(request.args['next']):
            next_url = request.args['next']
            flash('Please login in order to complete this action!', 'info')
        return render_template('login.html', next_url=next_url)


@app.route('/logout', methods=['GET'])
def logout():
    app.session_provider.logout_entity()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('index'))


@app.route('/write', methods=['GET', 'POST'])
@privilege_required(RolePrivilege('user'))
def write():
    if request.method == 'POST':
        blogpost = BlogPost(user=current_authenticated_entity, title=request.form['title'], text=request.form['text'])
        db.session.add(blogpost)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('write.html')


@app.route('/delete/<post_id>', methods=['GET'])
@privilege_required(RolePrivilege('user'))
def delete(post_id):
    blogpost = BlogPost.query.get(post_id)
    if not blogpost:
        flash('The blog post you want to delete could not be found!', 'warning')
        return redirect(url_for('index'))
    elif not blogpost.can_delete:
        flash('You do not have the rights to delete this blog post!', 'warning')
        return redirect(url_for('index'))
    else:
        db.session.delete(blogpost)
        db.session.commit()
        flash('Blog post deleted!', 'warning')
        return redirect(url_for('index'))


if __name__ == '__main__':

    with app.app_context():
        create_sample_data_on_first_start()
    app.run()
