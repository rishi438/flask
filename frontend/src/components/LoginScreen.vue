<template>
  <v-app id="login_screen">
    <v-container class="login-card" fluid>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="#3f3f3f">
              <v-toolbar-title class="text-wiz-ffffff" >{{ login_type }} Login</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field prepend-icon="mdi-account" name="login" label="Login" type="text"></v-text-field>
                <v-text-field id="password" prepend-icon="mdi-lock" name="password" label="Password"
                  type="password"></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions class="d-flex justify-end pr-4">
              <v-btn color="primary" to="/">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<style scoped>
.login-card {
  display: contents;
}
</style>

<script>
export default {
  name: 'Main-Login',
  props: {
    source: String,
    login_type: String
  },
};
</script>
