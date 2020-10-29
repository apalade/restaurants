<template>
  <div class="card mt-5">
    <img class="card-img-top" :src="img" alt="" />
    <div class="card-body">
      <span v-show="!edit" @click="editRestaurant">
        <h5 class="card-title">{{ name }}</h5>
        <div>{{ description }}</div>
      </span>

      <input type="text" v-show="edit" v-model="n" />
      <input type="text" v-show="edit" v-model="d" />
      <br />
    </div>

    <div v-if="owner">
        <a class="btn btn-primary m-1" v-if="edit" @click="saveEdit">Save</a>
        <a class="btn btn-warning m-1" v-if="!edit" @click="editRestaurant">Edit</a>
        <a class="btn btn-danger m-1" v-if="!edit" @click="deleteRestaurant">Delete</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "RestaurantSingle",
  props: ["id", "img", "owner", "name", "description"],
  data() {
    return {
      message: "",
      edit: false,
      n: this.name,
      d: this.description,
    };
  },
  methods: {
    editRestaurant() {
      this.edit = true;
    },
    deleteRestaurant() {
      this.$emit('deleteme');
    },
    saveEdit: function() {
      this.edit = !this.edit;
      if (!this.edit) {
        this.$emit("editme", {
          id: this.id,
          name: this.n,
          description: this.d,
          owner_id: this.$store.getters["auth/user"].id
        });
      }
    },
  },
  watch: {
    name(val) {
      this.n = val;
    },
    description(val) {
      this.d = val;
    },
  },
};
</script>

<style></style>
