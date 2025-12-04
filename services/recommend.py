from models import User, Profile, Connection
from app import db
from sqlalchemy import func

def compute_score(target_user, candidate):
    """Return a numeric score for sorting discover suggestions."""
    score = 0.0
    # weight settings (tweakable)
    w_interest = 3.0
    w_dept = 2.0
    w_mutuals = 2.5
    w_recent = 1.0
    w_activity = 1.2

    # shared interests (assuming Profile.interests is comma-separated)
    t_interests = set((target_user.profile.interests or "").lower().split(','))
    c_interests = set((candidate.profile.interests or "").lower().split(','))
    shared = len([i for i in t_interests if i.strip() and i in c_interests])
    score += w_interest * shared

    # same department
    if (target_user.profile.department and candidate.profile.department and
        target_user.profile.department == candidate.profile.department):
        score += w_dept

    # mutual connections: quick DB lookup
    # assume Connection has user_id, connected_user_id with status 'accepted'
    mutuals = db.session.query(func.count()).select_from(Connection).filter(
        Connection.user_id.in_([target_user.id, candidate.id]),
        Connection.connected_user_id.in_([target_user.id, candidate.id]),
        Connection.status == 'accepted'
    ).scalar() or 0
    score += w_mutuals * mutuals

    # recency: candidate recent login
    if candidate.last_login:
        age_hours = (func.now() - candidate.last_login).total_seconds() / 3600 if hasattr(candidate.last_login, 'timetuple') else 0
        # more recent -> higher score
        score += w_recent * max(0, 1/(1+age_hours/24))

    # profile completeness/activity
    completeness = 0
    if candidate.profile.bio: completeness += 0.5
    if candidate.profile.profile_picture: completeness += 0.5
    score += w_activity * completeness

    return score

def suggest_for(user, limit=20):
    # fetch candidates excluding current connections and self
    excluded = [user.id] + [c.connected_user_id for c in user.connections if c.status == 'accepted']
    candidates = User.query.filter(~User.id.in_(excluded)).limit(200).all()
    scored = []
    for c in candidates:
        s = compute_score(user, c)
        scored.append((s, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:limit]]
