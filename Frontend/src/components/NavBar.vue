<template>
    <v-app-bar class="container" :elevation="2">
        <template v-slot:prepend>
            <v-app-bar-nav-icon @click="shift" class="shifticon"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title>NeuroFlow</v-app-bar-title>

        <v-spacer></v-spacer>

        <v-menu>
            <template v-slot:activator="{ props }">
                <v-btn icon="mdi-account" v-bind="props"></v-btn>
            </template>

            <v-list class="list">
                <v-btn :prepend-icon="item.icon" @click="item.onClick" v-for="(item, i) in items2" :key="i"
                    class="button" variant="text">{{
                        item.title }}
                </v-btn>
            </v-list>
        </v-menu>

        <v-menu>
            <template v-slot:activator="{ props }">
                <v-btn icon="mdi-dots-vertical" v-bind="props"></v-btn>
            </template>

            <v-list class="list">
                <v-btn :prepend-icon="item.icon" @click="item.onClick" v-for="(item, i) in items" :key="i"
                    class="button" variant="text">{{
                        item.title }}
                </v-btn>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>

<script setup>
import { defineEmits, defineProps } from "vue";
import router from "../router";
import { setToken, setUID } from "../main";

const emit = defineEmits(["trigger"]);
const props = defineProps({ setPage: Function });

function shift() {
    emit("trigger");
}

const items = [
    { title: "Dashboard", onClick: () => props.setPage(0), icon: "mdi-view-dashboard" },
    { title: "My Boards", onClick: () => props.setPage(2), icon: "mdi-notebook" },
    { title: "Create Board", onClick: () => props.setPage(3), icon: "mdi-gesture" },
];

const items2 = [
    { title: "Profile", onClick: () => props.setPage(1), icon: "mdi-account" },
    {
        title: "Sign Out", onClick: () => {
            setToken("");
            setUID("");
            router.push("/login");
        }, icon: "mdi-logout",
    },
];

const signOut = () => {
    setToken("");
    setUID("");
    router.push("/login");
}
</script>

<style scoped>
.container {
    background-color: var(--primary-dark) !important;
    color: white !important;
    box-shadow: none !important;
    border: none !important;
}

.list {
    display: flex;
    flex-direction: column;
}

.button {
    height: 50px !important;
    border-radius: 0%;
    text-transform: none;
    font-weight: 400;
    font-size: 18px;
    letter-spacing: 0px;
    justify-content: start;
    width: 220px !important;
    gap: 10px;
}

@media screen and (max-width: 600px) {
    .shifticon {
        display: none;
    }

}
</style>