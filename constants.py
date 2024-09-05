# Regular expression for phone number validation
PHONE_REGEX = r"^(\+\d{1,3} )?(((\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4})|(\d{5} \d{5})|\d{6,15})(, ?\d{1,4})?$"