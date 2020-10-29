<template>

  <div v-if="message" id="global-message" class="fixed-top alert bring-in-front" :class="type == 'success' ? 'alert-primary' : 'alert-danger'" role="alert">
    {{ message }}
  </div>
</template>

<script>
export default {
  computed: {
    message() {
        return this.$store.getters["msg/msg"]
    },
    type() {
        return this.$store.getters["msg/type"]
    }
  },
};
</script>
<style scoped>
.bring-in-front {
    z-index: 1001
}
</style>
