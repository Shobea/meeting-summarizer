import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import HowTo from '@/pages/HowTo.vue'
import Meetings from '@/pages/Meetings.vue'
import ScanNewID from '@/pages/ScanNewID.vue'
import CreateNewMeeting from '@/pages/CreateNewMeeting.vue'
import StartMeeting from '@/pages/StartMeeting.vue'
import Settings from '@/pages/Settings.vue'
import ViewMeeting from '@/pages/ViewMeeting.vue'
import ScanMeeting from '@/pages/ScanMeeting.vue'


const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/howto', name: 'HowTo', component: HowTo },
  { path: '/meetings', name: 'Meetings', component: Meetings },
  { path: '/scannewid', name: 'ScanNewID', component: ScanNewID },
  { path: '/scanmeeting', name: 'ScanMeeting', component: ScanMeeting },
  { path: '/createnewmeeting', name: 'CreateNewMeeting', component: CreateNewMeeting },
  { path: '/startmeeting', name: 'StartMeeting', component: StartMeeting },
  { path: '/settings', name: 'Settings', component: Settings },
  { path: '/viewmeeting', name: 'ViewMeeting', component: ViewMeeting }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
