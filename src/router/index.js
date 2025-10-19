import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import HowTo from '@/pages/HowTo.vue'
import Meetings from '@/pages/Meetings.vue'
import Scan from '@/pages/Scan.vue'
import CreateNewMeeting from '@/pages/CreateNewMeeting.vue'
import StartMeeting from '@/pages/StartMeeting.vue'
import Settings from '@/pages/Settings.vue'
import ViewMeeting from '@/pages/ViewMeeting.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/howto', name: 'HowTo', component: HowTo },
  { path: '/meetings', name: 'Meetings', component: Meetings },
  { path: '/scan', name: 'Scan', component: Scan },
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
