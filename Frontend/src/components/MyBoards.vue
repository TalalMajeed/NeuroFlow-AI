<template>
    <div class="container">
        <div class="title">My Boards</div>
        <v-card class="card">
            <div class="heading">Search Boards</div>
            <div class="divider">
                <v-responsive>
                    <v-text-field v-model="filterText" variant="outlined" placeholder="Search Boards"></v-text-field>
                </v-responsive>
            </div>
        </v-card>
        <div class="title" style="margin-top:50px;">Recent Boards</div>
        <div class="divider">
            <div class="smallercontainer">
                <div class="boxcontainer" v-for="i in boards">
                    <v-card class="mx-auto">
                        <v-img max-height="250px" src="@/assets/document.png" cover></v-img>
                        <div class="textfield">{{ i['name'] }}</div>
                        <div class="hline"></div>
                        <div class="boxcontainer-sub">
                            <v-btn class="boxcontainer-button" text="Open Board" :loading="i['loading']"
                                @click="() => { openBoard(i); }"></v-btn>
                            <img class="genailogo" height="35px" width="35px" src="../assets/logo.png" cover></img>
                        </div>
                    </v-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import { API, TOKEN, UID } from '../main';

const props = defineProps({
    user: Object,
    page: Number,
    setPage: Function
});

const emit = defineEmits(['trigger']);

const Totalboards = ref([]);
const boards = ref([]);
const filterText = ref('');

watch(() => filterText.value, (next) => {
    boards.value = Totalboards.value.filter(d => d["name"].toLowerCase().includes(next.toLowerCase()));
});

watch(() => props.page, (next) => {
    if (next == 2) {
        getData();
    }
    Totalboards.value = [];
    boards.value = [];
});

const openBoard = (e) => {
    emit("trigger", e["DiagramID"]);

    let t = e["loading"];

    boards.value = boards.value.map(d => {
        if (d["DiagramID"] == e["DiagramID"]) {
            d["loading"] = !t;
        }
        return d;
    });
}

const getData = async () => {
    try {
        const response = await fetch(`${API}/getdiagrams`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                'uid': UID
            })
        });
        const data = await response.json();

        if (data.status == '200') {
            console.log(JSON.parse(data['data']));
            let temp = JSON.parse(data['data']);
            temp = temp.map(d => {
                return { DiagramID: d["DiagramId"], name: d["name"], loading: false }
            })

            Totalboards.value = temp
            boards.value = temp
        }
        else {
            throw new Error(data['message'])
        }
    }
    catch (err) {
        console.log(err);
    }
}

onMounted(() => {
    getData();
});
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    width: 100%;
    overflow-y: scroll;
    padding: 20px;
}

.title {
    font-size: 2rem;
    font-weight: bold;
    color: var(--secondary);
}

.card {
    padding: 20px;
    width: 100%;
    margin-top: 20px;
}

.smallercontainer {
    margin-top: 20px;
    display: flex;
    gap: 20px;
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: start;
    padding-bottom: 100px !important;
}

.textfield {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--secondary);
    margin: 40px 0 0 0;
}

.boxcontainer {
    width: 100%;
    max-width: 400px;
    height: 100%;
    transition: box-shadow 0.3s ease;
}

.hline {
    border-top: 1px solid #0D6274;
    margin: 20px 0 20px 0;
}

.mx-auto {
    padding: 20px;
}

.boxcontainer-sub {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 0 0 10px 0;
}

.boxcontainer-button {
    background-color: var(--primary);
    color: white;
    width: 150px;
    height: 40px !important;
    font-weight: 400;
}

.placeholder-padded::placeholder {
    padding-left: 5px;
}

.card {
    padding: 20px;
    width: 100%;
    margin-top: 20px;
}

.heading {
    font-weight: 400;
    letter-spacing: 2px;
    font-size: 14px;
    text-transform: uppercase;
    color: var(--secondary);
    margin-bottom: 10px;
}

.divider {
    height: 80px
}
</style>