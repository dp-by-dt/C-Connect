from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db
from datetime import datetime, timezone


# Creating the db structure
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    username = db.Column(db.String(100), nullable=False)  # Name of the user (later can add this unique if needed)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email of the user
    password = db.Column(db.String(200), nullable=False)  # Passwords not hashed yet (done in setup_db.py)
    created_at = db.Column(db.DateTime, default=db.func.now())  # Timestamp of account creation
    last_login = db.Column(db.DateTime, nullable=True)  # Timestamp of last login

    #hashing passwords for security
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    pass



# PROFILE table
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,unique=True)  # Foreign key to User

    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(225), nullable=True)  # URL to profile
    department = db.Column(db.String(100), nullable=True)
    year=db.Column(db.String(20),nullable=True)
    interests=db.Column(db.JSON,nullable=True,default=list) #or db.String(500), can be comma separated values or db.Text
    location = db.Column(db.String(150), nullable=True)
    visibility = db.Column(db.String(50), default='public')  # public, private, connections-only
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


    #relationship to User table
    user = db.relationship('User', backref=db.backref('profile', uselist=False)) #here changed 'profiles' to 'profile'


# CONNECTIONS
class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who initiated the connection
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who is targetted to connect

    status = db.Column(db.String(20), nullable=False, default='pending')
 #pending, accepted, rejected, blocked
    created_at = db.Column(db.DateTime, default=db.func.now()) #current_timestamp())

    #uniqueness id indexes on (user_id, target_user_id) for avoiding duplicate and
    #Indexing: index target_user_id so fetching incoming requests is fast
    __table_args__ = (
        db.UniqueConstraint('user_id', 'target_user_id', name='_user_target_uc'),
        db.Index('idx_target_user', 'target_user_id'),
    )



    #relationships to User table
    user = db.relationship('User', foreign_keys=[user_id], backref='sent_requests')
    connected_user = db.relationship('User', foreign_keys=[target_user_id], backref='received_requests')


#optional visibility table
''' Later we add option for privacy options like, what option can be viewed by who (like the owner-private, or for all- public)'''




class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    type = db.Column(db.String(30), nullable=False, default='general')
    ref_id = db.Column(db.Integer, nullable=True, index=True)  # ID of post/connection/etc

    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=db.func.now())

    # relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='notifications')
    sender = db.relationship('User', foreign_keys=[sender_id])



class ProfileVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now(), server_default=db.func.now())

    viewer = db.relationship("User", foreign_keys=[viewer_id])
    viewed = db.relationship("User", foreign_keys=[viewed_id])

    __table_args__ = (
        db.Index('idx_viewed_id', 'viewed_id'),
    )




#for posting feeds 
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)

    image_path = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)

    user = db.relationship("User", backref="posts", lazy=True)

    likes = db.relationship(
        "PostLike",
        backref="post",
        cascade="all, delete-orphan",
        lazy="select"
    )



class PostLike(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("post_id", "user_id", name="unique_post_like"),
    )





# For messaging (one to one)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    expires_at = db.Column(db.DateTime, index=True)

    is_saved = db.Column(db.Boolean, default=False)



# ================ college vibe modules ===================
class VibeQuestion(db.Model):
    __tablename__ = "vibe_questions"

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(120), nullable=False)

    # JSON string: ["Easy", "Meh", "Hard"]
    options_json = db.Column(db.Text, nullable=False)

    active_date = db.Column(db.Date, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )



class VibeResponse(db.Model):
    __tablename__ = "vibe_responses"

    id = db.Column(db.Integer, primary_key=True)

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("vibe_questions.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    # Index of the selected option (0-based)
    choice_index = db.Column(db.Integer, nullable=False)

    anonymous_text = db.Column(db.String(80))
    vanish_count = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        db.UniqueConstraint("question_id", "user_id", name="uq_vibe_vote_once"),
        db.Index("ix_vibe_question_created", "question_id", "created_at"),
    )



class VibeReport(db.Model): #for no reports by the same user
    __tablename__ = "vibe_reports"

    id = db.Column(db.Integer, primary_key=True)

    response_id = db.Column(
        db.Integer,
        db.ForeignKey("vibe_responses.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        db.UniqueConstraint("response_id", "user_id", name="uq_vanish_once"),
    )



class VibeDailyState(db.Model): #daily theme color (also for calender view)
    __tablename__ = "vibe_daily_state"

    date = db.Column(db.Date, primary_key=True)

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("vibe_questions.id"),
        nullable=False
    )


    total_responses = db.Column(db.Integer, default=0)
    dominant_choice = db.Column(db.Integer)
    accent_color = db.Column(db.String(7))  # e.g. "#FF4500"

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )





# For campus events board (notice board)
class CampusBoardPost(db.Model):
    __tablename__ = "campus_board_posts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    content = db.Column(db.String(300), nullable=False)

    department = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)

    likes_count = db.Column(db.Integer, default=0)

    user = db.relationship("User", backref="campus_board_posts")

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at



# likes in campus board section
class CampusBoardLike(db.Model):
    __tablename__ = "campus_board_likes"

    id = db.Column(db.Integer, primary_key=True)
    campus_post_id = db.Column(
        db.Integer,
        db.ForeignKey("campus_board_posts.id"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint(
            "campus_post_id",
            "user_id",
            name="unique_campus_board_like"
        ),
    )
