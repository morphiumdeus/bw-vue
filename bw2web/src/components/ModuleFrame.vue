<template>
  <div class="ModuleFrame">
    <h3>Select</h3>
    <div>
      <sui-input v-for="option in options" :key="option.comment" :type="option.inputType">option</sui-input>
    </div>
  </div>
</template>

<script>
import { EventBus } from '../event-bus';

export default {
  name: 'ModuleFrame',
  props: {
    currentModule: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      current: "",
      options: []
    }
  },
  created: function(){
    EventBus.$on('loadOptions',this.updateOptions)
  },
  computed: {
    
  },
  methods: {
    updateOptions: function(name){
      console.log(name)
      if(this.current !== name){
        this.axios.post(location.protocol+'//'+location.hostname+":5555/getOptions", {'module': name}).then(response => {
          console.log(response.data[0])
          this.options = response.data
        })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
