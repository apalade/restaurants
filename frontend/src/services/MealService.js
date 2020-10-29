import http from "../helpers/http-common";

class MealService {
  getAll(owner_id = null) {
    const path = "/meals";
    var params = {}
    if (owner_id != null) {
      params.owner_id = owner_id
    }

    return http.get(path, {params: params});
  }

  create(data) {
    return http.post("/meal", data);
  }

  update(data) {
    return http.put("/meal", data);
  }

  delete(id) {
    return http.delete("/meal", {params: {mid: id}});
  }
}

export default new MealService();