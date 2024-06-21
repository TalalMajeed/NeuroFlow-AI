<template>
  <div class="container">
    <div class="title">Dashboard</div>
    <div class="divider">
      <v-card class="card">
        <div class="heading">User Information</div>
        <div class="divider">
          <div class="profilecontainer">
            <div class="usertitle">{{ props.user["name"] }}</div>
            <div class="userid"><b>Email:</b> {{ props.user["email"] }}</div>
            <div class="userid"><b>User ID:</b> {{ props.user["id"] }}</div>
            <div class="userid">{{ props.user["description"] }}</div>
          </div>
          <div class="imgcontainer">
            <div class="profile">
              <img class="profile-pic" v-show="props.user['image'] != null" :src="props.user['image']"></img>
              <v-icon v-show="props.user['image'] == null">mdi-account</v-icon>
            </div>
            <v-btn class="button" @click="signOut">Sign Out</v-btn>
          </div>
        </div>
      </v-card>
      <v-card class="card">
        <div class="heading">Account Analytics</div>
        <div class="divider">

          <div class="analyticscontainer">
            <div class="usertitle">Usage Details</div>
            <div class="userid"><b>Boards Saved Today:</b> {{ props.user["today"] }}</div>
            <div class="userid"><b>Total Generated:</b> {{ props.user["total"] }}</div>
            <div class="userid"><b>Total Saved Boards:</b> {{ props.user["diagramCount"] }}</div>

          </div>
          <div class="graphdata">
            <div class="keycontainer">
              <div class="key">
                <div class="key1"></div>
                <div><b>Saved Today
                  </b></div>
              </div>
              <div class="key">
                <div class="key2"></div>
                <div><b>Total Saved
                  </b></div>
              </div>
            </div>
            <div class="graphcontainer">
              <Pie :options="chartOptions" :data="chartData" width="300" height="300" />
            </div>
          </div>

        </div>
      </v-card>
    </div>
    <div class="title" style="margin-top:50px;">Recent Boards</div>
    <div class="divider">
      <div class="smallercontainer">
        <div class="boxcontainer" v-for="i in userDiagrams">
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
        <div class="boxcontainer" v-if="userDiagrams.length < 1">
          <v-card class="mx-auto no-recent">
            <div>No Recent Diagram!</div>
          </v-card>
        </div>
        <div class="boxcontainer" v-if="userDiagrams.length < 2">
          <v-card class="mx-auto no-recent">
            <div>No Recent Diagram!</div>
          </v-card>
        </div>
      </div>
      <div class="container2">
        <v-card class="manageprofile">
          <v-card-item>
            <v-card-title class="cardmanageprofileheader">
              Manage Profile
            </v-card-title>
          </v-card-item>
          <v-card-text class="container2-text">
            Easily customize your profile with options for updating personal information, preferences, and
            security
            settings. Streamline user experience, ensuring data accuracy and privacy. Accessible across devices
            for
            seamless profile management.
          </v-card-text>
          <v-btn @click="userPage" class="button btn2">Manage Profile</v-btn>
        </v-card>
        <v-card class="createboard">
          <v-card-item>
            <v-card-title class="cardcreateboardheader">
              Create Board
            </v-card-title>
          </v-card-item>
          <v-card-text class="container2-text">
            Effortlessly generate flowcharts with an intuitive interface, code integration, and collaboration
            tools.
            Streamline workflows, enhance code quality, and facilitate effective communication among team members.
          </v-card-text>
          <v-btn @click="boardPage" class="button btn2">Create Board</v-btn>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, watch, defineEmits } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { Pie } from 'vue-chartjs'
import { setToken, setUID, TOKEN, API, UID } from "../main";
import router from "../router";




ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)
const emit = defineEmits(['trigger']);

const props = defineProps({
  user: Object,
  setPage: Function,
  page: Number
});

const getRecent = async () => {
  try {
    const response = await fetch(`${API}/getRecent`, {
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
      userDiagrams.value = JSON.parse(data['data']);
    }
    else {
      throw new Error(data['message'])
    }
  }
  catch (err) {
    console.log(err);
  }
}

const userDiagrams = ref(props.user['diagrams']);
const chartData = {
  labels: ['Saved Today', 'Total Saved'],
  datasets: [{
    data: [(props.user["today"]), props.user["diagramCount"]],
    backgroundColor: [
      'rgba(155, 155, 155, 0.2)',
      'rgba(54, 162, 235, 0.2)',
    ],
    borderColor: [
      'rgba(155, 155, 155, 1)',
      'rgba(54, 162, 235, 1)',
    ],
    borderWidth: 1
  }]
};
const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: ''
    }
  }
}

watch(() => props.page, (next) => {
  userDiagrams.value = [];
  if (next == 0) {
    getRecent();
  }
});

const signOut = () => {
  setToken("");
  setUID("");
  router.push("/login");
}

const userPage = () => {
  props.setPage(1);
}

const boardPage = () => {
  props.setPage(3);
}

const openBoard = (e) => {
  emit("trigger", e["DiagramID"]);

  let t = e["loading"];

  userDiagrams.value = userDiagrams.value.map(d => {
    if (d["DiagramID"] == e["DiagramID"]) {
      d["loading"] = !t;
    }
    return d;
  });
}

</script>


<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  overflow-y: scroll;
  padding: 20px;
  padding-bottom: 120px;
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

.heading {
  font-weight: 400;
  letter-spacing: 2px;
  font-size: 14px;
  text-transform: uppercase;
  color: var(--secondary);
  margin-bottom: 10px;
}

.usertitle {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--secondary);
  margin-bottom: 10px;
}

.userid {
  font-size: 1rem;
  font-weight: 400;
  color: var(--secondary);
  margin-bottom: 10px;
}

.divider {
  display: flex;
  width: 100%;
  gap: 20px;
  justify-content: space-between;
}

.button {
  color: white;
  font-weight: 300;
  width: 150px;
  height: 40px !important;
  background-color: var(--primary);
}

.imgcontainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  justify-content: space-around;
  height: 180px;
}

.profilecontainer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.analyticscontainer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.profile {
  background-color: var(--primary);
  color: white;
  max-width: 110px;
  max-height: 110px;
  min-width: 110px;
  min-height: 110px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 50px;
}

.graphcontainer {
  height: 160px;
  width: 160px;
  min-width: 160px;
  min-height: 160px;
  overflow: hidden;
}

.smallercontainer {
  margin-top: 20px;
  display: flex;
  gap: 20px;
  width: 100%;
  justify-content: space-between;
}

.textfield {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--secondary);
  margin: 40px 0 0 0;
}

.boxcontainer {
  width: 100%;
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


.side-by-side {
  display: flex;
  justify-content: space-between;
}

.spacer {
  width: 50px;
}

.manageprofile {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.createboard {
  align-self: flex-end;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cardmanageprofileheader,
.cardcreateboardheader {
  color: #0D6274;
  font-size: 30px;
  margin: 20px;
  text-align: center;
}

.container2 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  height: calc(100% - 20px);
  gap: 20px;
  margin-top: 20px;
}

.container2-text {
  font-size: 1.2rem;
  font-weight: 300;
  line-height: 30px !important;
  color: var(--secondary);
  margin: 10px 20px;
  height: 100px !important;
  overflow: hidden
}

.profile-pic {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.key1 {
  width: 20px;
  height: 20px;
  min-width: 20px;
  min-height: 20px;
  background-color: rgba(155, 155, 155, 0.2);
  border: 1px solid rgba(155, 155, 155, 1);
}

.key2 {
  width: 20px;
  height: 20px;
  min-width: 20px;
  min-height: 20px;
  background-color: rgba(54, 162, 235, 0.2);
  border: 1px solid rgba(54, 162, 235, 1);
}

.key {
  display: flex;
  gap: 20px;
}

.keycontainer {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 160px;
  justify-content: center;
}

.graphdata {
  display: flex;
  gap: 40px;
}

.btn2 {
  width: 80%;
  height: 40px !important;
  margin-bottom: 30px;
}

.no-recent {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 450px;
  width: 100%;
  font-size: 1.5rem;
  font-weight: 300;
  color: var(--secondary);
}
</style>
