<template>
    <div class="container">
        <div class="center">
            <div class="title-bar">
                <div class="diagram-title">
                    {{ flowTitle }}
                    <span style="font-weight: 300">- {{ diagramID }}</span>
                </div>
                <div class="title-controls">
                    <div class="diagram-controls">

                        <v-btn icon="mdi-select-drag" @click="position" class="cbutton"></v-btn>
                        <v-btn icon="mdi-cursor-move" @click="drag" class="cbutton"> </v-btn>
                    </div>
                    <v-btn class="tbutton" @click="newDiagram">New</v-btn>
                    <v-btn class="tbutton" @click="showSave = true">Save</v-btn>
                    <v-btn class="tbutton" @click="eraseDiagram" :loading="deleteLoading">Delete</v-btn>
                </div>
            </div>
            <canvas id="main-canvas" :width="cw" :height="ch"></canvas>
            <input id="text"></input>
        </div>
        <div class="right">
            <div class="title">Generate</div>
            <v-form @submit.prevent>
                <v-responsive class="text-bar">
                    <div>Enter a general description related to a Real World Problem</div>
                    <v-textarea rows="4" no-resize class="input-handler" :rules="[required]" v-model="descriptionInput"
                        label="Description" variant="outlined"></v-textarea>
                    <div>Enter the set of Required Technologies or Resources</div>
                    <v-textarea rows="4" no-resize class="input-handler" :rules="[required]" v-model="languagesInput"
                        label="Technologies" variant="outlined"></v-textarea>
                    <div>Provide further Context for generation (Optional)</div>
                    <v-textarea rows="4" no-resize class="input-handler" :rules="[required]" v-model="contextInput"
                        label="Context" variant="outlined"></v-textarea>
                </v-responsive>
                <v-btn class="button" :loading="loading" @click="generate" type="submit">Generate</v-btn>
                <v-alert v-show="error" class="generate-error" variant="tonal" color="error"
                    text="Generation Error!"></v-alert>
            </v-form>
        </div>
        <v-dialog v-model="showSave" max-width="400" persistent>
            <v-card prepend-icon="mdi-content-save" text="" title="Save Flow?">
                <template v-slot:actions>
                    <div class="save-dialog">
                        <v-text-field class="save-text" v-model="flowTitle" label="Title"
                            variant="outlined"></v-text-field>


                        <div class="save-buttons">
                            <v-spacer></v-spacer>
                            <v-btn @click="showSave = false">
                                Go Back
                            </v-btn>

                            <v-btn @click="saveDiagram" :loading="saveLoading">
                                Save
                            </v-btn>
                        </div>

                    </div>

                </template>
            </v-card>
        </v-dialog>
    </div>
</template>

<script setup>

import { defineProps, onMounted, ref, watch } from 'vue';
import { Flowchart } from './flowchart.js';
import { UID, API, TOKEN } from '../main.js';

let frame = ref(null);
let descriptionInput = ref('');
let languagesInput = ref('');
let contextInput = ref('');
let loading = ref(false);
let showSave = ref(false);
let saveLoading = ref(false);
let flowTitle = ref("Unititled");
let diagramID = ref("Unsaved");
let deleteLoading = ref(false);
let error = ref(false);

const required = (v) => !!v || 'Field is Required!';

const props = defineProps({
    user: Object,
    open: Boolean,
    board: Object,
    setPage: Function
});

const position = () => {
    console.log("Position");
    frame.value.cursorShift = false;
}

const drag = () => {
    console.log("Drag");
    frame.value.cursorShift = true;
}

const newDiagram = () => {
    flowTitle.value = "Unititled";
    diagramID.value = "Unsaved";
    frame.value.setFlowState([[], []]);
}

const resize = () => {
    const canvas = document.getElementById('main-canvas');
    canvas.width = window.innerWidth - 420;
    canvas.height = window.innerHeight - 120;
    if (frame.value) {
        frame.value.resizeCanvas(window.innerWidth - 420, window.innerHeight - 120);
    }
}

const requestDiagram = async () => {
    console.log(props.board[0]);
    if (!props.board[0]) {
        return;
    }
    try {
        const res = await fetch(`${API}/getdiagram`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                did: props.board[0]
            })
        });

        const data = await res.json();
        if (data.status == '200') {
            console.log("THUASD")
            let temp = JSON.parse(data['data']);
            diagramID.value = temp['DiagramId'];
            flowTitle.value = temp['name'];
            let j = temp['data'];
            frame.value.setFlowState(JSON.parse(j));
            props.setPage(3);
        }
        else {
            throw new Error(data.message);
        }
    }
    catch (e) {
        console.log(e);
    }
}

watch(() => props.board, (next) => {
    if (next != null) {
        console.log(next);
        console
        console.log(next[0]);
        requestDiagram();
    }
});

onMounted(() => {
    resize();
    console.log('mounted');
    frame.value = new Flowchart('main-canvas');
})

const eraseDiagram = async () => {
    if (!diagramID.value || diagramID.value == "Unsaved") {
        flowTitle.value = "Unititled";
        frame.value.setFlowState([[], []]);
        return;
    }
    deleteLoading.value = true;
    try {
        const res = await fetch(`${API}/deletediagram`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                did: diagramID.value
            })
        });

        const data = await res.json();
        if (data.status == '200') {
            console.log(data);
            diagramID.value = "Unsaved";
            flowTitle.value = "Unititled";
            frame.value.setFlowState([[], []]);
            props.setPage(3);
        }
        else {
            throw new Error(data.message);
        }
    }
    catch (e) {
        console.log(e);
    }
    finally {
        deleteLoading.value = false;
    }
}
const saveDiagram = async () => {
    if (!flowTitle.value) {
        return;
    }
    let x = frame.value.getFlowState();
    saveLoading.value = true;

    try {
        const res = await fetch(`${API}/savediagram`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                uid: UID,
                title: flowTitle.value,
                data: x,
                did: diagramID.value
            })
        });

        const data = await res.json();
        if (data.status == '200') {
            console.log(data);
            diagramID.value = data['data'];
        }
        else {
            throw new Error(data.message);
        }
    }
    catch (e) {
        console.log(e);
    }
    finally {
        saveLoading.value = false;
        showSave.value = false;
    }

}


const generate = async () => {
    if (!descriptionInput.value || !languagesInput.value || !contextInput.value) {
        return;
    }
    error.value = false;
    loading.value = true;
    //Replace all new lines with commas
    descriptionInput.value = descriptionInput.value.replace(/\n/g, ' ');
    languagesInput.value = languagesInput.value.replace(/\n/g, ' ');
    contextInput.value = contextInput.value.replace(/\n/g, ' ');
    try {
        const res = await fetch(`${API}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                description: descriptionInput.value,
                languages: languagesInput.value,
                context: contextInput.value
            })
        });
        const data = await res.json();

        if (data.status == '200') {
            let extract = data['data']
            let id = data['id'];
            console.log(extract);
            console.log(id);
            let dim = frame.value.setData(extract[0]);

            const res2 = await fetch(`${API}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'authorization': `Bearer ${TOKEN}`
                },
                body: JSON.stringify({
                    id: id,
                    dim: dim,
                    uid: UID
                })
            });

            const data2 = await res2.json();
            if (data2.status == '200') {
                let dimensions = data2['data'][0];
                let connections = data2['data'][1];

                connections = connections.map((c) => {
                    return [parseInt(c[0].replace('B', '')) - 1, parseInt(c[1].replace('B', '')) - 1, c[2], c[3]]
                });
                console.log(connections);
                frame.value.setRender(dimensions, connections)

                console.log(frame.value.getFlowState());
            }
            else {
                throw new Error(data2.message);
            }
        }
        else {
            throw new Error(data.message);
        }
    }
    catch (e) {
        console.log(e);
        error.value = true;
    }
    finally {
        loading.value = false;
    }
}

window.addEventListener('resize', resize);

</script>


<style scoped>
canvas {}

#text {
    position: absolute;
    left: 0;
    outline: none;
    font-family: "Arial";
    font-size: 16px;
    display: none;
    text-align: center;
    border: none;
    color: black;
}

.center {
    flex-grow: 1;
}

.container {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 100%;
}

.title {
    font-size: 2rem;
    font-weight: bold;
    color: var(--secondary);
    text-align: center;
}

.right {
    position: absolute;
    height: calc(100% - 128px);
    right: 0;
    min-width: 350px;
    max-width: 350px;
    padding: 20px;
    background-color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-y: auto;
}

.desc {
    margin: 20px 0;
}

.input-handler {
    width: 100%;
    margin: 15px 0;
}

.text-bar {
    margin-top: 30px;
    width: 100%;
}


.button {
    color: white;
    font-weight: 300;
    width: 100%;
    height: 45px !important;
    margin-bottom: 10px;
    background-color: var(--primary);
}

.title-bar {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    align-items: center;
    max-width: calc(100% - 350px);
    border: 2px;
}

.diagram-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--secondary);
    text-align: center;
}

.title-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.diagram-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-right: 50px;
}


.tbutton {
    color: white;
    font-weight: 300;
    height: 40px !important;
    background-color: var(--primary);
    width: 120px;
}

.cbutton {
    color: white;
    font-weight: 300;
    height: 40px !important;
    background-color: var(--primary);
    width: 40px;
}

.save-dialog {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    width: 100%;
}

.save-buttons {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: end;
    margin-top: 20px;
    width: 100%;
    padding: 0 5px;
}

.generate-error {
    margin-top: 10px;
    text-align: center;
}

.save-text {
    width: 90%;
}
</style>