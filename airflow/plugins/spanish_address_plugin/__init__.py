from airflow.plugins_manager import AirflowPlugin
from spanish_address_plugin.operators.address_source_list import AddressSourceListOperator


class SpanishAddressPlugin(AirflowPlugin):
    name = "SpanishAddressPlugin"
    operators = [AddressSourceListOperator]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []