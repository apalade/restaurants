<template>
  <div>
    <h2>My Restaurants
       <router-link class="btn btn-primary small" :to="{ name: 'restaurant-add' }"
          >Add
        </router-link>
    </h2>

    <div class="container">
      <div class="row">
        <div v-for="(el, idx) in restaurants" v-bind:key="idx" class="col-lg-3">
          <RestaurantSingle
            :id="el.id"
            :img="img_link"
            :owner="true"
            :name="el.name"
            :description="el.description"
            v-on:deleteme="deleteRestaurant(idx)"
            v-on:editme="(data) => editRestaurant(idx, data)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RestaurantSingle from "@/components/restaurant/Single.vue";
import RestaurantService from "@/services/RestaurantService";
import getErrMsg from "@/helpers"

export default {
  name: "RestaurantMine",
  components: {
    RestaurantSingle,
  },
  data() {
    return {
      user: this.$store.getters["auth/user"],
      img_link: "https://picsum.photos/400/200",
      restaurants: []
    };
  },
  methods: {
    getRestaurants(id) {
      RestaurantService.getAll(id)
        .then((response) => {
          this.restaurants = response.data;
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {msg: getErrMsg(error), type: 'error'})
        });
    },
    editRestaurant(idx, data) {
      RestaurantService.update(data)
        .then((resp) => {
          this.$set(this.restaurants, idx, resp.data)
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {msg: getErrMsg(error), type: 'error'})
        });
    },
    deleteRestaurant(idx) {
      RestaurantService.delete(this.restaurants[idx].id)
        .then(() => {
          this.restaurants.splice(idx, 1);
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {msg: getErrMsg(error), type: 'error'})
        });
    },
  },
  mounted() {
    this.getRestaurants(this.user.id);
  },
};
</script>

<style>
body {
  background-color: #f4f4f4;
}
</style>
