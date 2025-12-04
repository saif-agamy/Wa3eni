from flask import Flask,render_template,redirect, url_for, request
from forms import login_form, signup_form, post_form, activity_form
from flask_login import LoginManager,login_user, logout_user, login_required, current_user
from models import db, User, Post, Upvote, activity
from os import path
from datetime import datetime

BASE_DIR = path.abspath(path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "174174916476127361976412786491784971364"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR}/instance/site.db"
#-------------------------------------------------------------
app_login_manager = LoginManager()
app_login_manager.init_app(app)
app_login_manager.login_view='login'

@app_login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#-------------------------------------------------------------
db.init_app(app=app)
#-------------------------------------------------------------

@app.route("/")
def home():
    return render_template('Home/home.html', current_user=current_user)

@app.route('/awareness/<type>/')
def awareness(type):
    a_type = ""
    pic_name = ""
    if type=='علمي' :
        pic_name = "Scientific"
        a_type = "Scientific"
    elif type=='بيئي' :
        pic_name = "environmental"
        a_type = "environmental"
    elif type=='رقمي' :
        pic_name = "Digital"
        a_type = "Digital"
    elif type=='اجتماعي' :
        pic_name = "Social"
        a_type = "Social"
    elif type=='ثقافي' :
        pic_name = "Cultural"
        a_type = "Cultural"
    elif type=='رياضي' :
        pic_name = "Sports"
        a_type = "Sports"

    return render_template('Home/awareness.html', type=type, current_user=current_user, pic=pic_name, a_type=a_type)

@app.route('/progress/')
def progress():
    return render_template('Home/progress.html', current_user=current_user)

@app.route('/team/')
def team():
    return render_template('Home/team.html', current_user=current_user)

@app.route('/contact/')
def contact():
    return render_template('Home/contact.html', current_user=current_user)

@app.route('/login/', methods=['GET','POST'])
def login():
    message = None
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user :
            if form.password.data == user.password:
                login_user(user)
                return redirect(url_for('home'))
            else :
                message = 'password is wrong!'
        else :
                message = 'there is no such a user with this username!'

    return render_template('user/login.html', form=form, message=message, current_user=current_user)

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = signup_form()
    if form.validate_on_submit():
        print('valid')
        NewUser = User(
            username=form.username.data,
            email=form.user_email.data,
            age=form.age.data,
            position=form.pos.data,
            phone=form.phone.data,
            password=form.password.data,
            is_active=True)
        db.session.add(NewUser)
        db.session.commit()
        return redirect(url_for('login'))
    else :
        print('form is unvalid')

    return render_template('user/signup.html', form=form, current_user=current_user)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile/<id>/')
@login_required
def profile(id):
    posts = Post.query.filter_by(author_id=id).all()
    return render_template('user/profile.html', current_user=current_user,user=User.query.get(id), posts=posts)

@app.route('/blog/')
@login_required
def blog():
    return render_template('blog/blog.html', current_user=current_user, posts=Post.query.all())

@app.route('/blog/post/share/', methods=['GET','POST'])
@login_required
def share_post():
    form = post_form()
    if form.validate_on_submit():
        post = Post(
            author_id=current_user.id,
            category=form.category.data,
            title=form.title.data,
            content=form.content.data,
            comments=[],
            date=datetime.utcnow(),
            upvotes = 0,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    else :
        print('not valid post', form.errors)

    return render_template('blog/share_post.html', current_user=current_user, form=form)

@app.route('/blog/post/<id>/')
@login_required
def post(id):
    post = Post.query.get(id)
    author = User.query.get(post.author_id)
    upvotes = Upvote.query.filter_by(post_id=id).count()

    return render_template('blog/post.html', current_user=current_user, post=post, author=author, upvotes=upvotes)

@app.route('/blog/post/<id>/delete/')
@login_required
def delete_post(id):
    post = Post.query.get(id)
    user = current_user
    admin = User.query.filter_by(username=admin, password=admin).first()
    if user.id == post.author_id or user.id == admin.id :
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('blog'))

@app.route('/blog/post/<id>/upvote/', methods=['POST'])
@login_required
def upvote(id):
    post = Post.query.get(id)

    already = Upvote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if already:
        db.session.delete(already)
        upvotes_num = Upvote.query.filter_by(post_id=id).count()
        post.upvotes = upvotes_num
        db.session.commit()
        return f"""<span style="color: white;" id="upvotes-btn-{post.id}">{upvotes_num} Upvotes</span>"""

    upvote = Upvote(
        user_id=current_user.id,
        post_id=post.id
    )
    db.session.add(upvote)
    upvotes_num = Upvote.query.filter_by(post_id=id).count()
    post.upvotes = upvotes_num
    db.session.commit()
    return f"""<span style="color: #F2C14E;" id="upvotes-btn-{post.id}">{upvotes_num} Upvotes</span>"""

@app.route('/blog/post/<id>/comment/', methods=['POST'])
@login_required
def comment(id):
    comment = request.form.get('content')

    post = Post.query.get(id)
    comments = post.comments or []
    comments.append({"user": current_user.username, "content": comment})
    post.comments = comments
    
    # Tell SQLAlchemy the attribute changed
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(post, "comments")
    
    db.session.commit()

    return redirect(url_for('post', id=id))

@app.route('/blog/post/<id>/comment/<int:comment_index>/')
@login_required
def comment_delete(id,comment_index):
    from sqlalchemy.orm.attributes import flag_modified
    
    post = Post.query.get(id)
    
    if not post or not post.comments:
        return redirect(url_for('post', id=id))
    
    # Check if the comment exists and belongs to the current user
    if comment_index < len(post.comments):
        comment = post.comments[comment_index]
        
        # Only allow the comment author to delete their own comment
        if comment['user'] == current_user.username:
            post.comments.pop(comment_index)
            flag_modified(post, "comments")
            db.session.commit()
    
    return redirect(url_for('post', id=id))

@app.route('/admin/')
@login_required
def admin():
    admin = User.query.filter_by(username='admin', password='admin').first()
    users = User.query.filter(User.id!=admin.id).all()
    users_num = User.query.filter(User.id!=admin.id).count()

    posts = Post.query.all()
    posts_num = Post.query.count()

    activites = activity.query.all()
    activites_num = activity.query.count()

    return render_template('admin/admin.html', users=users, users_num=users_num, posts=posts, posts_num=posts_num, activites=activites , activites_num=activites_num)

@app.route('/admin/ban/<int:id>')
@login_required
def ban_user(id):
    user = User.query.get(id)
    if user.is_active :
        user.is_active = False
    else :
        user.is_active = True

    db.session.commit()

    return redirect(url_for('admin'))

@app.route('/admin/add_activity', methods=['GET','POST'])
@login_required
def add_activity():
    form = activity_form()
    if form.validate_on_submit():
        act = activity(
            name = form.name.data,
            describtion = form.describtion.data,
            category = form.category.data,
        )

        db.session.add(act)
        db.session.commit()

        return redirect(url_for('admin'))
    
    return render_template('activities/add_activity.html', form=form)

@app.route('/admin/activity/delete/<int:id>/')
@login_required
def finish_activity(id):
    act = activity.query.get(id)
    db.session.delete(act)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/activities/')
@login_required
def activities():
    activities = activity.query.all()
    
    return render_template('activities/activities.html', activities=activities)

@app.route('/activity/subscripe/<int:id>/')
@login_required
def sub_activity(id):
    act = activity.query.get(id)
    user = current_user
    
    if user.id not in act.students :
        students = act.students or []
        students.append(current_user.id)
        act.students = students
        
        # Tell SQLAlchemy the attribute changed
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(act, "students")

        db.session.commit()
    else :
        students = act.students or []
        students.remove(current_user.id)
        act.students = students
        
        # Tell SQLAlchemy the attribute changed
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(act, "students")

        db.session.commit()

    return redirect(url_for('activities', current_user=current_user))

if __name__ == "__main__":
    app.run(debug=True,port=8000)