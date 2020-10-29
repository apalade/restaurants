<template>
  <div class="card mt-5">
    <img class="card-img-top" :src="img" alt="" />
    <div class="card-body">
      <div v-show="!edit">
        <h5 class="card-title">{{ meal.name }}</h5>
        <div>{{ meal.description }}</div>

        <a v-if="!owner" class="btn btn-primary" @click="add(meal)">Order now</a
        ><br />
        <div class="small">
          only <strong>${{ meal.price | printNumber }}</strong> from
          <strong>{{ meal.restaurant.name }}</strong>
        </div>
      </div>

      <input type="text" v-show="edit" v-model="m.name" />
      <input type="text" v-show="edit" v-model="m.description" />
      <input type="text" v-show="edit" v-model="m.price" />
      <select
        v-show="edit"
        v-model="rid"
        class="form-control"
        id="id"
        name="id"
      >
        <option
          v-for="(el, idx) in restaurants"
          v-bind:key="idx"
          v-bind:value="el.id"
          :selected="el.id == rid"
          >{{ el.name }}</option
        >
      </select>
    </div>

    <div v-if="owner">
      <a class="btn btn-success m-1" v-if="edit" @click="saveEdit">Save</a>
      <a class="btn btn-warning m-1" v-if="!edit" @click="editMeal">Edit</a>
      <a class="btn btn-danger m-1" v-if="!edit" @click="deleteMeal">Delete</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "MealSingle",
  props: ["id", "img", "owner", "meal", "restaurant_id", "restaurants"],
  data() {
    return {
      message: "",
      edit: false,
      m: this.meal,
      rid: this.restaurant_id,
    };
  },
  methods: {
    add(selected_meal) {
      const meals = this.$store.getters["cart/meals"];
      if (
        meals.findIndex(
          (el) => el.restaurant.id != selected_meal.restaurant.id
        ) > -1
      ) {
        this.$store.dispatch("msg/set", {
          msg: "Please order from only one restaurant at a time.",
          type: "error",
        });
        return;
      }

      this.$store.dispatch("cart/add", this.m);
    },

    editMeal() {
      this.edit = true;
    },
    deleteMeal() {
      this.$emit("deleteme");
    },
    saveEdit: function() {
      this.edit = !this.edit;
      if (!this.edit) {
        this.$emit("editme", { meal: this.m, restaurant_id: this.rid });
      }
    },
  },
  watch: {
    meal(val) {
      this.m = val;
    },
    restaurant_id(val) {
      this.rid = val;
    },
  },
};
</script>

<style></style>
