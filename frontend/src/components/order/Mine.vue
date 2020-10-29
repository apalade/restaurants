<template>
  <div>
    <div class="container pt-5">
      <div v-if="orders.length < 1" class="alert alert-info">You have no orders yet.</div>
      <div v-for="(el, idx) in orders" v-bind:key="idx" class="row">
        <div class="col-2">
          <h3>Order #{{ el.id}}</h3>
          <div class="small">total: <strong>${{ el.total | printNumber }}</strong></div>
          <div class="small"> for <strong>{{ el.restaurant.name }} </strong></div>
          <div class="small" v-show="user.is_owner">
            from <strong>{{ el.user.email }}</strong>
            <a v-show="!el.user.is_owner" class="btn btn-danger btn-small" @click="blockUser(el.user.id)">ban</a>
          </div>
        </div>

        <div class="col">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Price</th>
                <th scope="col">Quantity</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(l, idxl) in el.lines" v-bind:key="'l' + idxl">
                <th scope="row">{{ idxl + 1 }}</th>

                <td>{{ l.meal.name }}</td>
                <td>${{ l.meal.price | printNumber }}</td>
                <td>{{ l.quantity }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="col-2">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Status</th>
                <th scope="col">Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(h, idxh) in el.history" v-bind:key="'h' + idxh">
                <td>{{ h.status }}</td>
                <td>{{ h.updated_on | printDate }}</td>
              </tr>
              <tr>
                <a
                  v-show="canChangeStatus(idx)"
                  class="btn btn-link"
                  @click="changeStatus(idx)"
                  >Mark as {{ peekStatus(idx) }}</a
                >
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import OrderService from "@/services/OrderService";
import { OrderStatusUserNext, OrderStatusOwnerNext } from "@/config";
import getErrMsg from '../../helpers';

export default {
  name: "OrderMine",

  data() {
    return {
      user: this.$store.getters["auth/user"],
      orders: [],
      message: ""
    };
  },
  computed: {
    peekStatus() {
      return (idx) =>
        this.user.is_owner
          ? OrderStatusOwnerNext[this.status(idx)]
          : OrderStatusUserNext[this.status(idx)];
    },
    canChangeStatus() {
      return (idx) => this.peekStatus(idx) !== undefined;
    },
    status() {
      return (idx) =>
        [...this.orders[idx].history]
          .sort((h1, h2) => h1.updated_on.localeCompare(h2.updated_on))
          .slice(-1)[0].status;
    },
  },
  methods: {
    getOrders() {
      OrderService.getAll(this.user.id)
        .then((response) => {
          this.orders = response.data;
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {msg: getErrMsg(error), type: 'error'})
        });
    },
    changeStatus(idx) {
      const next = this.peekStatus(idx);
      OrderService.setStatus(this.orders[idx].id, next)
        .then((response) => {
          this.$set(this.orders, idx, response.data);
        })
        .catch(() => {
          this.getOrders()
          this.$store.dispatch("msg/set", {msg: "New status update for the order in place.", type: 'error'})
        });
    },
    blockUser(id) {
      OrderService.blockUser(id)
        .then(() => {
          this.$store.dispatch("msg/set", {msg: "User has been banned.", type: 'success'})
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {msg: getErrMsg(error), type: 'error'})
        });
    },
  },
  mounted() {
    this.getOrders();
  },
};
</script>

<style>
body {
  background-color: #f4f4f4;
}
</style>
