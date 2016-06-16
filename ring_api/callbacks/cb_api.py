# This file is the python callbacks API.
# It is written to help the user to identify the python callbacks to register.

# Function names should be the same as the keys from callbacks_to_register().
# Each method should contain a docstring that describes it.

def text_message(account_id, from_ring_id, content):
    """Receives a text message

    Keyword arguments:
    account_id      -- account id string
    from_ring_id    -- ring id string
    content         -- dict of content defined as [<mime-type>, <message>]
    """
    pass

