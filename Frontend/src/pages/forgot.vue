<template>
    <div class="reset-password-container">
        <div class="reset-password-box" :style="boxStyle()">

            <div class="reset-password-heading">Reset Password</div>
            <div class="reset-password-desc">You have requested to reset password for</div>
            <div class="reset-password-email">{{ email }}</div>
            <div class="reset-password-desc">Please Enter a new Password for your Account</div>

            <v-form class="reset-password-form" @submit.prevent>
                <v-responsive class="reset-password-input-bar">


                    <div class="reset-password-hline"></div>


                    <v-text-field class="reset-password-input-handler" :rules="[required]" ref="passwordInput"
                        label="Password" :type="showPassword ? 'text' : 'password'"
                        :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                        @click:append-inner="togglePassword" variant="outlined"></v-text-field>
                </v-responsive>


                <v-btn :loading="loading" @click="reset" class="reset-password-button" type="submit" block>Reset
                    Password</v-btn>
                <v-alert v-show="error" class="reset-password-error" variant="tonal" color="error"
                    text="Try Again!"></v-alert>

            </v-form>

        </div>
    </div>
</template>

<script setup>
import router from "./../router/index";
import { ref, onMounted } from "vue";
import { API, setToken, setUID, TOKEN, UID, RESET, setRESET } from "../main"

const showPassword = ref(false);

const passwordInput = ref(null);
const loading = ref(false);
const error = ref(false);
const email = ref("");

/*if (!TOKEN || !UID) {
    router.push("/login");
}

if (!RESET) {
    router.push("/login");
}*/

onMounted(() => {
    requestEmail();
})

const requestEmail = async () => {
    try {
        const response = await fetch(API + '/email', {
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

            email.value = data['message'].split(" ")[0];
        }
        else {
            throw new Error(data['message']);
        }
    } catch (error) {
        console.log(error)
        router.push("/login");
    }
}

function required(v) {
    return !!v || 'Field is required'
}


function boxStyle() {
    return {
        maxHeight: error.value ? '640px' : '600px',
    }

}

function togglePassword() {
    showPassword.value = !showPassword.value;
    setTimeout(() => {
        passwordInput.value.focus();
        passwordInput.value.selectionStart = passwordInput.value.value.length;
    }, 0);
}

const reset = async () => {
    error.value = false;
    if (!passwordInput.value.value) return;
    loading.value = true;
    try {
        const response = await fetch(API + '/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                uid: UID,
                password: passwordInput.value.value
            })
        });
        const data = await response.json();
        console.log(data)
        loading.value = false;
        if (data['status'] == '200') {
            setRESET(false);
            router.push("/login");
        }
        else {
            throw new Error(data['message']);
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


function shift() {
    router.push("/resetpassword");
}
</script>

<style scoped>
.reset-password-form {
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-right: 5px;
}

.reset-password-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100svw;
    height: 100svh;
    background: var(--gradient-color)
}

.reset-password-box {
    width: 480px;
    height: 90%;
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


img {
    width: 160px;
    margin-top: 20px;
    user-select: none;
}

.reset-password-heading {
    font-size: 32px;
    font-weight: 600;
    margin: 70px 0 40px 0;
}

.reset-password-desc {
    font-size: 17px;
    margin: 10px 50px;
}

.reset-password-hline {
    width: 100%;
    height: 1px;
    background-color: #ccc;
    margin-top: 20px;
    margin-bottom: 40px;
}



.reset-password-button {
    margin-top: 30px;
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

.reset-password-input-bar {
    width: 100%;
    display: flex;
    flex-grow: 0;
    padding: 40px 0 0 0;
}


.forgot-container {
    display: flex;
    justify-content: end;
    width: 100%;
}

.reset-password-input-handler {
    width: 100%;
    margin-bottom: 5px;
    text-align: left;
}

.reset-password-error {
    width: 100%;
    margin-top: 20px;
    margin-bottom: -10px;

}

@media screen and (max-width: 500px) {
    .reset-password-box {
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
        max-height: 100%;
        box-shadow: none;
    }

    .reset-password-container {
        background: none;
    }

    .phone {
        flex-grow: 0;
        height: 30px;
    }

    .reset-password-form {
        width: 85%;
    }

    .reset-password-heading {
        margin: 20px 0 30px 0;
    }
}


.reset-password-email {
    color: #2094AB;
    font-size: 17px;
}
</style>