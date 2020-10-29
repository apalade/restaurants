<template>
  <div>
    <div class="container m-5 p-5">
      <div v-for="(meals, rid, ridx) in meals_by_restaurant" :key="ridx">
        <h3 class="mb-0">{{ meals[0].restaurant.name }}</h3>
        <div class="row">
          <div v-for="(el, idx) in meals" :key="idx" class="col-lg-3">
            <MealSingle :id="el.id" :img="el.img" :meal="el" />
          </div>
        </div>
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
import MealSingle from "@/components/meal/Single.vue";
import MealService from "@/services/MealService";
import getErrMsg from "../helpers";

export default {
  name: "Homepage",
  components: {
    MealSingle,
  },
  data() {
    return {
      user: this.$store.getters["auth/user"],
      meals_by_restaurant: {},
    };
  },
  methods: {
    getMeals() {
      MealService.getAll()
        .then((response) => {
          this.meals_by_restaurant = response.data.reduce(function(r, meal) {
            r[meal.restaurant.id] = r[meal.restaurant.id] || [];
            r[meal.restaurant.id].push(meal);
            return r;
          }, Object.create(null));
        })
        .catch((error) => {
          this.$store.dispatch[
            ("msg/set", { msg: getErrMsg(error), type: "error" })
          ];
        });
    },
  },
  mounted() {
    this.getMeals();
  },
};
</script>

<style>
body {
  background-color: #f4f4f4;
}
</style>
