<template>
    <div v-show="auth">
        <NavBar @trigger="setOpenMenu" :setPage="setPage" />
        <Loader v-show="!user" />
        <div class="main" v-if="user">
            <div class="left" :style="shiftWidth()">
                <LeftBar @trigger="setPage" :page="page" />
            </div>
            <div class="center">
                <Dashboard v-show="page == 0" :user="user" :setPage="setPage" :page="page" @trigger="setBoard" />
                <UserProfile v-show="page == 1" :user="user" :page="page" />
                <MyBoards v-show="page == 2" :user="user" :page="page" @trigger="setBoard" :setPage="setPage" />
                <CreateBoards v-show="page == 3" :user="user" :open="openMenu" :board="board" :setPage="setPage" />
            </div>
        </div>
    </div>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue";
import { TOKEN, API, UID, setToken, setUID } from "../main";
import router from '../router';
import { ref } from 'vue';
import MyBoards from "@/components/MyBoards.vue";

const user = ref(null);
const auth = ref(true);
const openMenu = ref(true);
const page = ref(0);
const board = ref(null);

const setBoard = (b) => {
    board.value = [b, new Date().getTime()];
}

const setPage = (p) => {
    page.value = p;
    console.log(page.value);
}


const setOpenMenu = () => {
    openMenu.value = !openMenu.value;
}

const shiftWidth = () => {
    return {
        width: openMenu.value ? "70px" : "250px",
        minWidth: openMenu.value ? "70px" : "250px",
    }
}

if (!TOKEN || !UID) {
    router.push("/login");
}
if (TOKEN === "" || UID === "") {
    router.push("/login");
}

const RenewToken = async () => {
    try {
        console.log("Renewing Token")
        const response = await fetch(`${API}/renew`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                "uid": UID
            })
        });

        const data = await response.json();
        if (data["status"] === 200) {
            if (data['status'] == '200') {
                let temp = JSON.parse(data['data'])
                setToken(temp['token']);
                setUID(temp['uid']);
                router.push("/panel");
                console.log("Token Renewed")
            }
        }
        else {
            throw new Error("Token Renewal Failed");
        }
    }
    catch (e) {
        console.log(e);
        localStorage.setItem("TOKEN", "");
        localStorage.setItem("UID", "");
        router.push("/login");
    }

}

const checkToken = async () => {
    try {
        const response = await fetch(`${API}/checkauth`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                "uid": UID
            })
        });
        const data = await response.json();
        console.log(data);
        if (data["status"] !== 200) {
            throw new Error("Token Expired");
        }
        else {
            user.value = JSON.parse(data["data"]);
            auth.value = true;
        }
    }
    catch (e) {
        console.log(e);
        localStorage.setItem("TOKEN", "");
        localStorage.setItem("UID", "");
        router.push("/login");
    }

}

checkToken();
RenewToken();
setInterval(() => {
    RenewToken();
}, 1000 * 60 * 10);
</script>

<style scoped>
.left {
    height: 100%;
    overflow: hidden;
    transition: width 0.2s, min-width 0.2s;
}

.main {
    display: flex;
    height: 100svh;
}

.center {
    width: 100%;
    height: 100%;
    display: flex;
    background-color: var(--primary-light);
}
</style>