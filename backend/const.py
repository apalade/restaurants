from enum import Enum


class OrderStatusValues(str, Enum):
    PLACED = "Placed"
    CANCELLED = "Cancelled"
    PROCESSING = "Processing"
    IN_ROUTE = "In route"
    DELIVERED = "Delivered"
    RECEIVED = "Received"


ORDER_STATUS_VALUES_NEXT = {
    'owner': {
        OrderStatusValues.PLACED: OrderStatusValues.PROCESSING,
        OrderStatusValues.PROCESSING: OrderStatusValues.IN_ROUTE,
        OrderStatusValues.IN_ROUTE: OrderStatusValues.DELIVERED,
    },
    'user': {
        OrderStatusValues.PLACED: OrderStatusValues.CANCELLED,
        OrderStatusValues.DELIVERED: OrderStatusValues.RECEIVED,
    }
}
