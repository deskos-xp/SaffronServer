import enum


class messages(enum.Enum):
    NO_JSON="json required not provided",400
    NO_ID="missing required id",400
    NO_WHO_ID="missing id for WHO",400
    NO_ADDRESS_ID="missing required ADDRESS_ID",400
    NO_LEDGER_ID="missing required LEDGER_ID",400
    NO_PRODUCT_COUNT_ID="missing required PRODUCT_COUNT_ID",400
    NO_PRODUCT_ID="missing required PRODUCT_COUNT_ID",400
    NO_VENDOR_ID="missing vendor_id required",400
    NO_BRAND_ID="missing brand_id required",400
    NO_MANUFACTURER_ID="missing manufacturer_id required",400
    NO_DEPARTMENT_ID="missing department_id required",400
    NO_ROLE_ID="missing role_id required",400

    NO_TYPE_FOR_EXPORT="missing TYPE for export",400

    ENTITY_DOES_NOT_EXIST="entity provided by id does not exist",400
    
    ENTITY_DOES_NOT_EXIST_PRODUCT="product provided by id does not exist",400
    ENTITY_DOES_NOT_EXIST_PRODUCT_COUNT="productCount provided by id does not exist",400
    ENTITY_DOES_NOT_EXIST_MANUFACTURER="manufacturer provided by id does not exist",400
    #ENTITY_DOES_NOT_EXIST_PRODUCT="product provided by id does not exist",400
    ENTITY_DOES_NOT_EXIST_BRAND="brand entity does not exist",400
    ENTITY_DOES_NOT_EXIST_ADDRESS="address entity does not exist",400
    ENTITY_DOES_NOT_EXIST_USER="user entity does not exist",400
    ENTITY_DOES_NOT_EXIST_VENDOR="vendor entity does not exist",400
    ENTITY_DOES_NOT_EXIST_DEPARTMENT="department entity does not exist",400
    ENTITY_DOES_NOT_EXIST_ROLE="role entity does not exist",400

    ENTITY_NOT_RELATED="entity not related",400

    FMT_NOT_PROVIDED="no FMT provided!",400
    TO_FORMAT_NOT_PROVIDED="missing the TO field of the uri",400
    PHONE_EMPTY="missing phone number",400
    EMAIL_EMPTY="missing email address",400
    WHAT_EMPTY="object WHAT is None!",400

    INVALID_KEY_MANUFACTURER="invalid key provided manufacturer",400
    INVALID_KEY_VENDOR="invalid key provided vendor",400
    INVALID_KEY_ADDRESS="invalid key provided address",400
    INVALID_KEY_BRAND="invalid key provided brand",400

    INVALID_UPC_LEN="invalid length for upc",400
    NO_WHICH_PROVIDED="which not provided",400
    NOT_ADMIN="not an admin",400
