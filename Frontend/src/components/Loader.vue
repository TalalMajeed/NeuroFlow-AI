<template>
    <div class="container">
        <img :width=100 :height=100 src="@/assets/logo.png"></img>
        <div class="progress">
            <v-progress-linear height="6" class="progress" color="teal" indeterminate></v-progress-linear>
        </div>
    </div>

</template>

<script setup></script>

<style scoped>
img {
    user-select: none;
}

.progress {
    width: 150px;
    margin-top: 0px;
}

.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100svw;
    height: 100svh;
    gap: 40px;
    margin-top: -40px;
}
</style>