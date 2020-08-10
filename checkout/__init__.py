# We need to tell django the name of the default config class for the app in order to ensure our signals are working
# This class come from apps.py where we imported our signals module

default_app_config = 'checkout.apps.CheckoutConfig'