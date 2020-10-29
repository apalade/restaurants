import http from "../helpers/http-common";

class AuthService {
  login(data) {
    const path = '/auth/login'
    return http.post(path, data);
  }

  register(data) {
    const path = '/auth/register'
    return http.post(path, data);
  }

  blockUser(data) {
    const path = '/auth/block'
    return http.post(path, data);
  }
}

export default new AuthService();
