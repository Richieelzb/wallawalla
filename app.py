import os
import requests
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    session
)
from sqlalchemy import or_, func
from sqlalchemy import cast, String
from flask_sqlalchemy import SQLAlchemy
from models import db, Business, Property
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.route("/")
def home():

    email = session.get("email")

    property = None

    if email:
        property = Property.query.filter_by(
            email=email
        ).first()

    featured_property_count = (
        Property.query
        .filter(
            Property.status == "approved",
            Property.is_featured.is_(True),
            or_(
                Property.featured_expires_at.is_(None),
                Property.featured_expires_at > utc_now()
            )
        )
        .count()
    )

    premium_category_counts = (
        get_premium_category_counts()
    )

    premium_property_count = sum(
        item["count"]
        for item in premium_category_counts
    )

    return render_template(
        "frontend.html",
        email=email,
        property=property,
        featured_property_count=featured_property_count,
        premium_property_count=premium_property_count,
        premium_category_counts=premium_category_counts
    )


COGNITO_USER_POOL_ID = os.getenv(
    "COGNITO_USER_POOL_ID"
)

COGNITO_CLIENT_ID = os.getenv(
    "COGNITO_CLIENT_ID"
)

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME"
)

SES_REGION = os.getenv(
    "SES_REGION"
)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY"
)

app.config["SESSION_COOKIE_DOMAIN"] = ".wallawalla.co.za"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://"
    f"{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def utc_now():
    """
    Return a timezone-naive UTC datetime because the existing database
    DateTime columns are likely stored without timezone information.
    """
    return datetime.utcnow()


def has_active_premium(business):
    if not business.is_premium:
        return False

    if business.premium_expires_at is None:
        return True

    return business.premium_expires_at > utc_now()


def has_active_featured_listing(business):
    if not business.is_featured:
        return False

    if business.featured_expires_at is None:
        return True

    return business.featured_expires_at > utc_now()

def is_business_visible_by_distance(
    business,
    distance
):
    """
    Distance visibility rules:

    Featured:
        No distance restriction.

    Premium:
        Visible up to 300 km.

    Verified:
        Visible up to 100 km.

    Free:
        Visible up to 50 km.
    """

    # Featured first
    if has_active_featured_listing(business):
        return True

    # Premium
    if has_active_premium(business):
        return distance <= 300

    # Verified
    if is_verified_business(business):
        return distance <= 100

    # Free
    return distance <= 50


def is_verified_business(business):
    return business.verification_status == "verified"


@app.context_processor
def business_status_helpers():
    return {
        "has_active_premium": has_active_premium,
        "has_active_featured_listing": has_active_featured_listing,
        "is_verified_business": is_verified_business
    }

# @app.route("/")
# def home():
#  return render_template("index.html")


def distance_km(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


@app.route("/api/business-count")
def business_count():

    lat = request.args.get(
        "lat",
        type=float
    )

    lng = request.args.get(
        "lng",
        type=float
    )

    if lat is None or lng is None:
        return jsonify({
            "count": 0
        })

    businesses = (
        Business.query
        .filter(
            Business.status == "approved",
            Business.latitude.isnot(None),
            Business.longitude.isnot(None)
        )
        .all()
    )

    count = 0

    for business in businesses:

        distance = calculate_distance(
            lat,
            lng,
            business.latitude,
            business.longitude
        )

        if is_business_visible_by_distance(
            business,
            distance
        ):
            count += 1

    return jsonify({
        "count": count
    })

@app.route("/pricing")
def pricing():

    email = session.get("email")

    business = None

    if email:
        business = Business.query.filter_by(
            email=email
        ).first()

    return render_template(
        "pricing.html",
        email=email,
        business=business
    )

@app.route(
    "/business/request-verification",
    methods=["POST"]
)
def request_business_verification():

    email = session.get("email")

    if not email:
        return jsonify({
            "status": "error",
            "message": (
                "Please sign in before requesting "
                "business verification."
            )
        }), 401

    data = request.get_json()

    business_id = data.get(
        "business_id"
    )

    business = Business.query.filter_by(
        id=business_id,
        email=email
    ).first()

    if not business:
        return jsonify({
            "status": "error",
            "message": (
                "No business profile was found for "
                "your account."
            )
        }), 404

    if business.status != "approved":
        return jsonify({
            "status": "error",
            "message": (
                "Your business must be approved before "
                "you can request verification."
            )
        }), 400

    if business.verification_status == "verified":
        return jsonify({
            "status": "error",
            "message": "Your business is already verified."
        }), 400

    if business.verification_status == "pending":
        return jsonify({
            "status": "error",
            "message": (
                "Your verification request is already "
                "being reviewed."
            )
        }), 400

    business.verification_status = "pending"
    business.verification_requested_at = utc_now()
    business.verification_rejection_reason = None

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": (
            "Your verification request has been submitted. "
            "WallaWalla will review your business information."
        )
    }), 200

@app.route("/api/featured-businesses")
def get_featured_businesses():

    latitude = request.args.get(
        "latitude",
        type=float
    )

    longitude = request.args.get(
        "longitude",
        type=float
    )

    if latitude is None or longitude is None:
        return jsonify({
            "status": "error",
            "message": (
                "Location is required to arrange "
                "Featured businesses by distance."
            )
        }), 400

    featured_businesses = (
        Business.query
        .filter(
            Business.status == "approved",
            Business.is_featured.is_(True),
            or_(
                Business.featured_expires_at.is_(None),
                Business.featured_expires_at > utc_now()
            )
        )
        .all()
    )

    results = []

    for business in featured_businesses:

        distance = None

        if (
            business.latitude is not None
            and business.longitude is not None
        ):
            distance = calculate_distance(
                latitude,
                longitude,
                business.latitude,
                business.longitude
            )

        results.append({
            "id": business.id,
            "business_name": business.business_name,
            "category": business.category or "Other",
            "subcategory": business.subcategory,
            "description": business.description,
            "distance": distance,
            "is_featured": True,
            "is_premium": has_active_premium(business),
            "is_verified": is_verified_business(business)
        })

    # Closest Featured businesses first.
    # Businesses without coordinates are placed last.
    results.sort(
        key=lambda item: (
            item["distance"] is None,
            item["distance"]
                if item["distance"] is not None
                else float("inf"),
            item["business_name"] or ""
        )
    )

    return jsonify({
        "status": "success",
        "total": len(results),
        "businesses": results
    }), 200

@app.route("/api/premium-businesses")
def get_premium_businesses():

    category = request.args.get(
        "category",
        ""
    ).strip()

    latitude = request.args.get(
        "latitude",
        type=float
    )

    longitude = request.args.get(
        "longitude",
        type=float
    )

    if not category:
        return jsonify({
            "status": "error",
            "message": "Please select a category."
        }), 400

    if latitude is None or longitude is None:
        return jsonify({
            "status": "error",
            "message": (
                "Location is required to arrange "
                "Premium businesses by distance."
            )
        }), 400

    query = Business.query.filter(
        Business.status == "approved",
        Business.is_premium.is_(True),
        or_(
            Business.premium_expires_at.is_(None),
            Business.premium_expires_at > utc_now()
        )
    )

    if category == "Other":

        normalized_category = func.coalesce(
            func.nullif(
                func.trim(Business.category),
                ""
            ),
            "Other"
        )

        query = query.filter(
            normalized_category == "Other"
        )

    else:

        query = query.filter(
            func.lower(
                func.trim(Business.category)
            ) == category.lower()
        )

    matching_businesses = query.all()

    results = []

    for business in matching_businesses:

        if (
            business.latitude is None
            or business.longitude is None
        ):
            continue

        distance = calculate_distance(
            latitude,
            longitude,
            business.latitude,
            business.longitude
        )

        featured_active = (
            has_active_featured_listing(
                business
            )
        )

        # Featured has no distance restriction.
        # Normal Premium is restricted to 300 km.
        if (
            not featured_active
            and distance > 300
        ):
            continue

        results.append({
            "id": business.id,
            "business_name": (
                business.business_name
            ),
            "category": (
                business.category or "Other"
            ),
            "subcategory": (
                business.subcategory
            ),
            "description": (
                business.description
            ),
            "distance": distance,
            "is_featured": featured_active,
            "is_premium": True,
            "is_verified": (
                is_verified_business(
                    business
                )
            )
        })

    results.sort(
        key=lambda item: (
            item["distance"] is None,
            item["distance"]
                if item["distance"] is not None
                else float("inf"),
            item["business_name"] or ""
        )
    )

    return jsonify({
        "status": "success",
        "category": category,
        "total": len(results),
        "businesses": results
    }), 200

def get_address(lat, lng):
    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={lat},{lng}"
        f"&key={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["results"]:
        return data["results"][0]["formatted_address"]

    return "Location not found"

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(R * c, 1)

@app.template_filter("hours")
def hours_display(value):
    return value.strftime("%H:%M") if value else "Closed"

@app.template_global()
def whatsapp_link(number):
    if not number:
        return None

    number = str(number).strip()

    # Remove common formatting
    number = number.replace(" ", "")
    number = number.replace("-", "")
    number = number.replace("(", "")
    number = number.replace(")", "")

    # South African local format: 0821234567 → 27821234567
    if number.startswith("0"):
        number = "27" + number[1:]

    # International format: +27821234567 → 27821234567
    elif number.startswith("+"):
        number = number[1:]

    return "https://wa.me/" + number

@app.route("/search")
def search():
    query = request.args.get("query")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    try:
        url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?keyword={query}"
            f"&location={latitude},{longitude}"
            "&radius=10000"
            f"&key={API_KEY}"
        )

        response = requests.get(url)
        data = response.json()

        results = []

        for place in data.get("results", []):

            place_lat = place["geometry"]["location"]["lat"]
            place_lng = place["geometry"]["location"]["lng"]

            address = get_address(place_lat, place_lng)

            distance = calculate_distance(float(latitude), float(longitude), place_lat, place_lng)

            results.append({
                "name": place.get("name"),
                "address": address,
                # "address": place.get("formatted_address") or place.get("vicinity"),
                "rating": place.get("rating", "N/A"),
                "distance": distance,
                "lat": place_lat,    
                "lng": place_lng
                # "raw": place
            })
        results.sort(key=lambda x: x["distance"])
    except Exception as e:
                print(e)
                results = []

    return render_template(
        "results.html",
        query=query,
        results=results
    )

# @app.route("/location")
# def location():
#     lat = request.args.get("lat")
#     lng = request.args.get("lng")

#     url = (
#         "https://maps.googleapis.com/maps/api/geocode/json"
#         f"?latlng={lat},{lng}"
#         f"&key={API_KEY}"
#     )

#     response = requests.get(url)
#     data = response.json()

#     if data["results"]:
#         address = data["results"][0]["formatted_address"]
#     else:
#         address = "Location not found"

#     return {"address": address}

@app.route("/business-search")
def business_search():

    query = request.args.get(
        "query",
        ""
    ).strip()

    latitude = request.args.get(
        "latitude",
        type=float
    )

    longitude = request.args.get(
        "longitude",
        type=float
    )

    if latitude is None or longitude is None:
        return render_template(
            "business_results.html",
            businesses=[],
            query=query,
            error=(
                "Location access is required to find "
                "businesses near you."
            )
        )

    keywords = query.split()
    conditions = []

    for keyword in keywords:

        search_term = f"%{keyword}%"

        conditions.extend([
            Business.business_name.ilike
            (
                search_term
            ),
            Business.category.ilike(
                search_term
            ),
            Business.subcategory.ilike(
                search_term
            ),
            Business.description.ilike(
                search_term
            ),
            Business.address.ilike(
                search_term
            ),
            cast(
                Business.id,
                String
            ).ilike(search_term),
                    ])

    # Do not apply the old latitude +/- 0.5 and
    # longitude +/- 0.5 restriction here.
    #
    # That restriction prevented Premium businesses
    # within 300 km and distant Featured businesses
    # from reaching the distance visibility check.
    business_query = Business.query.filter(
        Business.status == "approved",
        Business.latitude.isnot(None),
        Business.longitude.isnot(None)
    )

    if conditions:
        business_query = business_query.filter(
            or_(*conditions)
        )

    matching_businesses = (
        business_query.all()
    )

    businesses = []

    for business in matching_businesses:

        distance = calculate_distance(
            latitude,
            longitude,
            business.latitude,
            business.longitude
        )

        business.featured_active = (
            has_active_featured_listing(
                business
            )
        )

        business.premium_active = (
            has_active_premium(
                business
            )
        )

        business.verified_active = (
            is_verified_business(
                business
            )
        )

        if not is_business_visible_by_distance(
            business,
            distance
        ):
            continue

        business.distance = distance

        businesses.append(
            business
        )

    # Sorting priority:
    #
    # 1. Featured
    # 2. Featured position
    # 3. Premium
    # 4. Distance
    businesses.sort(
        key=lambda business: (
            0
            if business.featured_active
            else 1,

            business.featured_position
            if business.featured_active
            and business.featured_position
            is not None
            else 999999,

            0
            if business.premium_active
            else 1,

            business.distance
        )
    )

    return render_template(
        "business_results.html",
        businesses=businesses,
        query=query
    )
# @app.route(
#     "/business-view/<int:business_id>",
#     methods=["POST"]
# )

@app.route(
    "/business-click/<int:business_id>/<string:action>",
    methods=["POST"]
)
def record_business_click(
    business_id,
    action
):

    business = Business.query.get_or_404(
        business_id
    )

    if action == "phone":
        business.phone_clicks = (
            business.phone_clicks or 0
        ) + 1

    elif action == "whatsapp":
        business.whatsapp_clicks = (
            business.whatsapp_clicks or 0
        ) + 1

    elif action == "website":
        business.website_clicks = (
            business.website_clicks or 0
        ) + 1

    else:
        return jsonify({
            "status": "error"
        }), 400

    db.session.commit()

    return jsonify({
        "status": "success"
    })

@app.route(
    "/business-click/<int:business_id>/<string:action>"
)
def track_business_click(
    business_id,
    action
):

    business = db.session.get(
        Business,
        business_id
    )

    if not business:
        return "Business not found.", 404

    if business.status != "approved":
        return "Business is not available.", 404

    action = (
        action or ""
    ).strip().lower()

    redirect_url = None

    if action == "phone":

        if not business.phone or not business.show_phone:
            return "Phone number is not available.", 404

        business.phone_clicks = (
            business.phone_clicks or 0
        ) + 1

        clean_phone = (
            str(business.phone)
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        redirect_url = f"tel:{clean_phone}"

    elif action == "whatsapp":

        if (
            not business.whatsapp
            or not business.show_whatsapp
        ):
            return "WhatsApp is not available.", 404

        business.whatsapp_clicks = (
            business.whatsapp_clicks or 0
        ) + 1

        clean_whatsapp = (
            str(business.whatsapp)
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if clean_whatsapp.startswith("0"):
            clean_whatsapp = (
                "27" + clean_whatsapp[1:]
            )

        elif clean_whatsapp.startswith("+"):
            clean_whatsapp = clean_whatsapp[1:]

        redirect_url = (
            f"https://wa.me/{clean_whatsapp}"
        )

    elif action == "website":

        if not business.website:
            return "Website is not available.", 404

        business.website_clicks = (
            business.website_clicks or 0
        ) + 1

        redirect_url = business.website

    else:

        return "Invalid click action.", 400

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        app.logger.exception(
            "Unable to track %s click for business ID %s",
            action,
            business.id
        )

        # Do not block the customer's action merely because
        # analytics could not be saved.

    return redirect(
        redirect_url,
        code=302
    )

@app.route("/business-view/<int:business_id>", methods=["POST"])
def count_business_view(business_id):

    business = Business.query.get_or_404(business_id)

    business.views += 1
    business.last_viewed = datetime.utcnow()

    db.session.commit()

    return {"success": True}, 200

def get_premium_category_counts():

    normalized_category = func.coalesce(
        func.nullif(
            func.trim(Business.category),
            ""
        ),
        "Other"
    )

    results = (
        db.session.query(
            normalized_category.label("category"),
            func.count(Business.id).label("business_count")
        )
        .filter(
            Business.status == "approved",
            Business.is_premium.is_(True),
            or_(
                Business.premium_expires_at.is_(None),
                Business.premium_expires_at > utc_now()
            )
        )
        .group_by(normalized_category)
        .order_by(
            func.count(Business.id).desc(),
            normalized_category.asc()
        )
        .all()
    )

    return [
        {
            "category": row.category,
            "count": row.business_count
        }
        for row in results
    ]

def get_coordinates(address):

    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={address}"
        f"&key={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["results"]:

        location = (
            data["results"][0]
            ["geometry"]
            ["location"]
        )

        return (
            location["lat"],
            location["lng"]
        )

    return None, None

@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("terms_and_conditions.html")


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/refund-policy")
def refund_policy():
    return render_template("refund_policy.html")


@app.route("/location")
def location():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={lat},{lng}"
        f"&key={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["results"]:
            address = data["results"][0]["formatted_address"]
        else:
            address = "Location not found"

        return {"address": address}
    except requests.exceptions.Timeout:
        return {"address": "Location lookup timeout"}, 504
    
    except Exception as e:
        return {"address": str(e)}, 500

@app.route("/health")
def health():
   return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
