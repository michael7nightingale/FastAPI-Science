<script>
export default {
  name: "FooterItem",
  data() {
    return {
      author: "michael7nightingale",
      authorGitHubUrl: "https://github.com/michael7nightingale",

    }
  },
  computed: {
    year() {
      let now = new Date();
      return now.getFullYear();
    }
  },

  methods: {
    openAuthorGitHubUrl() {
      window.open(this.authorGitHubUrl, "_blank");
    }
  }
}
</script>

<template>
  <footer class="border-top footer text-muted text-center">
    <div class="p-2">
      <p class="">© {{ year }}, Все права защищены. Создан <a href="#" @click="openAuthorGitHubUrl">{{ author }}</a></p>
    </div>
  </footer>
</template>

<style>

</style>