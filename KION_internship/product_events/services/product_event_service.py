from product_events.models import ProductEvent


def _create_product_event(product_event_data: dict) -> object:
    """
    Creates a unique instance of a product event.
    """
    return ProductEvent.objects.create(event_data=product_event_data)
