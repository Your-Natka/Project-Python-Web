# from sqlalchemy import Table, Column, Integer, ForeignKey
# from app.db.base import Base

# photo_tags = Table(
#     "photo_tags",
#     Base.metadata,
#     Column("photo_id", Integer, ForeignKey("photos.id", ondelete="CASCADE")),
#     Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
# )