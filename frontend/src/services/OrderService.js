import http from "../helpers/http-common";

class OrderService {
  getAll(user_id = null) {
    const path = "/orders";
    var params = {}
    if (user_id != null) {
      params['user_id'] = user_id
    } 
    
    return http.get(path, {params: params});
  }

  create(data) {
    return http.post("/order", data);
  }

  setStatus(id, status) {
    return http.put("/order/history", {'order_id': id, 'status': status});
  }

  blockUser(id) {
    return http.post("/order/ban", {'user_id': id});
  }

  delete(id) {
    return http.delete(`/order/${id}`);
  }
}

export default new OrderService();