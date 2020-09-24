<template>
  <div class="ModuleChooser">
    <h3>Modules</h3>
    <div>
        <sui-button fluid compact class="spaced" v-for="module in orderedModules" :key="module.name" v-on:click="loadOptions(module.name)">{{module.displayName}}</sui-button>
    </div>
  </div>
</template>

<script>
import sortBy from "lodash"
import { EventBus } from '../event-bus'

export default {
  name: 'ModuleChooser',
  props: {},
  data: function () {
    return {
      modules: []
    }
  },
  computed: {
    orderedModules: function(){
      return this.modules.sort((a,b) =>  a.priority-b.priority)
    }
  },
  methods: {
    loadOptions: function(name){
      console.log(name)
      EventBus.$emit('loadOptions', name)
    }
  },
  mounted: function(){
    this.axios.get(location.protocol+'//'+location.hostname+":5555/getModules").then(response => {
        this.modules = response.data;
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.spaced {
    margin: 0.5rem !important;
}
</style>
