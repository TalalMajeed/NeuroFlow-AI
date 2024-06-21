<template>
    <v-btn-toggle v-model="activeIndex" mandatory shaped class="left-bar">
        <v-btn variant="text" v-for="(item, i) in items" :key="i" color="teal-darken-3" class="bar-item"
            :prepend-icon="item.icon">
            {{ item.title }}
        </v-btn>
    </v-btn-toggle>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps } from 'vue';

const emit = defineEmits(["trigger"]);

const props = defineProps({
    page: Number
});

const items = ref([
    { title: 'Dashboard', icon: 'mdi-view-dashboard' },
    { title: 'User Profile', icon: 'mdi-account' },
    { title: 'My Boards', icon: 'mdi-notebook' },
    { title: 'Create Board', icon: 'mdi-gesture' },
]);

const activeIndex = ref(0);
watch(activeIndex, (newValue, oldValue) => {
    emit("trigger", newValue);
});

watch(() => props.page, (newValue, oldValue) => {
    activeIndex.value = newValue;
});
</script>

<style scoped>
.left-bar {
    height: 100%;
    padding-top: 0;
    display: flex;
    flex-direction: column;
    border-radius: 0%;
}

.bar-item {
    height: 60px !important;
    justify-content: start;
    padding-left: 27px;
    font-weight: 400;
    font-size: 16px;
    text-transform: none;
    gap: 20px;
    color: var(--secondary-light);
}
</style>
