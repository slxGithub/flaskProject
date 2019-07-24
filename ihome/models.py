from . import db
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from ihome import constants


class BasicModel():
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 更新时间


class User(BasicModel, db.Model):
    __tablename__ = "ih_user_profile"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11), unique=True, nullable=False)
    real_name = db.Column(db.String(32))
    real_card = db.Column(db.String(20))
    avatar_url = db.Column(db.String(128))
    houses = db.relationship("House", backref="user")
    orders = db.relationship("Order", backref="user")

    @property  # 把函数变为属性 # getter @property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值
    def password(self):
        raise AttributeError("这个属性只能设置,不能读取")

    @password.setter  # setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "avatar": constants.YOUPAIYUN_URL_DOMAIN + self.avatar_url if self.avatar_url else "",
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

    def auth_to_dict(self):
        """将实名信息转换为字典数据"""
        auth_dict = {
            "user_id": self.id,
            "real_name": self.real_name,
            "id_card": self.real_card
        }
        return auth_dict


class Area(BasicModel, db.Model):
    __tablename__ = "ih_area_info"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def to_dict(self):
        """将对象转换为字典"""
        d = {
            "aid": self.id,
            "aname": self.name
        }
        return d


# 房屋设施多对多关系
house_facility = db.Table(
    "ih_house_facility",
    db.Column("house_id", db.Integer, db.ForeignKey("ih_house_info.id"), primary_key=True),
    db.Column("facility_id", db.Integer, db.ForeignKey("ih_facility_info.id"), primary_key=True)
)


class House(BasicModel, db.Model):
    __tablename__ = "ih_house_info"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("ih_area_info.id"), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, default=0)
    address = db.Column(db.String(512), default="")
    room_count = db.Column(db.Integer, default=1)
    acreage = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(32), default="")
    capacity = db.Column(db.Integer, default=1)  # 准入几人
    beds = db.Column(db.String(64), default="")  # 床铺配置
    deposit = db.Column(db.Integer, default=0)  # 押金
    min_days = db.Column(db.Integer, default=1)
    max_days = db.Column(db.Integer, default=0)  # 最大入住天数 0 :无限制
    order_count = db.Column(db.Integer, default=0)  # 历史订单数
    index_image_url = db.Column(db.String(256), default="")  # 首页图片
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋设施
    images = db.relationship("HouseImage")
    orders = db.relationship("Order", backref="house")

    def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        house_dict = {
            "house_id": self.id,
            "title": self.title,
            "price": self.price,
            "area_name": self.area.name,
            "img_url": constants.YOUPAIYUN_URL_DOMAIN + self.index_image_url if self.index_image_url else "",
            "room_count": self.room_count,
            "order_count": self.order_count,
            "address": self.address,
            "user_avatar": self.user.avatar_url if self.user.avatar_url else "",
            "ctime": self.create_time.strftime("%Y-%m-%d")
        }
        return house_dict

    def to_full_dict(self):
        """将详细信息转换为字典数据"""
        house_dict = {
            "hid": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name,
            "user_avatar": constants.YOUPAIYUN_URL_DOMAIN + self.user.avatar_url if self.user.avatar_url else "",
            "title": self.title,
            "price": self.price,
            "address": self.address,
            "room_count": self.room_count,
            "acreage": self.acreage,
            "unit": self.unit,
            "capacity": self.capacity,
            "beds": self.beds,
            "deposit": self.deposit,
            "min_days": self.min_days,
            "max_days": self.max_days,
        }

        img_urls = []
        for image in self.images:
            img_urls.append(image.url)
        house_dict["img_urls"] = img_urls

        # 房屋设施
        facilities = []
        for facility in self.facilities:
            facilities.append(facility.id)
        house_dict["facilities"] = facilities

        # 评论信息
        comments = []
        orders = Order.query.filter(Order.house_id == self.id, Order.status == "COMPLETE",
                                    Order.comment != None).order_by(
            Order.update_time.desc()).limit(5)
        for order in orders:
            comment = {
                "comment": order.comment,  # 评论的内容
                "user_name": order.user.name if order.user.name != order.user.mobile else "匿名用户",  # 发表评论的用户
                "ctime": order.update_time.strftime("%Y-%m-%d %H:%M:%S")  # 评价的时间
            }
            comments.append(comment)
        house_dict["comments"] = comments
        return house_dict


class Facility(BasicModel, db.Model):
    __tablename__ = "ih_facility_info"
    id = db.Column(db.Integer, primary_key=True)  # 设施编号
    name = db.Column(db.String(32), nullable=False)  # 设施名字


class HouseImage(BasicModel, db.Model):
    __tablename__ = "ih_house_image"
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)
    url = db.Column(db.String(256), nullable=False)


class Order(BasicModel, db.Model):
    __tablename__ = "ih_order_info"
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)
    begin_date = db.Column(db.DateTime, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    house_price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum(
            "WAIT_ACCEPT",  # 待接单,
            "WAIT_PAYMENT",  # 待支付
            "PAID",  # 已支付
            "WAIT_COMMENT",  # 待评价
            "COMPLETE",  # 已完成
            "CANCELED",  # 已取消
            "REJECTED"  # 已拒单
        ),
        default="WAIT_ACCEPT", index=True
    )
    comment = db.Column(db.Text)
    trade_no = db.Column(db.String(80))  # 流水号

    def to_dict(self):
        """将订单信息转换为字典数据"""
        order_dict = {
            "order_id": self.id,
            "title": self.house.title,
            "img_url": constants.YOUPAIYUN_URL_DOMAIN + self.house.index_image_url if self.house.index_image_url else "",
            "start_date": self.begin_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "ctime": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "days": self.days,
            "amount": self.amount,
            "status": self.status,
            "comment": self.comment if self.comment else ""
        }
        return order_dict
