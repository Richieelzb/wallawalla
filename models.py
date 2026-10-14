from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import Time, Date


db = SQLAlchemy()

class ActivationToken(db.Model):
    __tablename__ = "activation_tokens"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        nullable=False
    )

    token = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    cognito_sub = db.Column(
        db.String(255),
        unique=True
    )

    email = db.Column(
        db.String(255),
        unique=True
    )

    businesses = db.relationship(
        "Business",
        backref="owner",
        lazy=True
    )

    properties = db.relationship(
        "Property",
        backref="owner",
        lazy=True
)


class Business(db.Model):
    __tablename__ = "business"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    # owner_cognito_sub = db.Column(
    #     db.String(255)
    # )

    business_name = db.Column(db.String(200))
    category = db.Column(db.String(100))
    subcategory = db.Column(
        db.Text,
        nullable=True
    )

    description = db.Column(db.Text)
    # Opening Hours

    mon_thu_open = db.Column(db.Time, nullable=True)
    mon_thu_close = db.Column(db.Time, nullable=True)

    fri_open = db.Column(db.Time, nullable=True)
    fri_close = db.Column(db.Time, nullable=True)

    sat_open = db.Column(db.Time, nullable=True)
    sat_close = db.Column(db.Time, nullable=True)

    sun_open = db.Column(db.Time, nullable=True)
    sun_close = db.Column(db.Time, nullable=True)

    holiday_open = db.Column(db.Time, nullable=True)
    holiday_close = db.Column(db.Time, nullable=True)

    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(255))

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    show_address = db.Column(db.Boolean,default=False)
    show_whatsapp = db.Column(db.Boolean,default=False)
    show_phone = db.Column(db.Boolean,default=True)

    status = db.Column(
        db.String(20),
        default="pending"
    )

    views = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    last_viewed = db.Column(
        db.DateTime,
        nullable=True
    )

    images = db.relationship(
        "BusinessImage",
        backref="business",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ------------------------------
    # PREMIUM PROFILE
    # ------------------------------
    is_premium = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    premium_started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    premium_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ------------------------------
    # FEATURED LISTING
    # ------------------------------
    is_featured = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    featured_started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    featured_expires_at = db.Column(
        db.DateTime,
        nullable=True,
        index=True
    )

    # Lower number means a higher featured position.
    featured_position = db.Column(
        db.Integer,
        nullable=False,
        default=100
    )

    # ------------------------------
    # VERIFIED BUSINESS
    # ------------------------------
    verification_status = db.Column(
        db.String(30),
        nullable=False,
        default="not_requested"
    )

    verification_requested_at = db.Column(
        db.DateTime,
        nullable=True
    )

    verified_at = db.Column(
        db.DateTime,
        nullable=True
    )

    verification_rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    # ------------------------------
    # ANALYTICS
    # ------------------------------

    whatsapp_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    phone_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    website_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    website = db.Column(
        db.String(500),
        nullable=True
    )

    facebook = db.Column(
        db.String(500),
        nullable=True
    )

    special_offer = db.Column(
        db.Text,
        nullable=True
    )

    instagram = db.Column(
        db.String(500),
        nullable=True
    )

    linkedin = db.Column(
        db.String(500),
        nullable=True
    )

    tiktok = db.Column(
        db.String(500),
        nullable=True
    )

    youtube = db.Column(
        db.String(500),
        nullable=True
    )

    x_twitter = db.Column(
        db.String(500),
        nullable=True
    )

    # -------------------------------------------------
    # SUBSCRIPTION HELPERS
    # -------------------------------------------------

    @property
    def has_active_premium(self):
        if not self.is_premium:
            return False

        if self.premium_expires_at is None:
            return True

        return self.premium_expires_at > datetime.utcnow()

    @property
    def has_active_featured(self):
        if not self.is_featured:
            return False

        if self.featured_expires_at is None:
            return True

        return self.featured_expires_at > datetime.utcnow()

    @property
    def verified(self):
        return self.verification_status == "verified"

    @property
    def premium(self):
        return self.has_active_premium

    @property
    def featured(self):
        return self.has_active_featured

    @property
    def subscription_plan(self):
        """
        Featured takes precedence over Premium,
        Premium over Verified, and Verified over Free.
        """

        if self.has_active_featured:
            return "featured"

        if self.has_active_premium:
            return "premium"

        if self.verified:
            return "verified"

        return "free"

    @property
    def subscription_end(self):
        if self.has_active_featured:
            return self.featured_expires_at

        if self.has_active_premium:
            return self.premium_expires_at

        return None

    @property
    def can_manage_listing(self):
        """
        Premium and Featured users can edit listing details,
        manage images, and view analytics.
        """

        return (
            self.has_active_premium
            or self.has_active_featured
        )

    @property
    def can_add_business(self):
        """
        Premium and Featured users can add another business.
        """

        return self.can_manage_listing

    @property
    def dashboard_images(self):
        """
        Free and Verified plans see one image.
        Premium and Featured plans see all images.
        """

        if self.can_manage_listing:
            return self.images

        return self.images[:1]

class BusinessImage(db.Model):
    __tablename__ = "business_images"

    id = db.Column(db.Integer, primary_key=True)

    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.id"),
        nullable=False
    )

    image_url = db.Column(
        db.String(1000),
        nullable=False
    )

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Owner
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    email = db.Column(
        db.String(255),
        nullable=False
    )

    # Property Information
    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    property_type = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    listing_type = db.Column(
        db.Text,
        nullable=False,
        index=True
    )

    status = db.Column(
        db.String(20),
        default="pending",
        index=True
    )

     # pending
        # approved
        # rejected
        # sold
        # rented

    description = db.Column(
        db.Text,
        nullable=True
    )
    # House
    # Apartment
    # Flat
    # Townhouse
    # Room
    # Commercial
    # Land
    # Farm
    # sale
    # rent
    # short_term

    # Pricing
    price = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    monthly_rent = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    deposit_amount = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    # Property Details
    bedrooms = db.Column(
        db.Float,
        nullable=True
    )

    bathrooms = db.Column(
        db.Float,
        nullable=True
    )

    parking_spaces = db.Column(
        db.Integer,
        nullable=True
    )

    floor_size = db.Column(
        db.Float,
        nullable=True
    )

    land_size = db.Column(
        db.Float,
        nullable=True
    )

    furnished = db.Column(
        db.Boolean,
        default=False
    )

    pet_friendly = db.Column(
        db.Boolean,
        default=False
    )

    # Contact Information
    contact_name = db.Column(
        db.String(200),
        nullable=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    whatsapp = db.Column(
        db.String(20),
        nullable=True
    )

    email = db.Column(
        db.String(255),
        nullable=True
    )

    # Address
    address = db.Column(
        db.String(500),
        nullable=False
    )

    suburb = db.Column(
        db.String(100),
        nullable=True
    )

    city = db.Column(
        db.String(100),
        nullable=True
    )

    province = db.Column(
        db.String(100),
        nullable=True
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    verification_rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    property_condition = db.Column(
        db.String(50),
        nullable=True
    )

    available_from = db.Column(
        db.Date,
        nullable=True
    )

    agent_name = db.Column(
        db.String(255),
        nullable=True
    )

    agency_name = db.Column(
        db.String(255),
        nullable=True
    )

   

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Analytics
    views = db.Column(
        db.Integer,
        default=0
    )

    whatsapp_clicks = db.Column(
        db.Integer,
        default=0
    )

    phone_clicks = db.Column(
        db.Integer,
        default=0
    )

    email_clicks = db.Column(
        db.Integer,
        default=0
    )

    # Premium
    is_premium = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    premium_started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    premium_expires_at = db.Column(
        db.DateTime,
        nullable=True,
        index=True
    )

    # Featured
    is_featured = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    featured_started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    featured_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    featured_position = db.Column(
        db.Integer,
        nullable=False,
        default=100
    )

    last_viewed = db.Column(
        db.DateTime,
        nullable=True
    )

    youtube = db.Column(
        db.String(500),
        nullable=True
    )

    x_twitter = db.Column(
        db.String(500),
        nullable=True
    )

    facebook = db.Column(
        db.String(500),
        nullable=True
    )

    instagram = db.Column(
        db.String(500),
        nullable=True
    )

    tiktok = db.Column(
        db.String(500),
        nullable=True
    )

    listing_status = db.Column(
        db.String(30),
        nullable=False,
        default="available"
    )

    sale_or_rent = db.Column(
        db.String(30),
        nullable=False,
    )

    images = db.relationship(
        "PropertyImage",
        backref="property",
        lazy=True,
        order_by="PropertyImage.display_order",
        cascade="all, delete-orphan"
    )

    features = db.relationship(
        "PropertyFeature",
        backref="property",
        lazy=True,
        cascade="all, delete-orphan"
    )

    verification_status = db.Column(
        db.String(30),
        nullable=False,
        default="not_requested"
    )

    verification_requested_at = db.Column(
        db.DateTime,
        nullable=True
    )

    verified_at = db.Column(
        db.DateTime,
        nullable=True
    )

    reference_number = db.Column(
        db.String(50),
        unique=True,
        nullable=True
    )

    show_phone = db.Column(
        db.Boolean,
        default=True
    )

    show_whatsapp = db.Column(
        db.Boolean,
        default=True
    )

    show_address = db.Column(
        db.Boolean,
        default=True
    )

    owner_type = db.Column(
        db.String(50),
        nullable=True
    )

    website_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    directions_clicks = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    website = db.Column(
        db.String(500),
        nullable=True
    )

    listing_impressions = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    search_appearances = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    gallery_views = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    @property
    def featured(self):
        return self.has_active_featured

    @property
    def premium(self):
        return self.has_active_premium

    @property
    def subscription_plan(self):

        if self.has_active_featured:
            return "featured"

        if self.has_active_premium:
            return "premium"

        return "free"

    @property
    def subscription_end(self):

        if self.has_active_featured:
            return self.featured_expires_at

        if self.has_active_premium:
            return self.premium_expires_at

        return None

    @property
    def has_active_premium(self):

        if not self.is_premium:
            return False

        if self.premium_expires_at is None:
            return True

        return self.premium_expires_at > datetime.utcnow()

    @property
    def has_active_featured(self):

        if not self.is_featured:
            return False

        if self.featured_expires_at is None:
            return True

        return self.featured_expires_at > datetime.utcnow()

    @property
    def verified(self):
        return self.verification_status == "verified"

    @property
    def dashboard_images(self):

        if (
            self.has_active_premium
            or self.has_active_featured
        ):
            return self.images

        return self.images[:3]


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    image_url = db.Column(
        db.String(1000),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    display_order = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )


class PropertyFeature(db.Model):
    __tablename__ = "property_features"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    feature_name = db.Column(
        db.String(100),
        nullable=False
    )