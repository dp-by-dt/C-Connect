from . import posts_bp
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Post, PostLike
from models import Notification

import os
from datetime import datetime, timezone
from PIL import Image
from werkzeug.utils import secure_filename

from PIL import Image, ImageOps
from blueprints.notifications.service import create_notification

from services.file_service import FileService



#============== Helper functions ============

#---------- post image upload crop helper ----------
def save_post_image(file, user_id):
    # Open image
    img = Image.open(file)
    #Apply EXIF orientation FIRST
    img = ImageOps.exif_transpose(img)
    width, height = img.size

    # Center crop to square
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim

    img = img.crop((left, top, right, bottom))
    img = img.resize((600, 600))

    # Build readable filename
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    filename = f"post_img{user_id}_{timestamp}.jpg"

    # Upload directory: static/uploads/posts
    upload_root = current_app.config["UPLOAD_FOLDER"]
    upload_dir = os.path.join(upload_root, "posts")
    os.makedirs(upload_dir, exist_ok=True)

    # Save file
    filepath = os.path.join(upload_dir, filename)
    img.save(filepath, format="JPEG", quality=85)

    # Return path relative to /static
    return f"uploads/posts/{filename}"




# =========== routes ==================
@posts_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    content = request.form.get("content", "").strip()
    image = request.files.get("image")

    if not content and not image:
        flash("Post cannot be empty", "error")
        return redirect(request.referrer or url_for("posts.feed"))

    image_path = None
    if image and image.filename:
        try:
            image_path = save_post_image(image, current_user.id)
        except Exception:
            flash("Invalid image file", "error")
            return redirect(request.referrer or url_for("posts.feed"))

    post = Post(
        user_id=current_user.id,
        content=content,
        image_path=image_path
    )

    db.session.add(post)
    db.session.commit()

    return redirect(url_for("posts.feed"))




@posts_bp.route("/posts/feed")
@login_required
def feed():
    page = request.args.get("page", 1, type=int)

    pagination = (
        Post.query
        .order_by(Post.created_at.desc())
        .paginate(page=page, per_page=10, error_out=False)
    )

    # Clamp to last page if invalid page number 
    if not pagination.items and page > 1:
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(
            page=pagination.pages or 1, per_page=10, error_out=False
        )

    posts = pagination.items

    #passing profile picture of the user who's the post is
    # since the profile picture is stored in Profiel model (not in User), we can access it via user relationship
    #that is take the user_id of the owner of the post, 
    user_ids = [post.user_id for post in posts]
    profile_picture_cache = {}

    # lookup in the profile table for the "profile_picture" for that user_id
    from models import Profile
    profiles = Profile.query.filter(Profile.user_id.in_(user_ids)).all()
    for profile in profiles:
        profile_picture_cache[profile.user_id] = profile.profile_picture


    # adding current user profile picture to profile_pic_cache
    if current_user.id not in profile_picture_cache:
        profile_picture_cache[current_user.id] = current_user.profile.profile_picture
    #profile_picture = profile.query.filter_by(user_id=user.id).first().profile_picture
    
    
    # Get liked post IDs for current user
    liked_post_ids = {
        like.post_id
        for like in PostLike.query.filter_by(user_id=current_user.id).all()
    }

    return render_template(
        "posts/feed.html",
        posts=posts,
        profile_picture_cache=profile_picture_cache,
        pagination=pagination,
        liked_post_ids=liked_post_ids
    )



@posts_bp.route("/<int:post_id>/like", methods=["POST"])
@login_required
def toggle_like(post_id):
    post = Post.query.get_or_404(post_id)

    like = PostLike.query.filter_by(
        post_id=post_id,
        user_id=current_user.id
    ).first()

    if like:
        db.session.delete(like)

        #remove existing like notification (if any)
        Notification.query.filter_by(
            user_id=post.user_id,
            sender_id=current_user.id,
            type="post_like",   
            ref_id=post.id
        ).delete()

    else:
        db.session.add(PostLike(post_id=post_id, user_id=current_user.id))

        # create notification for like
        create_notification(
            user_id=post.user_id,
            sender_id=current_user.id,
            message=f"{current_user.username} liked your post",
            type='post_like',
            ref_id=post.id,           # Prevents duplicate likes on same post
            rate_limit=True           # Default - applies limits
        )

    db.session.commit()

    # Add #post-{post_id} to referrer
    referrer = request.referrer #scrolls to the position
    return redirect(f"{referrer}#post-{post_id}" if referrer else url_for("posts.feed"))



#for deleting the own posts
@posts_bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        flash("Unauthorized action", "error")
        return redirect(url_for("posts.feed"))
    
    #for deleting the posts images from db
    file_service = FileService()
    if post.image_path:
        print(f"image_path = {post.image_path}")
        current_app.logger.warning(f"IMAGE_PATH (DB): {post.image_path}")
        current_app.logger.warning(f"UPLOAD_FOLDER: {current_app.config['UPLOAD_FOLDER']}")

        success = file_service.delete_post_image(post.image_path)
        print("success deletion")
        if not success:
            print("failed deletion")
            current_app.logger.warning(f"Failed to delete image: {post.image_path}")

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted", "success")

    # Smart redirect to nearby post
    referrer_or_url = request.referrer or url_for("posts.feed") #scrolls to the position

    # Try scroll to PREVIOUS post
    prev_id = post_id - 1
    if Post.query.get(prev_id):
        return redirect(f"{referrer_or_url}#post-{prev_id}")
    
    # Try scroll to NEXT post  
    next_id = post_id + 1
    if Post.query.get(next_id):
        return redirect(f"{referrer_or_url}#post-{next_id}")
    
    # Fallback: Original position or feed
    return redirect(referrer_or_url)

    #return redirect(f"{referrer}#post-{post_id-1}" if referrer else url_for("posts.feed"))



