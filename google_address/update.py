import threading
import pprint

from google_address.api import GoogleAddressApi
from google_address.models import Address, AddressComponent


def update_address(instance):
    response = GoogleAddressApi().query(instance.raw)

    if len(response["results"]) > 0:
        result = response["results"][0]
    else:
        return False

    instance.address_components.clear()
    for api_component in result["address_components"]:
        component = AddressComponent.get_or_create_component(api_component)
        instance.address_components.add(component)

    # Using update to avoid post_save signal. insert update_params in update_kwargs
    update_kwargs = {}
    try:
        if result["geometry"]:
            update_kwargs['lat'] = result["geometry"]["location"]["lat"]
            update_kwargs['lng'] = result["geometry"]["location"]["lng"]

    except:  # pragma: no cover
        pass

    address_line = instance.get_address()
    if address_line != instance.address_line:
        update_kwargs['address_line'] = instance.get_address()

    city_state = instance.get_city_state()
    if city_state != instance.city_state:
        update_kwargs['city_state'] = instance.get_city_state()

    if update_kwargs:
        Address.objects.filter(pk=instance.pk).update(**update_kwargs)



class UpdateThread(threading.Thread):
    def __init__(self, instance):
        self.instance = instance
        threading.Thread.__init__(self)

    def run(self):
        return update_address(self.instance)
