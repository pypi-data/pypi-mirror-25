from enum import Enum


class SaleType(Enum):
    HOUSES = '/houses-for-sale/'
    PROPERTIES = '/property-for-sale/'
    AUCTION = '/houses-for-auction/'
    APARTMENTS = '/apartments-for-sale/'
    COMMERCIAL = '/commercial-property/'
    NEW = '/new-homes-for-sale/'
    OVERSEAS = '/overseas-property-for-sale/'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<SaleType: %s>" % self


class CommercialType(Enum):
    OFFICE = '/offices/'
    RETAIL = '/retail-units/'
    OFFICE_SHARE = '/office-share/'
    INDUSTRIAL_UNIT = '/industrial-unit/'
    COMMERCIAL_SITE = '/commercial-site/'
    AGRICULTURAL_LAND = '/agricultural-farm-land/'
    RESTAURANT_BAR_HOTEL = '/restaurant-hotel-bar/'
    INDUSTRIAL_SITE = '/industrial_site/'
    DEV_LAND = '/development-land/'
    INVESTMENT_PROPERTY = '/investment-property/'
    SERVICED_OFFICE = '/serviced-office/'
    OVERSEAS = '/overseas-commercial-property-for-sale/'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<CommercialType: %s>" % self


class RentType(Enum):
    HOUSES = '/houses-for-rent/'
    APARTMENTS = '/apartments-for-rent/'
    ANY = '/residential-property-for-rent/'
    STUDIO = '/studio-apartments-for-rent/'
    FLAT = '/flats-for-rent/'
    SHORT_TERM = '/short-term-rentals/'
    STUDENT_ACCOMMODATION = '/student-accommodation/'
    PARKING_SPACES = '/parking-spaces/'
    ROOMS_TO_SHARE = '/rooms-to-share/'
    FLAT_TO_SHARE = '/flat-to-share/'
    APARTMENT_TO_SHARE = '/apartment-share/'
    HOUSE_SHARE = '/house-share/'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<RentType: %s>" % self


class StudentAccommodationType(Enum):
    ROOMS_TO_SHARE = '/rooms-to-share/'
    APARTMENTS = '/apartments-for-rent/'
    ANY = '/residential-property-for-rent/'
    STUDIO = '/studio-apartments-for-rent/'
    FLAT = '/flats-for-rent/'
    SHORT_TERM = '/short-term-rentals/'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<StudentAccommodationType: %s>" % self


class RoomType(Enum):
    SINGLE = 'single'
    DOUBLE = 'double'
    TWIN_ROOM = 'twin'
    SHARED = 'shared'
    SINGLE_OR_DOUBLE = 'own'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<RoomType: %s>" % self


class QueryParam(Enum):
    SALE_AGREED = '&s[area_type]=on&s[agreed]=1&s[advanced]=1'
    SALE_AGREED_WITH_PRICE = '&s%5Bagreed%5D=1&s%5Badvanced%5D=1'
    MIN_PRICE = '&s%5Bmnp%5D='
    MAX_PRICE = '&s%5Bmxp%5D='
    IGNORED_AGENTS = '&s%5Bignored_agents%5D%5B1%5D'
    MIN_BEDS = '&s%5Bmnb%5D='
    MAX_BEDS = '&s%5Bmxb%5D='
    SORT_BY = '&s%5Bsort_by%5D='
    SORT_ORDER = '&s%5Bsort_type%5D='
    COMMERCIAL_MIN = '&s%5Bmin_size%5D='
    COMMERCIAL_MAX = '&s%5Bmax_size%5D='
    OPEN_VIEWING = '&s%5Bopenviewing%5D=1'
    WITH_PHOTOS = '&s%5Bphotos%5D=1'
    KEYWORDS = '&s%5Btxt%5D='
    FURNISHED = '&s%5Bfurn%5D=1'
    COUPLES_ACCEPTED = '&couples=1'
    ENSUITE_ONLY = '&s%5Bes%5D=1'
    ROOM_TYPE = '&s%5Broom_type%5D='
    GENDER = '&gender='

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<QueryParam: %s>" % self


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    EITHER = 'on'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<Gender: %s>" % self


class SortOrder(Enum):
    ASCENDING = 'a'
    DESCENDING = 'd'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<SortOrder: %s>" % self


class SortType(Enum):
    DATE = 'date'
    DISTANCE = 'distance'
    PRICE = 'price'
    UPCOMING_VIEWING = 'upcoming_viewing'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<SortType: %s>" % self


class University(Enum):
    NCI = 'national-college-of-ireland-nci'
    UCD = 'university-college-dublin-nui'
    GCD = 'griffith-college-dublin'
    TCD = 'trinity-college-university-of-dublin'
    DCU = 'dublin-city-university'

    def __str__(self):
        return self._value_

    def __repr__(self):
        return "<University: %s>" % self
