import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home'
import About from './views/About'
import dataTable from './components/dataTable'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/load',
      name: 'load',
      component: dataTable
    },
    // {
    //   path: '/go',
    //   name: 'processor',
    //   component: processor
    // }
  ]
})
