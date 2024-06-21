<template>
</template>

<script setup>
import router from '../router';
import { TOKEN, UID } from '../main';

if (!TOKEN || !UID) {
    router.push("/welcome");
}
else if (TOKEN === "" || UID === "") {
    router.push("/welcome");
}
else {
    router.push("/panel");
}
</script>
