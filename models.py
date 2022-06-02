from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from database import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_sale = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Item(name={self.name}, price={self.price})"
