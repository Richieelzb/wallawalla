from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
    __tablename__ = "user"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cognito_sub = db.Column(
        db.String(255),
        unique=True,
        nullable=True,
        index=True
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    businesses = db.relationship(
        "Business",
        backref="owner",
        lazy=True,
        foreign_keys="Business.user_id"
    )

    properties = db.relationship(
        "Property",
        backref="owner",
        lazy=True,
        foreign_keys="Property.user_id"
    )

    business_claims = db.relationship(
        "BusinessClaim",
        backref="claimant",
        lazy=True,
        foreign_keys="BusinessClaim.claimant_user_id"
    )

    property_claims = db.relationship(
        "PropertyClaim",
        backref="claimant",
        lazy=True,
        foreign_keys="PropertyClaim.claimant_user_id"
    )

    cars = db.relationship(
        "Car",
        backref="owner",
        lazy=True,
        foreign_keys="Car.user_id"
    )

    car_claims = db.relationship(
        "CarClaim",
        backref="claimant",
        lazy=True,
        foreign_keys="CarClaim.claimant_user_id"
    )

    jobs = db.relationship(
        "Job",
        backref="owner",
        lazy=True,
        foreign_keys="Job.user_id"
    )

    job_claims = db.relationship(
        "JobClaim",
        backref="claimant",
        lazy=True,
        foreign_keys="JobClaim.claimant_user_id"
    )

    job_applications = db.relationship(
        "JobApplication",
        backref="applicant",
        lazy=True,
        foreign_keys="JobApplication.applicant_user_id"
    )

class Business(db.Model):
    __tablename__ = "business"

    id = db.Column(db.Integer, primary_key=True)

    # owner_cognito_sub = db.Column(
    #     db.String(255)
    # )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    # ------------------------------
    # LISTING OWNERSHIP / CLAIM
    # ------------------------------

    claim_status = db.Column(
        db.String(30),
        nullable=False,
        default="unclaimed",
        server_default="unclaimed",
        index=True
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    claim_invite_created = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_by_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    listing_source = db.Column(
        db.String(100),
        nullable=True
    )


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
    address = db.Column(db.Text, nullable=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    show_address = db.Column(db.Boolean,default=True)
    show_whatsapp = db.Column(db.Boolean,default=True)
    show_phone = db.Column(db.Boolean,default=True)

    status = db.Column(
        db.String(20),
        default="pending"
    )

    approved_at = db.Column(
        db.DateTime,
        nullable=True
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
        nullable=True
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
    # ANALYTICS
    # ------------------------------

    whatsapp_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    phone_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    website_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
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
    def is_claimed(self):
        return (
            self.claim_status == "claimed"
            and self.user_id is not None
        )

    @property
    def is_unclaimed(self):
        return (
            self.claim_status == "unclaimed"
            and self.user_id is None
        )

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

class BusinessClaim(db.Model):
    __tablename__ = "business_claims"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    business_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "business.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    claimant_user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    claimant_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    claimant_whatsapp = db.Column(
        db.String(30),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        nullable=False,
        unique=True,
        index=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="invited",
        server_default="invited",
        index=True
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    business = db.relationship(
        "Business",
        backref=db.backref(
            "claim_requests",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    @property
    def is_available(self):
        return (
            self.status == "invited"
            and not self.is_expired
        )

class BusinessUpgradeRequest(db.Model):

    __tablename__ = "business_upgrade_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    business_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "business.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    owner_email = db.Column(
        db.String(120),
        nullable=False
    )

    requested_plan = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    business = db.relationship(
        "Business",
        backref=db.backref(
            "upgrade_requests",
            cascade="all, delete-orphan",
            passive_deletes=True
        )
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

    # ------------------------------
    # LISTING OWNERSHIP / CLAIM
    # ------------------------------

    claim_status = db.Column(
        db.String(30),
        nullable=False,
        default="unclaimed",
        server_default="unclaimed",
        index=True
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    claim_invite_created = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_by_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    listing_source = db.Column(
        db.String(100),
        nullable=True
    )

    owner_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
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
    address = db.Column(db.Text, nullable=True)

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

    featured_impressions = db.Column(
        db.Integer,
        nullable=False,
        default=0
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
        nullable=True,
        index=True
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

    linkedin = db.Column(
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
        nullable=True,
        index=True
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

    approved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    special_offer = db.Column(
        db.Text,
        nullable=True
    )

    @property
    def featured(self):
        return self.has_active_featured

    @property
    def is_claimed(self):
        return (
            self.claim_status == "claimed"
            and self.user_id is not None
        )

    @property
    def is_unclaimed(self):
        return (
            self.claim_status == "unclaimed"
            and self.user_id is None
        )

    @property
    def premium(self):
        return self.has_active_premium

    @property
    def subscription_plan(self):

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
    def can_manage_listing(self):
        """
        Premium and Featured users can edit listing details,
        manage images and view analytics.
        """

        return (
            self.has_active_premium
            or self.has_active_featured
        )

    @property
    def can_add_property(self):
        """
        Premium and Featured users can add another property.
        """

        return self.can_manage_listing

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

class PropertyClaim(db.Model):
    __tablename__ = "property_claims"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "properties.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    claimant_user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    claimant_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    claimant_whatsapp = db.Column(
        db.String(30),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        nullable=False,
        unique=True,
        index=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="invited",
        server_default="invited",
        index=True
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    property_listing = db.relationship(
        "Property",
        backref=db.backref(
            "claim_requests",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    @property
    def is_expired(self):

        return (
            datetime.utcnow()
            > self.expires_at
        )

    @property
    def is_available(self):

        return (
            self.status == "invited"
            and not self.is_expired
        )

class PropertyUpgradeRequest(db.Model):
    __tablename__ = "property_upgrade_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "properties.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    owner_email = db.Column(
        db.String(120),
        nullable=False
    )

    requested_plan = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    property_listing = db.relationship(
        "Property",
        backref=db.backref(
            "upgrade_requests",
            cascade="all, delete-orphan",
            passive_deletes=True
        )
    )

class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==================================================
    # OWNER
    # ==================================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    owner_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    # ==================================================
    # LISTING OWNERSHIP / CLAIM
    # ==================================================

    claim_status = db.Column(
        db.String(30),
        nullable=False,
        default="unclaimed",
        server_default="unclaimed",
        index=True
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    claim_invite_created = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    created_by_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    listing_source = db.Column(
        db.String(100),
        nullable=True
    )

    # ==================================================
    # BASIC VEHICLE INFORMATION
    # ==================================================

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    make = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    model = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    variant = db.Column(
        db.String(150),
        nullable=True,
        index=True
    )

    year = db.Column(
        db.Integer,
        nullable=True,
        index=True
    )

    category = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    body_type = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    condition = db.Column(
        db.String(50),
        nullable=True,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # Suggested values:
    #
    # category:
    # Car
    # SUV
    # Bakkie
    # Van
    # Minibus
    # Motorcycle
    # Commercial Vehicle
    # Other
    #
    # condition:
    # New
    # Used
    # Demo

    # ==================================================
    # VEHICLE IDENTIFICATION
    # ==================================================

    reference_number = db.Column(
        db.String(50),
        unique=True,
        nullable=True,
        index=True
    )

    vin_number = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    registration_number = db.Column(
        db.String(50),
        nullable=True,
        index=True
    )

    stock_number = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    # ==================================================
    # PRICING
    # ==================================================

    price = db.Column(
        db.Numeric(12, 2),
        nullable=True,
        index=True
    )

    monthly_instalment = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    deposit_amount = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    finance_available = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    negotiable = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    # ==================================================
    # VEHICLE SPECIFICATIONS
    # ==================================================

    mileage = db.Column(
        db.Integer,
        nullable=True,
        index=True
    )

    transmission = db.Column(
        db.String(50),
        nullable=True,
        index=True
    )

    fuel_type = db.Column(
        db.String(50),
        nullable=True,
        index=True
    )

    colour = db.Column(
        db.String(50),
        nullable=True,
        index=True
    )

    engine_size = db.Column(
        db.String(50),
        nullable=True
    )

    engine_power = db.Column(
        db.String(50),
        nullable=True
    )

    drivetrain = db.Column(
        db.String(50),
        nullable=True
    )

    doors = db.Column(
        db.Integer,
        nullable=True
    )

    seats = db.Column(
        db.Integer,
        nullable=True
    )

    previous_owners = db.Column(
        db.Integer,
        nullable=True
    )

    service_history = db.Column(
        db.String(100),
        nullable=True
    )

    warranty_available = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    accident_history = db.Column(
        db.String(100),
        nullable=True
    )

    # ==================================================
    # SELLER / DEALERSHIP
    # ==================================================

    seller_type = db.Column(
        db.String(50),
        nullable=False,
        default="private",
        server_default="private",
        index=True
    )

    seller_name = db.Column(
        db.String(200),
        nullable=True
    )

    dealership_name = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    contact_name = db.Column(
        db.String(200),
        nullable=True
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    whatsapp = db.Column(
        db.String(30),
        nullable=True
    )

    email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    website = db.Column(
        db.String(500),
        nullable=True
    )

    show_phone = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    show_whatsapp = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    show_address = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    # ==================================================
    # LOCATION
    # ==================================================

    address = db.Column(
        db.Text,
        nullable=True
    )

    suburb = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    city = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    province = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    latitude = db.Column(
        db.Float,
        nullable=True,
        index=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True,
        index=True
    )

    # ==================================================
    # APPROVAL AND AVAILABILITY
    # ==================================================

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
        server_default="pending",
        index=True
    )

    # Suggested status values:
    #
    # pending
    # approved
    # rejected

    listing_status = db.Column(
        db.String(30),
        nullable=False,
        default="available",
        server_default="available",
        index=True
    )

    # Suggested listing_status values:
    #
    # available
    # reserved
    # sold
    # unavailable

    approved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==================================================
    # PREMIUM PLAN
    # ==================================================

    is_premium = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True
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

    # ==================================================
    # FEATURED PLAN
    # ==================================================

    is_featured = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True
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

    featured_position = db.Column(
        db.Integer,
        nullable=False,
        default=100,
        server_default="100"
    )

    # ==================================================
    # VERIFICATION
    # ==================================================

    verification_status = db.Column(
        db.String(30),
        nullable=False,
        default="not_requested",
        server_default="not_requested",
        index=True
    )

    # Suggested verification_status values:
    #
    # not_requested
    # pending
    # verified
    # rejected

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

    # ==================================================
    # ONLINE LINKS
    # ==================================================

    facebook = db.Column(
        db.String(500),
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

    special_offer = db.Column(
        db.Text,
        nullable=True
    )

    # ==================================================
    # ANALYTICS
    # ==================================================

    views = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    listing_impressions = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    search_appearances = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    featured_impressions = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    phone_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    whatsapp_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    email_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    website_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    directions_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    gallery_views = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    last_viewed = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==================================================
    # TIMESTAMPS
    # ==================================================

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    images = db.relationship(
        "CarImage",
        backref="car",
        lazy=True,
        order_by="CarImage.display_order",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    features = db.relationship(
        "CarFeature",
        backref="car",
        lazy=True,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # ==================================================
    # CLAIM HELPERS
    # ==================================================

    @property
    def is_claimed(self):
        return (
            self.claim_status == "claimed"
            and self.user_id is not None
        )

    @property
    def is_unclaimed(self):
        return (
            self.claim_status == "unclaimed"
            and self.user_id is None
        )

    # ==================================================
    # SUBSCRIPTION HELPERS
    # ==================================================

    @property
    def has_active_premium(self):
        if not self.is_premium:
            return False

        if self.premium_expires_at is None:
            return True

        return (
            self.premium_expires_at
            > datetime.utcnow()
        )

    @property
    def has_active_featured(self):
        if not self.is_featured:
            return False

        if self.featured_expires_at is None:
            return True

        return (
            self.featured_expires_at
            > datetime.utcnow()
        )

    @property
    def premium(self):
        return self.has_active_premium

    @property
    def featured(self):
        return self.has_active_featured

    @property
    def verified(self):
        return (
            self.verification_status
            == "verified"
        )

    @property
    def subscription_plan(self):
        """
        Featured takes precedence over Premium.
        Premium takes precedence over Verified.
        Verified takes precedence over Free.
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
        Premium and Featured account holders can manage
        all listing details, images, and analytics.
        """

        return (
            self.has_active_premium
            or self.has_active_featured
        )

    @property
    def can_add_car(self):
        """
        Premium and Featured account holders can add
        additional vehicle listings.
        """

        return self.can_manage_listing

    @property
    def dashboard_images(self):
        """
        Free and Verified plans see up to three images.
        Premium and Featured plans see all images.
        """

        if self.can_manage_listing:
            return self.images

        return self.images[:3]

    @property
    def main_image(self):
        if not self.images:
            return None

        return self.images[0]

    @property
    def display_title(self):
        """
        Build a vehicle title if the stored title is empty.
        """

        if self.title:
            return self.title

        title_parts = [
            self.year,
            self.make,
            self.model,
            self.variant
        ]

        title = " ".join(
            str(value)
            for value in title_parts
            if value not in (
                None,
                ""
            )
        )

        return title or "Car"


class CarImage(db.Model):
    __tablename__ = "car_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "cars.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    image_url = db.Column(
        db.String(1000),
        nullable=False
    )

    display_order = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    is_primary = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


class CarFeature(db.Model):
    __tablename__ = "car_features"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "cars.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    feature_name = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    feature_category = db.Column(
        db.String(100),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


class CarClaim(db.Model):
    __tablename__ = "car_claims"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "cars.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    claimant_user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    claimant_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    claimant_whatsapp = db.Column(
        db.String(30),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        nullable=False,
        unique=True,
        index=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="invited",
        server_default="invited",
        index=True
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    car_listing = db.relationship(
        "Car",
        backref=db.backref(
            "claim_requests",
            lazy=True,
            cascade="all, delete-orphan",
            passive_deletes=True
        )
    )

    @property
    def is_expired(self):
        return (
            datetime.utcnow()
            > self.expires_at
        )

    @property
    def is_available(self):
        return (
            self.status == "invited"
            and not self.is_expired
        )


class CarUpgradeRequest(db.Model):
    __tablename__ = "car_upgrade_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "cars.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    owner_email = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    requested_plan = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
        server_default="pending",
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    car_listing = db.relationship(
        "Car",
        backref=db.backref(
            "upgrade_requests",
            cascade="all, delete-orphan",
            passive_deletes=True
        )
    )

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==================================================
    # EMPLOYER / OWNER
    # ==================================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    owner_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    # ==================================================
    # LISTING OWNERSHIP / CLAIM
    # ==================================================

    claim_status = db.Column(
        db.String(30),
        nullable=False,
        default="unclaimed",
        server_default="unclaimed",
        index=True
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    claim_invite_created = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    created_by_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    listing_source = db.Column(
        db.String(100),
        nullable=True
    )

    # ==================================================
    # BASIC JOB INFORMATION
    # ==================================================

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    company_name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    company_description = db.Column(
        db.Text,
        nullable=True
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    subcategory = db.Column(
        db.String(150),
        nullable=True,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    responsibilities = db.Column(
        db.Text,
        nullable=True
    )

    requirements = db.Column(
        db.Text,
        nullable=True
    )

    qualifications = db.Column(
        db.Text,
        nullable=True
    )

    skills = db.Column(
        db.Text,
        nullable=True
    )

    benefits = db.Column(
        db.Text,
        nullable=True
    )

    reference_number = db.Column(
        db.String(50),
        unique=True,
        nullable=True,
        index=True
    )

    # Suggested category values:
    #
    # Admin & Office
    # Skilled Trades
    # IT & Technology
    # Sales & Retail
    # Healthcare
    # Education
    # Hospitality
    # Driving & Logistics
    # Security
    # Finance
    # Marketing
    # Engineering
    # Other

    # ==================================================
    # EMPLOYMENT DETAILS
    # ==================================================

    employment_type = db.Column(
        db.String(50),
        nullable=False,
        default="full_time",
        server_default="full_time",
        index=True
    )

    # Suggested employment_type values:
    #
    # full_time
    # part_time
    # contract
    # temporary
    # internship
    # learnership
    # apprenticeship
    # freelance
    # volunteer

    workplace_type = db.Column(
        db.String(50),
        nullable=False,
        default="on_site",
        server_default="on_site",
        index=True
    )

    # Suggested workplace_type values:
    #
    # on_site
    # hybrid
    # remote

    experience_level = db.Column(
        db.String(50),
        nullable=True,
        index=True
    )

    # Suggested experience_level values:
    #
    # no_experience
    # entry_level
    # junior
    # mid_level
    # senior
    # management
    # executive

    minimum_experience_years = db.Column(
        db.Integer,
        nullable=True
    )

    education_level = db.Column(
        db.String(100),
        nullable=True
    )

    number_of_positions = db.Column(
        db.Integer,
        nullable=False,
        default=1,
        server_default="1"
    )

    # ==================================================
    # SALARY
    # ==================================================

    salary_min = db.Column(
        db.Numeric(12, 2),
        nullable=True,
        index=True
    )

    salary_max = db.Column(
        db.Numeric(12, 2),
        nullable=True,
        index=True
    )

    salary_period = db.Column(
        db.String(30),
        nullable=True,
        index=True
    )

    # Suggested salary_period values:
    #
    # hourly
    # daily
    # weekly
    # monthly
    # annual

    salary_currency = db.Column(
        db.String(10),
        nullable=False,
        default="ZAR",
        server_default="ZAR"
    )

    salary_negotiable = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    show_salary = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    # ==================================================
    # LOCATION
    # ==================================================

    address = db.Column(
        db.Text,
        nullable=True
    )

    suburb = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    city = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    province = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    postal_code = db.Column(
        db.String(20),
        nullable=True
    )

    latitude = db.Column(
        db.Float,
        nullable=True,
        index=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True,
        index=True
    )

    show_address = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    # ==================================================
    # EMPLOYER CONTACT
    # ==================================================

    contact_name = db.Column(
        db.String(200),
        nullable=True
    )

    contact_position = db.Column(
        db.String(150),
        nullable=True
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    whatsapp = db.Column(
        db.String(30),
        nullable=True
    )

    email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    website = db.Column(
        db.String(500),
        nullable=True
    )

    application_email = db.Column(
        db.String(255),
        nullable=True
    )

    external_application_url = db.Column(
        db.String(1000),
        nullable=True
    )

    application_method = db.Column(
        db.String(50),
        nullable=False,
        default="wallawalla",
        server_default="wallawalla"
    )

    # Suggested application_method values:
    #
    # wallawalla
    # email
    # website
    # whatsapp
    # phone

    show_phone = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    show_whatsapp = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    show_email = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    # ==================================================
    # APPLICATION DATES
    # ==================================================

    application_opening_date = db.Column(
        db.Date,
        nullable=True,
        index=True
    )

    application_closing_date = db.Column(
        db.Date,
        nullable=True,
        index=True
    )

    start_date = db.Column(
        db.Date,
        nullable=True
    )

    # ==================================================
    # APPROVAL AND LISTING STATUS
    # ==================================================

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
        server_default="pending",
        index=True
    )

    # Suggested status values:
    #
    # pending
    # approved
    # rejected

    listing_status = db.Column(
        db.String(30),
        nullable=False,
        default="open",
        server_default="open",
        index=True
    )

    # Suggested listing_status values:
    #
    # open
    # paused
    # filled
    # closed
    # expired
    # unavailable

    approved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    # ==================================================
    # PREMIUM PLAN
    # ==================================================

    is_premium = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True
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

    # ==================================================
    # FEATURED PLAN
    # ==================================================

    is_featured = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True
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

    featured_position = db.Column(
        db.Integer,
        nullable=False,
        default=100,
        server_default="100"
    )

    # ==================================================
    # EMPLOYER VERIFICATION
    # ==================================================

    verification_status = db.Column(
        db.String(30),
        nullable=False,
        default="not_requested",
        server_default="not_requested",
        index=True
    )

    # Suggested verification_status values:
    #
    # not_requested
    # pending
    # verified
    # rejected

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

    # ==================================================
    # COMPANY LINKS
    # ==================================================

    facebook = db.Column(
        db.String(500),
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

    # ==================================================
    # ANALYTICS
    # ==================================================

    views = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    listing_impressions = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    search_appearances = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    featured_impressions = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    application_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    applications_received = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    phone_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    whatsapp_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    email_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    website_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    directions_clicks = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    last_viewed = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==================================================
    # TIMESTAMPS
    # ==================================================

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    applications = db.relationship(
        "JobApplication",
        backref="job",
        lazy=True,
        order_by="JobApplication.created_at.desc()",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # ==================================================
    # CLAIM HELPERS
    # ==================================================

    @property
    def is_claimed(self):
        return (
            self.claim_status == "claimed"
            and self.user_id is not None
        )

    @property
    def is_unclaimed(self):
        return (
            self.claim_status == "unclaimed"
            and self.user_id is None
        )

    # ==================================================
    # SUBSCRIPTION HELPERS
    # ==================================================

    @property
    def has_active_premium(self):
        if not self.is_premium:
            return False

        if self.premium_expires_at is None:
            return True

        return (
            self.premium_expires_at
            > datetime.utcnow()
        )

    @property
    def has_active_featured(self):
        if not self.is_featured:
            return False

        if self.featured_expires_at is None:
            return True

        return (
            self.featured_expires_at
            > datetime.utcnow()
        )

    @property
    def premium(self):
        return self.has_active_premium

    @property
    def featured(self):
        return self.has_active_featured

    @property
    def verified(self):
        return (
            self.verification_status
            == "verified"
        )

    @property
    def subscription_plan(self):
        """
        Featured takes precedence over Premium.
        Premium takes precedence over Verified.
        Verified takes precedence over Free.
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
        Premium and Featured employers can manage all
        listing details and view listing analytics.
        """

        return (
            self.has_active_premium
            or self.has_active_featured
        )

    @property
    def can_add_job(self):
        """
        Premium and Featured employers can add
        additional job listings.
        """

        return self.can_manage_listing

    # ==================================================
    # JOB STATE HELPERS
    # ==================================================

    @property
    def is_expired(self):
        if self.application_closing_date is None:
            return False

        return (
            self.application_closing_date
            < datetime.utcnow().date()
        )

    @property
    def is_open(self):
        return (
            self.status == "approved"
            and self.listing_status == "open"
            and not self.is_expired
        )

    @property
    def salary_display(self):
        """
        Return a display-ready South African Rand salary.
        """

        if not self.show_salary:
            return "Salary not disclosed"

        if (
            self.salary_min is None
            and self.salary_max is None
        ):
            return "Market related"

        period_labels = {
            "hourly": "per hour",
            "daily": "per day",
            "weekly": "per week",
            "monthly": "per month",
            "annual": "per year"
        }

        period = period_labels.get(
            self.salary_period,
            ""
        )

        if (
            self.salary_min is not None
            and self.salary_max is not None
        ):
            return (
                f"R{self.salary_min:,.0f} - "
                f"R{self.salary_max:,.0f} "
                f"{period}"
            ).strip()

        if self.salary_min is not None:
            return (
                f"From R{self.salary_min:,.0f} "
                f"{period}"
            ).strip()

        return (
            f"Up to R{self.salary_max:,.0f} "
            f"{period}"
        ).strip()

    @property
    def applications_count(self):
        return len(self.applications)


class JobApplication(db.Model):
    __tablename__ = "job_applications"

    __table_args__ = (
        db.UniqueConstraint(
            "job_id",
            "email",
            name=(
                "uq_job_application_"
                "job_email"
            )
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "jobs.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    applicant_user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    full_name = db.Column(
        db.String(255),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    whatsapp = db.Column(
        db.String(30),
        nullable=True
    )

    location = db.Column(
        db.String(255),
        nullable=True
    )

    linkedin_url = db.Column(
        db.String(500),
        nullable=True
    )

    cover_letter = db.Column(
        db.Text,
        nullable=True
    )

    cv_url = db.Column(
        db.String(1000),
        nullable=True
    )

    cv_s3_key = db.Column(
        db.String(1000),
        nullable=False
    )

    cv_original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    cv_content_type = db.Column(
        db.String(150),
        nullable=True
    )

    cv_size = db.Column(
        db.Integer,
        nullable=True
    )

    supporting_document_url = db.Column(
        db.String(1000),
        nullable=True
    )

    supporting_document_s3_key = db.Column(
        db.String(1000),
        nullable=True
    )

    supporting_document_original_filename = db.Column(
        db.String(255),
        nullable=True
    )

    supporting_document_content_type = db.Column(
        db.String(150),
        nullable=True
    )

    supporting_document_size = db.Column(
        db.Integer,
        nullable=True
    )

    consent_given = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    consent_at = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="submitted",
        server_default="submitted",
        index=True
    )

    employer_notes = db.Column(
        db.Text,
        nullable=True
    )

    viewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @property
    def application_reference(self):
        if not self.id:
            return None

        return (
            f"WA-JOB-"
            f"{self.job_id}-"
            f"{self.id}"
        )

    @property
    def is_new(self):
        return (
            self.status
            == "submitted"
        )

class JobClaim(db.Model):
    __tablename__ = "job_claims"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "jobs.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    claimant_user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    claimant_email = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    claimant_whatsapp = db.Column(
        db.String(30),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        nullable=False,
        unique=True,
        index=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="invited",
        server_default="invited",
        index=True
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    job_listing = db.relationship(
        "Job",
        backref=db.backref(
            "claim_requests",
            lazy=True,
            cascade="all, delete-orphan",
            passive_deletes=True
        )
    )

    @property
    def is_expired(self):
        return (
            datetime.utcnow()
            > self.expires_at
        )

    @property
    def is_available(self):
        return (
            self.status == "invited"
            and not self.is_expired
        )


class JobUpgradeRequest(db.Model):
    __tablename__ = "job_upgrade_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "jobs.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    owner_email = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    requested_plan = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
        server_default="pending",
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    job_listing = db.relationship(
        "Job",
        backref=db.backref(
            "upgrade_requests",
            cascade="all, delete-orphan",
            passive_deletes=True
        )
    )