<template>
    <div class="landing-container">
        <div class="landing-box">
            <img src="../assets/Logo.png" alt="" class="landing-logo">
            <div class="landing-heading">NeuroFlow AI</div>
            <div class="landing-desc">An application which uses Generative AI to create Work Flows for Coding Projects &
                Applications</div>
            <div class="landing-desc">Dear User! Welcome to NeuroFlow</div>

            <div class="spacer phone"></div>
            <div class="landing-hline"></div>
            <div class="spacer phone"></div>
            <v-btn @click="login" class="landing-button">Get Started</v-btn>
            <div class="landing-copyright">© TechFlow - SEECS NUST - GenAI 2024</div>
        </div>
    </div>
</template>

<script setup>
import router from "./../router/index";

function login() {
    router.push("/login");
}
</script>

<style scoped>
.landing-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100svw;
    height: 100svh;
    background: var(--gradient-color);
}


.landing-box {
    width: 500px;
    height: 90%;
    max-height: 650px;
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

.landing-logo {
    width: 120px;
    margin-top: 50px;
    margin-bottom: 20px;
    user-select: none;
}

.landing-heading {
    font-size: 32px;
    font-weight: 600;
    margin: 10px 0 20px 0;
}

.landing-desc {
    font-size: 17px;
    margin-top: 10px;
    margin: 10px 50px;
}

.landing-hline {
    width: 75%;
    height: 1px;
    background-color: #ccc;
    margin-top: 20px;
}

.landing-copyright {
    font-size: 17px;
    color: gray;
    margin-top: 20px;
    margin-bottom: 30px;
}

.landing-button {
    margin-top: 20px;
    background-color: var(--primary);
    color: white;
    font-weight: 600;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 400;
    width: 75%;
    margin-bottom: 20px;
    height: 50px !important;
}

@media screen and (max-width: 500px) {
    .landing-box {
        width: 100%;
        height: 100%;
        max-height: 100%;
        align-items: center;
        justify-content: center;
    }

    .phone {
        flex-grow: 0;
        height: 30px;
    }

    .landing-desc {
        margin: 10px 20px;
    }

    .landing-button {
        width: 85%;
    }

    .landing-hline {
        width: 85%;
    }
}
</style>
