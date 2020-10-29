export const OrderStatus = Object.freeze({
    PLACED: "Placed",
    CANCELED: "Cancelled",
    PROCESSING: "Processing",
    IN_ROUTE: "In route",
    DELIVERED: "Delivered",
    RECEIVED: "Received"

});

export const OrderStatusUserNext = Object.freeze({
  [OrderStatus.PLACED]: OrderStatus.CANCELED,
  [OrderStatus.DELIVERED]: OrderStatus.RECEIVED
});

export const OrderStatusOwnerNext = Object.freeze({
    [OrderStatus.PLACED]: OrderStatus.PROCESSING,
    [OrderStatus.PROCESSING]: OrderStatus.IN_ROUTE,
    [OrderStatus.IN_ROUTE]: OrderStatus.DELIVERED,
  });
  