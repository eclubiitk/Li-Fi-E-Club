import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const state = {
  portdata: [],
  avports: [],
  updated: false,
  rogue: ''
}

const mutations = {
  setPortdata: (state, data) => (state.portdata = data),
  updateSuccess: (state) => {
    state.updated=true
    setTimeout(()=>(state.updated=false),2000)
  },
  setPortNumbers: (state, data) => (state.avports = data.data)
}

const actions = {
  async getPortdata({commit}) {
    const response = await axios.get(
      'http://localhost:30000/load'
    );
    commit('setPortdata', response.data);
  },
  async getPortNumbers({commit}) {
    const response = await axios.get(
      'http://localhost:30000/portvals'
    );
    commit('setPortNumbers', response.data);
  },
  async updatePortinfo({ commit }) {
    let dat=[]
    dat.push(state.portdata[0])
    dat.push(state.portdata[1])
    const response = await axios.post(
      'http://localhost:30000/load',
      dat
    );
    state.rogue=response;
    commit('updateSuccess')
  }
}

const getters ={
  dataPorts: state => state.portdata,
  availPort: state => state.avports,
  updateStatus: state => state.updated
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
