
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Pitch,Comment
from .. import db,photos
from .forms import UpdateProfile,PitchForm,CommentForm
from flask_login import login_required,current_user
import datetime


@main.route('/')
def index():
    pickup = Pitch.get_pitches('pickup')
    interview = Pitch.get_pitches('interview')
    product = Pitch.get_pitches('product')
    promotion = Pitch.get_pitches('promotion')

    return render_template('index.html', title = 'Pitch App - Home', pickup = pickup, interview = interview, promotion = promotion, product = product)

@main.route('/pitches/pickup')
def pickup():
    pitches = Pitch.get_pitches('pickup lines')

    return render_template('pickup.html',pitches = pitches)


@main.route('/pitches/interview')
def interview():
    pitches = Pitch.get_pitches('interview')

    return render_template('interview.html',pitches = pitches)


@main.route('/pitches/product')
def product():
    pitches = Pitch.get_pitches('product')

    return render_template('product.html',pitches = pitches)


@main.route('/pitches/promotion')
def promotion():
    pitches = Pitch.get_pitches('promotion')

    return render_template('promotion.html',pitches = pitches)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitch_count = Pitch.count_pitches(uname)

    if user is None:
        abort(404)

    return render_template('profile/profile.html',user = user, pitches = pitch_count)


@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html', form = form)


@main.route('/user/<uname>/update/pic', methods = ['POST'])
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile', uname = uname))


@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.text.data
        category = form.category.data

        new_pitch = Pitch(pitch_title = title,pitch_content = pitch, category = category,user = current_user)
        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    title = 'New Pitch'
    return render_template('new_pitch.html', title = title, pitch_form = form)

@main.route('/pitch/<int:id>', methods = ["GET","POST"])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')
    if request.args.get('like'):
        pitch.likes += 1

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('.pitch', id = pitch.id))

    elif request.args.get('dislike'):
        pitch.dislikes += 1

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('.pitch', id = pitch.id))

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.text.data

        new_comment = Comment(comment = comment, user = current_user, pitch_id = pitch)

        new_comment.save_comment()

    comments = Comment.get_comments(pitch)

    return render_template('pitch.html', pitch = pitch, comment_form = form,comments = comments, date = posted_date)

@main.route('/user/<uname>/pitches', methods = ['GET','POST'])
def user_pitches(uname):
    user = User.query.filter_by(username = uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitch_count = Pitch.count_pitches(uname)

    return render_template('profile/pitches.html', user = user, pitches = pitches, pitches_count = pitch_count)