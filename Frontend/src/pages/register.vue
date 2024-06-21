<template>
    <div class="registration-container">
        <div class="registration-box" :style="boxStyle()">

            <div class="registration-heading">Register Account</div>
            <div class="registration-description">Create Account to Continue!</div>
            <v-form class="registration-form" @submit.prevent>
                <v-responsive class="registration-input-bar">
                    <v-text-field class="registration-input-handler" :rules="[required]" ref="NameInput" label="Name"
                        variant="outlined"></v-text-field>

                    <div class="occupation-and-gender-container">
                        <div class="registration-occupation">
                            <v-text-field class="registration-input-handler" :rules="[required]" ref="OccupationInput"
                                label="Occupation" variant="outlined"></v-text-field>
                        </div>
                        <div class="registration-gender">
                            <v-autocomplete v-model="GenderInput" class="registration-input-auto" label="Gender"
                                :rules="[required]" :items="['Male', 'Female']" variant="outlined"></v-autocomplete>
                        </div>
                    </div>

                    <div class="registration-h2line"></div>


                    <v-text-field class="registration-input-handler" :rules="[required]" ref="emailInput" label="Email"
                        variant="outlined"></v-text-field>
                    <v-text-field class="registration-input-handler" :rules="[required]" ref="passwordInput"
                        label="Password" :type="showPassword ? 'text' : 'password'"
                        :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                        @click:append-inner="togglePassword" variant="outlined"></v-text-field>
                </v-responsive>


                <div class="registration-hline"></div>
                <v-btn :loading="loading" @click="login" class="registration-button" type="submit" block>Sign up</v-btn>
                <v-alert v-if="error.length > 0" class="registration-error" variant="tonal" color="error"
                    :text="error"></v-alert>
                <div class="registration-signup">Already have an Account?
                    <v-btn @click="shift" class="registration-login-button" variant="text">Log in!</v-btn>
                </div>
            </v-form>

        </div>
    </div>
</template>

<script setup>
import router from "./../router/index";
import { ref } from "vue";
import { API, setREG, setToken, setUID } from "../main"

const showPassword = ref(false);
const NameInput = ref(null);
const OccupationInput = ref(null);
const GenderInput = ref(null);
const emailInput = ref(null);
const passwordInput = ref(null);
const loading = ref(false);
const error = ref("");

function required(v) {
    return !!v || 'Field is required'
}


function boxStyle() {
    return {
        maxHeight: error.value ? '840px' : '780px',
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
        error.value = "";
        if (!emailInput.value.value || !passwordInput.value.value || !GenderInput.value || !OccupationInput.value.value || !NameInput.value.value) return;
        loading.value = true;

        try {
            const response = await fetch(API + '/createUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: emailInput.value.value,
                    password: passwordInput.value.value,
                    name: NameInput.value.value,
                    gender: GenderInput.value,
                    occupation: OccupationInput.value.value,

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
                setREG(true);
                router.push("/info");
            }
            else {
                error.value = data['message'];
            }
        }
        catch (e) {
            console.log(e);
            loading.value = false;
            error.value = "";

        }
    }
    checkUser();
}

function shift() {
    router.push("/login");
}
</script>

<style scoped>
.registration-form {
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-right: 5px;
}

.registration-container {
    position: absolute;
    top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100svw;
    height: 100svh;
    background: var(--gradient-color)
}

.registration-box {
    width: 500px;
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

.registration-heading {
    font-size: 32px;
    font-weight: 600;
    margin: 70px 0 20px 0;
}

.registration-description {
    font-size: 15px;
    margin: 5px 50px;
}

.registration-hline {
    width: 100%;
    height: 1px;
    background-color: #ccc;
    margin-top: 20px;
    margin-bottom: 20px;
}

.registration-h2line {
    width: 100%;
    height: 1px;
    background-color: #ccc;
    margin-bottom: 20px;
}

.registration-button {
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

.registration-input-bar {
    width: 100%;
    display: flex;
    flex-grow: 0;
    padding: 40px 0 0 0;
}

.registration-forgot {
    font-size: 16px;
    color: var(--primary);
    text-transform: none;
    letter-spacing: 0px;
    cursor: pointer;
    padding: 5px;
}

.registration-signup {
    font-size: 16px;
    margin-top: 20px;
    margin-bottom: 40px;
    display: flex;
    align-items: center
}

.registration-forgot-container {
    display: flex;
    justify-content: end;
    width: 100%;
}

.registration-input-handler {
    width: 100%;
    margin-bottom: 5px;
    text-align: left;
}

.registration-error {
    width: 100%;
    margin-top: 20px;
    margin-bottom: -10px;
}

.registration-login-button {
    font-size: 16px;
    color: var(--primary);
    text-transform: none;
    letter-spacing: 0px;
    cursor: pointer;
    padding: 5px;
}

.occupation-and-gender-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
}

.registration-gender {
    width: 165px;
}

.registration-occupation {
    width: 165px;
}

@media screen and (max-width: 500px) {
    .registration-box {
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
        max-height: 100%;
        border-radius: 0%;
        box-shadow: none;
    }

    .registration-container {
        background: none;
    }

    .registration-form {
        width: 85%;
    }

    .registration-heading {
        margin: 40px 0 10px 0;
    }

    .registration-gender,
    .registration-occupation {
        width: 100%;
    }

    .occupation-and-gender-container {
        gap: 20px;
    }
}
</style>