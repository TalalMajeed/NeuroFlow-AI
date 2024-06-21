<template>
    <div class="info-container">
        <div class="info-box" :style="boxStyle()">
            <div class="info-heading">More Info</div>
            <input type="file" id="file" style="display: none" />
            <div class="info-profile" @mouseover="imgopen = true" @mouseleave="imgopen = false" @click="uploadImg">
                <div class="info-cover" v-show="imgopen"><v-icon>mdi-camera</v-icon></div>
                <v-icon v-if="image == null">mdi-account</v-icon>
                <img class="info-imghandler" v-if="image != null" v-bind:src="image" cover></img>
            </div>
            <div class="info-email-text">Hi {{ name }}, Welcome to NeuroFlow</div>
            <div class="info-desc">Please Enter Information to continue</div>
            <v-form class="info-form" @submit.prevent>
                <v-responsive class="info-input-bar">
                    <v-textarea class="info-input-handler-desc" :rules="[required]" v-model="descriptionInput" no-resize
                        label="Tell us about yourself!" variant="outlined" rows="2"></v-textarea>
                </v-responsive>
                <v-btn :loading="loading" @click="sendData" class="info-button" type="submit" block>Continue</v-btn>
                <v-alert v-show="error" class="info-error" variant="tonal" color="error" text="Try Again!"></v-alert>
            </v-form>
        </div>
    </div>
</template>


<script setup>
import router from "./../router/index";
import { ref, onMounted } from "vue";
import { API, setToken, setUID, REG, setREG } from "../main"
import { TOKEN, UID } from "../main";


if (!TOKEN || !UID) {
    router.push("/login");
}

if (REG == false) {
    router.push("/register");
}


const showPassword = ref(false);

const passwordInput = ref(null);
const loading = ref(false);
const error = ref(false);
const image = ref(null);
const imgopen = ref(false);
const name = ref(null);
const descriptionInput = ref(null);
name.value = "";

onMounted(() => {
    requestName();
})

const requestName = async () => {
    try {
        const response = await fetch(API + '/info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                uid: UID
            })
        });
        const data = await response.json();
        console.log(data)
        if (data['status'] == '200') {
            name.value = data['message'].split(" ")[0];
        }
        else {
            throw new Error(data['message']);
        }
    } catch (error) {
        console.log(error)
        router.push("/login");
    }
}

const uploadImg = () => {
    document.getElementById('file').click();

    document.getElementById('file').onchange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();

        reader.onload = () => {
            const img = new Image();
            img.src = reader.result;

            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                let newWidth, newHeight;
                if (img.width > img.height) {
                    newWidth = 120;
                    newHeight = (img.height / img.width) * 120;
                } else {
                    newHeight = 120;
                    newWidth = (img.width / img.height) * 120;
                }

                canvas.width = newWidth;
                canvas.height = newHeight;

                ctx.drawImage(img, 0, 0, newWidth, newHeight);
                const resizedImage = canvas.toDataURL('image/jpeg');
                image.value = resizedImage;
            };
        };

        reader.readAsDataURL(file);
    };
};

const sendData = async () => {

    if (!descriptionInput.value) {
        return;
    }
    loading.value = true;
    try {
        const response = await fetch(API + '/saveinfo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                uid: UID,
                name: name.value,
                description: descriptionInput.value,
                image: image.value
            })
        });
        const data = await response.json();
        console.log(data)

        if (data['status'] == '200') {
            router.push("/panel");
        }
        else {
            throw new Error(data['message']);
        }
    } catch (error) {
        console.log(error)
        router.push("/login");
    }
    finally {
        loading.value = false;
        setREG(false);
    }
}


function required(v) {
    return !!v || 'Field is required'
}


function boxStyle() {
    return {
        maxHeight: error.value ? '700px' : '650px',
    }

}

function togglePassword() {
    showPassword.value = !showPassword.value;
    setTimeout(() => {
        passwordInput.value.focus();
        passwordInput.value.selectionStart = passwordInput.value.value.length;
    }, 0);
}

function login() {
    let checkUser = async () => {
        error.value = false;
        if (!passwordInput.value.value) return;
        loading.value = true;
        const response = await fetch(API + '/MoreInfo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: emailInput.value.value,
                password: passwordInput.value.value
            })
        });
        const data = await response.json();
        console.log(data)
        loading.value = false;
        if (data['status'] == '200') {
            console.log(data['data'])
            let temp = JSON.parse(data['data'])
            setToken(temp['token']);
            setUID(temp['uid']);
            router.push("/panel");
        }
        else {
            error.value = true;
        }
    }
    checkUser();
}

function shift() {
    router.push("/resetpassword");
}
</script>

<style scoped>
.info-form {
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-right: 5px;
}

.info-container {
    position: absolute;
    top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100svw;
    height: 100svh;
    background: var(--gradient-color)
}

.info-box {
    width: 460px;
    height: 95%;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: start;
    text-align: center;
    overflow-y: auto;
}

.info-heading {
    font-size: 32px;
    font-weight: 600;
    margin: 40px 0 25px 0;
}

.info-desc {
    margin: 5px 50px;
    margin-top: 10px;
    font-size: 17px;
    color: gray;
    font-weight: 300;
}

.info-button {
    margin-top: 20px;
    background-color: var(--primary);
    color: white;
    font-weight: 600;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 400;
    font-family: "Roboto";
    height: 50px !important;
}

.info-input-bar {
    width: 100%;
    display: flex;
    flex-grow: 0;
    padding: 30px 0px 0px 0px;
    width: 600px;
}

.forgot-container {
    display: flex;
    justify-content: end;
    width: 100%;
}

.info-input-handler-desc {
    width: 320px;
    margin-bottom: 5px;
    text-align: left;
    font-size: 14px;
    margin-top: 10px;
    height: 100px;
}

.info-error {
    width: 100%;
    margin-top: 20px;
    margin-bottom: -10px;
}

@media screen and (max-width: 500px) {
    .info-box {
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
        max-height: 100%;
        box-shadow: none;
    }

    .info-container {
        background: none;
    }

    .phone {
        flex-grow: 0;
        height: 30px;
    }

    .info-form {
        width: 85%;
    }

    .info-input-handler-desc {
        width: 100%;
    }
}

.info-email-text {
    margin-top: 30px;
    font-size: 22px;
    font-weight: 400;
}

.info-cover {
    background-color: var(--secondary);
    width: 150px;
    height: 150px;
    border-radius: 50%;
    position: absolute;
    z-index: 1;
    opacity: 0.5;
    display: flex;
    justify-content: center;
    align-items: center;
    pointer-events: none;
}

.info-imghandler {
    width: 100%;
    height: 100%;
    border-radius: 50%;
}

.info-profile {
    background-color: var(--primary);
    color: white;
    max-width: 150px;
    max-height: 150px;
    min-width: 150px;
    min-height: 150px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 50px;
    cursor: pointer;
    overflow: hidden;
}
</style>