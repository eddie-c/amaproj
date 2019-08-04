from sqlalchemy import Column,String,Integer,DateTime,create_engine,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Product(base):
    __tablename__="product"
    id = Column(String(10),primary_key=True)
    asin = Column(String(20))
    site = Column(String(2))
    url = Column(String(1000))
    shop_id = Column(String(20),ForeignKey('shop.id'))
    shop_name = Column(String(50))
    brand = Column(String(50))
    shop_url = Column(String(1000))
    first_available = Column(String(50))
    first_level_cate = Column(String(255))
    second_level_cate = Column(String(255))
    product_history_data  = relationship('ProductHistory')

class Shop(base):
    __tablename__="shop"
    id = Column(String(10),primary_key=True)
    shop_amazon_id = Column(String(20))
    shop_name = Column(String(50))
    shop_url = Column(String(1000))
    product_count = Column(Integer)
    products = relationship('Product')

class Site(base):
    __tablename__ = "site"
    site_name = Column(String(50))
    site_short_name = Column(String(2))
    site_base_url = Column(String(30))
    site_marketplace= Column(String(20))

class ProductHistory(base):
    __tablename__="product_history"
    id = Column(String(10),primary_key=True)
    asin = Column(String(20))
    stars = Column(String(1))
    five_star = Column(String(6))
    four_star = Column(String(6))
    three_star = Column(String(6))
    two_star = Column(String(6))
    one_star = Column(String(6))
    site = Column(String(2))
    positive_vote = Column(Integer)
    negtive_vote = Column(Integer)
    ranking = Column(String(1024))
    updatetime = Column(DateTime)

class UserProfile(base):
    __tablename__="user_profile"
    id = Column(String(10),primary_key=True)
    userid = Column(String(25))
    username = Column(String(128))
    profile_link = Column(String(256))
    profile_id = Column(String(25))
    comment_ranking = Column(String(10))
    email = Column(String(128))

class Comments(base):
    __tablename__="comments"
    id = Column(String(10), primary_key=True)
    comment_id = Column(String(25))
    asin = Column(String(25))
    comment_date = Column(DateTime)
    verified_purchase = Column(String(3))
    stars = Column(10)
    user_id = Column(String(50))
    found_help = Column(Integer)

db = create_engine("sqlite:///amazondb.db")
DBSession = sessionmaker(bind=db)