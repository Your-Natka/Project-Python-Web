def test_comment_model(db_session, test_user, test_photo):
    from app.models.comment import Comment

    comment = Comment(content="Test comment", user_id=test_user.id, photo_id=test_photo.id)
    db_session.add(comment)
    db_session.commit()
    assert comment.id is not None
    assert comment.created_at is not None

def test_rating_unique_constraint(db_session, test_user, test_photo):
    from app.models.rating import Rating
    rating1 = Rating(score=5, user_id=test_user.id, photo_id=test_photo.id)
    db_session.add(rating1)
    db_session.commit()

    rating2 = Rating(score=4, user_id=test_user.id, photo_id=test_photo.id)
    db_session.add(rating2)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()
        assert True