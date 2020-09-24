<template>
  <div id="app">
    <sui-grid>
      <sui-grid-column :width=1>
        <ModuleChooser />
      </sui-grid-column>
      <sui-grid-column :width=2>
        <ModuleFrame :currentModule="currentModule" />
      </sui-grid-column>
      <sui-grid-column :width=6>
        <EditorFrame v-on:broadcastResults="broadcastResults" />
      </sui-grid-column>
      <sui-grid-column :width=7>
        <ResultFrame :displayableResult="displayableResult" />
      </sui-grid-column>
    </sui-grid>
  </div>
</template>

<script>
import ModuleChooser from './components/ModuleChooser.vue'
import ModuleFrame from './components/ModuleFrame.vue'
import EditorFrame from './components/EditorFrame.vue'
import ResultFrame from './components/ResultFrame.vue'
import store from './store'

export default {
  name: 'app',
  components: {
    ModuleChooser,
    ModuleFrame,
    EditorFrame,
    ResultFrame
  },
  store,
  methods: {
    broadcastResults: function(results){
      console.log('app received: ', results);
      this.displayableResult = results;
    },
    loadOptions: function(module){
      console.log('app received: ', module);
      this.currentModule = module
    }
  },
  data: function() {
    return {
      displayableResult: [],
      currentModule: ''
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 10px;
  height: 100%;
}
.grid, .column {
  height: 100%;
}
h1 {
  font-size: 1em;
}
a {
  color: #42b983;
}

</style>
