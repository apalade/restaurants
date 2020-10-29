import http from "../helpers/http-common";

class RestaurantService {
  getAll(owner_id = null) {
    const path = "/restaurants";
    var params = {}
    if (owner_id != null) {
      params.owner_id = owner_id
    }

    return http.get(path, {params: params});
  }

  create(data) {
    return http.post("/restaurant", data);
  }

  update(data) {
    return http.put("/restaurant", data);
  }

  delete(id) {
    return http.delete("/restaurant", {params: {rid: id}});
  }
}

export default new RestaurantService();